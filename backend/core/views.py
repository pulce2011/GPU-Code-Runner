import tempfile
import shutil
import subprocess
import threading
import time
import os
import select
from typing import Dict, Any, Optional
from django.conf import settings
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Exercise, Course, User, Task
from .serializers import ExerciseSerializer, UserSerializer, CourseSerializer, TaskSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# =============================================================================
# AUTENTICAZIONE E GESTIONE UTENTI
# =============================================================================
# Informazioni utente corrente
class UserInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Registrazione utente
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# =============================================================================
# GESTIONE CORSI ED ESERCIZI
# =============================================================================
# Lista corsi
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


# Lista esercizi filtrati per corso
class ExerciseListView(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser:
            return Exercise.objects.all()
        
        if user.course:
            return Exercise.objects.filter(courses=user.course)
        return Exercise.objects.none()
    

# =============================================================================
# CONSULTAZIONE E RECUPERO TASK
# =============================================================================

# Lista task dell'utente
class TaskListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:10]
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# Dettagli di un task specifico
class TaskDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id: int) -> Response:
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({'error': 'Task non trovato'}, status=status.HTTP_404_NOT_FOUND)



# =============================================================================
# ESECUZIONE CODICE E GESTIONE TASK
# =============================================================================

# Esecuzione codice con sistema crediti
class RunExerciseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    ### Richiesta POST /api/run/ ###
    def post(self, request) -> Response:
        # Validazione input
        validation_error = self._validate_request(request)
        if validation_error:
            return validation_error
        
        # Recupero dati input
        code = request.data['code']
        exercise_id = request.data['exercise_id']
        user = request.user

        # Controllo crediti
        task_start_cost = settings.TASK_START_COST
        if not user.has_credits(task_start_cost):
            return self._error_response('Crediti insufficienti.', status.HTTP_402_PAYMENT_REQUIRED)

        # Recupero esercizio
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            
            # Deduce crediti per avviare il task
            if not user.reduce_credits(task_start_cost):
                return self._error_response('Crediti insufficienti.', status.HTTP_402_PAYMENT_REQUIRED)
            
            # Crea il task
            task = self._create_task(user, exercise, code)
            
            # Controlla se può essere avviato immediatamente o va in coda
            if Task.can_start_new_task():
                self._start_task_execution(task)
                message = 'Lavoro avviato con successo'
            else:
                message = f'Lavoro aggiunto alla coda (posizione: {Task.objects.filter(status="pending").count()})'
            
            return Response({
                'task_id': task.id,
                'status': task.status,
                'message': message
            })
            
        # Gestione errori
        except Exercise.DoesNotExist:
            return self._error_response('Esercizio non trovato', status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return self._error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    ### Valida i dati della richiesta ###
    def _validate_request(self, request) -> Optional[Response]:
        if not request.data.get('code'):
            return self._error_response('Il campo "code" è obbligatorio.', status.HTTP_400_BAD_REQUEST)
        
        if not request.data.get('exercise_id'):
            return self._error_response('Errore nel recupero dell\'esercizio.', status.HTTP_404_NOT_FOUND)
        
        # Controllo lunghezza massima del codice sorgente
        code = request.data.get('code', '')
        if len(code) > settings.MAX_SOURCE_CODE_LENGTH:
            return self._error_response(
                f'Raggiunto limite massimo di {settings.MAX_SOURCE_CODE_LENGTH} caratteri.', 
                status.HTTP_400_BAD_REQUEST
            )
        
        return None
    
    ### Crea una risposta di errore standardizzata ###
    def _error_response(self, message: str, status_code: int) -> Response:
        return Response({'message': message}, status=status_code)
    
    ### Crea un nuovo task ###
    def _create_task(self, user: User, exercise: Exercise, code: str) -> Task:
        task = Task.objects.create(
            user=user,
            exercise=exercise,
            code=code,
            credits_cost=settings.TASK_START_COST,
        )
        task.pending()
        return task
    
    ### Crea un thread per eseguire il task in background ###
    def _start_task_execution(self, task: Task) -> None:
        thread = threading.Thread(target=self._execute_task, args=(task,))
        thread.daemon = True
        thread.start()

    ### Esecuzione del task in background con controllo crediti ###
    def _execute_task(self, task: Task) -> None:
        tmp_path = None
        try:
            # Avvia il task
            task.start()
            self._ws_broadcast(task)
            tmp_path = self._create_temp_file(task.code, task.exercise)
            process = self._start_process(tmp_path, task.exercise)
            task.process_id = process.pid
            task.save()
            self._ws_broadcast(task)

            # Monitoraggio task
            output_data = self._monitor_process(process, task, tmp_path)
            
            if not output_data['interrupted']:
                self._finalize_task(task, process, output_data)
            
        except Exception as e:
            task.fail(
                stdout='',
                stderr=f'Errore durante l\'esecuzione: {str(e)}',
                message=f'Errore durante l\'esecuzione: {str(e)}'
                )
            self._ws_broadcast(task)
            # Pulisce il file temporaneo anche in caso di errore
            self._cleanup_temp_file(tmp_path)
    
    ### Crea un file temporaneo con il codice in ./gpu/<exercise.name> ###
    def _create_temp_file(self, code: str, exercise: Exercise) -> str:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gpu', exercise.name))
        os.makedirs(base_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=exercise.file_extension,
            prefix='tmp_',
            delete=False, # Deve essere 'False' per evitare che il file non venga usato esternamente
            dir=base_dir
        ) as f:
            f.write(code)
            return f.name
    
    ### Avvia il processo di esecuzione ###
    def _start_process(self, tmp_path: str, exercise: Exercise) -> subprocess.Popen:
        
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'run_exercise.sh'))
        
        if shutil.which('stdbuf'):
            # Con controllo buffering
            cmd = ['stdbuf', '-oL', '-eL', 'bash', script_path, tmp_path, exercise.name]
        else:
            cmd = ['bash', script_path, tmp_path, exercise.name]

        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    
    ### Monitora il processo e gestisce i crediti ###
    def _monitor_process(self, process: subprocess.Popen, task: Task, tmp_path: str = None) -> Dict[str, Any]:
        # Variabili per accumulare l'output del processo
        stdout = ""
        stderr = ""
        last_broadcast_stdout_len = 0  # Lunghezza ultimo broadcast per evitare duplicati
        last_broadcast_stderr_len = 0  # Lunghezza ultimo broadcast per evitare duplicati
        start_time = time.time()     # Timestamp inizio esecuzione
        task_interrupted = False     # Flag per interruzione task
        last_credit_check = start_time  # Ultimo controllo crediti
        
        # Loop principale: continua finché il processo è attivo e non interrotto
        while process.poll() is None and not task_interrupted:
            # 1. LEGGE L'OUTPUT DEL PROCESSO (non bloccante)
            stdout, stderr = self._read_process_output(
                process, stdout, stderr
            )
            
            # 2. CONTROLLA SE C'È NUOVO OUTPUT DA INVIARE AL CLIENT
            if (len(stdout) > last_broadcast_stdout_len) or (len(stderr) > last_broadcast_stderr_len):
                try:
                    # 2a. CONTROLLO DIMENSIONE MASSIMA OUTPUT (protezione memoria)
                    if len(stdout) > settings.MAX_OUTPUT_BUFFER_SIZE or len(stderr) > settings.MAX_OUTPUT_BUFFER_SIZE:
                        # Tronca l'output se supera la dimensione massima
                        if len(stdout) > settings.MAX_OUTPUT_BUFFER_SIZE:
                            stdout = stdout[:settings.MAX_OUTPUT_BUFFER_SIZE] + "\n... [Output troncato per dimensione massima]"
                        if len(stderr) > settings.MAX_OUTPUT_BUFFER_SIZE:
                            stderr = stderr[:settings.MAX_OUTPUT_BUFFER_SIZE] + "\n... [Output troncato per dimensione massima]"
                        
                        # TERMINA IL PROCESSO se l'output è troppo grande
                        self._terminate_process(process)
                        task.fail(
                            stdout=stdout.strip(), 
                            stderr=f"{stderr.strip()}Task terminato per output troppo grande (max {settings.MAX_OUTPUT_BUFFER_SIZE} caratteri)",
                            message=f"Task terminato per output troppo grande (max {settings.MAX_OUTPUT_BUFFER_SIZE} caratteri)"
                            
                        )
                        self._ws_broadcast(task)
                        task_interrupted = True
                        
                        # PULIZIA: rimuove file temporaneo e avvia prossimo task
                        self._cleanup_temp_file(tmp_path)
                        self._start_next_pending_task()
                        break
                    
                    # 2b. AGGIORNA IL TASK CON L'OUTPUT E INVIALO AL CLIENT
                    task.stdout = stdout
                    task.stderr = stderr
                    task.save(update_fields=["stdout", "stderr"])
                    self._ws_broadcast(task)
                except Exception:
                    # Non interrompere il loop in caso di errori di I/O/WS
                    pass
                # Aggiorna le lunghezze per evitare duplicati
                last_broadcast_stdout_len = len(stdout)
                last_broadcast_stderr_len = len(stderr)
            
            # 3. CONTROLLI DI SICUREZZA E TIMEOUT
            current_time = time.time()
            elapsed_seconds = current_time - start_time
            
            # 3a. CONTROLLO TIMEOUT MASSIMO (evita processi infiniti)
            if elapsed_seconds >= settings.MAX_TASK_EXECUTION_TIME:
                # TERMINA IL PROCESSO per timeout
                self._terminate_process(process)
                stdout, stderr = self._get_remaining_output(
                    process, stdout, stderr
                )
                task.fail(
                    stdout=stdout.strip(), 
                    stderr=f"{stderr.strip()}Task terminato per timeout massimo ({settings.MAX_TASK_EXECUTION_TIME}s)",
                    message=f"Task terminato per timeout massimo ({settings.MAX_TASK_EXECUTION_TIME}s)"
                )
                self._ws_broadcast(task)
                task_interrupted = True
                
                # PULIZIA: rimuove file temporaneo e avvia prossimo task
                self._cleanup_temp_file(tmp_path)
                self._start_next_pending_task()
                break
            
            
            # 4. CONTROLLO CREDITI OGNI SECONDO (sistema di pagamento)
            if current_time - last_credit_check >= settings.REDUCE_CREDITS_TIME_AMOUNT:
                # Aggiorna i dati utente dal database
                task.user.refresh_from_db()
                
                # Controlla se l'utente ha ancora crediti e li riduce se necessario
                task_interrupted = self._handle_credits_deduction(task, elapsed_seconds, process)
                
                if task_interrupted:  # Se l'utente non ha più crediti
                    # Cattura l'output rimanente dal processo prima di terminarlo
                    stdout, stderr = self._get_remaining_output(
                        process, stdout, stderr
                    )
                    
                    # Segna il task come interrotto per crediti esauriti
                    task.interrupt(
                        stdout=stdout.strip(), 
                        stderr=stderr.strip(),
                        message="Crediti esauriti."
                    )
                    self._ws_broadcast(task)
                    self._cleanup_temp_file(tmp_path)
                    self._start_next_pending_task()
                
                last_credit_check = current_time
            time.sleep(0.01)  # 10ms di pausa
        
        # 6. RESTITUISCE I RISULTATI DEL MONITORAGGIO
        return {
            'stdout': stdout,      # Output completo del programma
            'stderr': stderr,      # Errori completi del programma
            'interrupted': task_interrupted,   # Se il task è stato interrotto
            'start_time': start_time,          # Timestamp di inizio
            'tmp_path': tmp_path               # Percorso del file temporaneo
        }
    
    ### Legge l'output del processo in modo non bloccante ###
    def _read_process_output(self, process: subprocess.Popen, stdout: str, stderr: str) -> tuple:
        try:
            # Drena tutte le linee disponibili su stdout
            while True:
                rlist, _, _ = select.select([process.stdout], [], [], 0)
                if not rlist:
                    break
                line = process.stdout.readline()
                if not line:
                    break
                stdout += line

            # Drena tutte le linee disponibili su stderr
            while True:
                rlist, _, _ = select.select([process.stderr], [], [], 0)
                if not rlist:
                    break
                line = process.stderr.readline()
                if not line:
                    break
                stderr += line

        except Exception:
            pass
        return stdout, stderr
    
    ### Gestisce la deduzione dei crediti e l'interruzione se necessario ###
    def _handle_credits_deduction(self, task: Task, elapsed_seconds: float, process: subprocess.Popen) -> bool:
        credits_needed = int(elapsed_seconds * settings.DEFAULT_CREDIT_COST_PER_TIME_AMOUNT)
    
        # Controlla se l'utente ha abbastanza crediti per continuare
        if task.user.credits >= credits_needed - task.credits_cost:
            credits_to_deduct = credits_needed - task.credits_cost
            if credits_to_deduct > 0:
                task.user.reduce_credits(credits_to_deduct)
                task.credits_cost = credits_needed
                task.save()
                self._ws_broadcast(task)
            return False
        else:
            self._terminate_process(process)
            return True
    
    ### Termina il processo in modo sicuro ###
    def _terminate_process(self, process: subprocess.Popen) -> None:
        process.terminate()
        try:
            process.wait(timeout=min(0.5, settings.PROGRAM_EXECUTION_TIMEOUT))
        except subprocess.TimeoutExpired:
            process.kill()
    
    ### Ottiene l'output rimanente dal processo terminato ###
    def _get_remaining_output(self, process: subprocess.Popen, stdout: str, stderr: str) -> tuple:
        try:
            remaining_stdout, remaining_stderr = process.communicate(timeout=min(0.5, settings.PROGRAM_EXECUTION_TIMEOUT))
            stdout += remaining_stdout
            stderr += remaining_stderr
        except subprocess.TimeoutExpired:
            pass
        return stdout, stderr
    
    ### Finalizza il task con l'output completo ###
    def _finalize_task(self, task: Task, process: subprocess.Popen, output_data: Dict[str, Any]) -> None:
        
        # Ottiene l'output rimanente dal processo terminato
        remaining_stdout, remaining_stderr = process.communicate()
        final_stdout = output_data['stdout'] + remaining_stdout
        final_stderr = output_data['stderr'] + remaining_stderr
        
        # Calcolo tempo di esecuzione e crediti utilizzati
        total_seconds = time.time() - output_data['start_time']
        total_credits_used = int(total_seconds * settings.DEFAULT_CREDIT_COST_PER_TIME_AMOUNT)
        
        # Deduzione crediti se necessario
        if total_credits_used > task.credits_cost:
            remaining_credits = total_credits_used - task.credits_cost
            task.user.reduce_credits(remaining_credits)
            task.credits_cost = total_credits_used
            task.save()
        
        if process.returncode == 0:
            task.complete(stdout=final_stdout.strip(), stderr=final_stderr.strip())
        else:
            task.fail(stdout=final_stdout.strip(), stderr=final_stderr.strip())
        self._ws_broadcast(task)
        
        # Pulisce il file temporaneo
        self._cleanup_temp_file(output_data.get('tmp_path'))
        
        # Avvia il prossimo task in coda se disponibile
        self._start_next_pending_task()
    
    ### Pulisce il file temporaneo ###
    def _cleanup_temp_file(self, tmp_path: Optional[str]) -> None:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
    
    ### Avvia il prossimo task in coda se disponibile ###
    def _start_next_pending_task(self) -> None:
        if Task.can_start_new_task():
            next_task = Task.get_next_pending_task()
            if next_task:
                self._start_task_execution(next_task)

    ### Invia aggiornamenti Task attraverso WebSocket ###
    def _ws_broadcast(self, task: Task) -> None:
        try:
            channel_layer = get_channel_layer()
            if not channel_layer:
                return
            data = TaskSerializer(task).data
            async_to_sync(channel_layer.group_send)(
                f'task_{task.id}',
                { 'type': 'task_update', 'data': data }
            )
        except Exception:
            # Ignora errori WebSocket
            pass
