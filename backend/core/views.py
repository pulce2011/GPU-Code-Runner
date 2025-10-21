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
# AUTHENTICATION & USER MANAGEMENT
# =============================================================================

### Informazioni utente corrente ###
class UserInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


### Registrazione utente ###
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
# COURSE & EXERCISE MANAGEMENT
# =============================================================================

### Lista corsi ###
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


### Lista esercizi filtrati per corso utente loggato ###
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
# CODE EXECUTION & TASK MANAGEMENT
# =============================================================================

### Esecuzione codice con sistema crediti ###
class RunExerciseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    
    # Valida i dati della richiesta
    def _validate_request(self, request) -> Optional[Response]:
        if not request.data.get('code'):
            return self._error_response('code is required', status.HTTP_400_BAD_REQUEST)
        
        if not request.data.get('exercise_id'):
            return self._error_response('exercise_id is required', status.HTTP_400_BAD_REQUEST)
        
        # Controllo lunghezza massima del codice sorgente
        code = request.data.get('code', '')
        if len(code) > settings.MAX_SOURCE_CODE_LENGTH:
            return self._error_response(
                f'Codice troppo lungo. Massimo {settings.MAX_SOURCE_CODE_LENGTH} caratteri, forniti {len(code)}', 
                status.HTTP_400_BAD_REQUEST
            )
        
        return None
    
    # Crea una risposta di errore standardizzata
    def _error_response(self, message: str, status_code: int) -> Response:
        return Response({'error': message}, status=status_code)
    
    # Crea un nuovo task
    def _create_task(self, user: User, exercise: Exercise, code: str) -> Task:
        task = Task.objects.create(
            user=user,
            exercise=exercise,
            code=code,
            credits_cost=settings.TASK_START_COST,
        )
        task.pending()
        return task
    
    # Avvia l'esecuzione del task in background
    def _start_task_execution(self, task: Task) -> None:
        thread = threading.Thread(target=self._execute_task, args=(task,))
        thread.daemon = True
        thread.start()

    # Esecuzione del task in background con controllo crediti
    def _execute_task(self, task: Task) -> None:
        tmp_path = None
        try:
            task.start()
            self._ws_broadcast(task)
            tmp_path = self._create_temp_file(task.code, task.exercise)
            process = self._start_process(tmp_path, task.exercise)
            
            task.process_id = process.pid
            task.save()
            self._ws_broadcast(task)

            output_data = self._monitor_process(process, task)
            
            if not output_data['interrupted']:
                self._finalize_task(task, process, output_data)
            
        except Exception as e:
            task.fail(stdout='', stderr=f'Errore durante l\'esecuzione: {str(e)}')
            self._ws_broadcast(task)
        finally:
            self._cleanup_temp_file(tmp_path)
    
    # Crea un file temporaneo con il codice
    def _create_temp_file(self, code: str, exercise: Exercise) -> str:
        # Directory: ./gpu/<exercise.name>
        safe_name = ''.join(ch for ch in exercise.name if ch.isalnum() or ch in ('-', '_')) or 'exercise'
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gpu', safe_name))
        os.makedirs(base_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=exercise.file_extension,
            prefix='code_',
            delete=False,
            dir=base_dir
        ) as f:
            f.write(code)
            return f.name
    
    # Avvia il processo di esecuzione
    def _start_process(self, tmp_path: str, exercise: Exercise) -> subprocess.Popen:
        
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'run_exercise.sh'))
        
        if shutil.which('stdbuf'):
            cmd = ['stdbuf', '-oL', '-eL', 'bash', script_path, tmp_path]
        else:
            cmd = ['bash', script_path, tmp_path]

        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    
    # Monitora il processo e gestisce i crediti
    def _monitor_process(self, process: subprocess.Popen, task: Task) -> Dict[str, Any]:
        accumulated_stdout = ""
        accumulated_stderr = ""
        last_broadcast_stdout_len = 0
        last_broadcast_stderr_len = 0
        start_time = time.time()
        task_interrupted = False
        last_credit_check = start_time
        
        while process.poll() is None and not task_interrupted:
            # Polling non bloccante per output istantaneo
            accumulated_stdout, accumulated_stderr = self._read_process_output(
                process, accumulated_stdout, accumulated_stderr
            )
            
            # Se c'è nuovo output, aggiorna il task e invia un broadcast per lo streaming realtime
            if (len(accumulated_stdout) > last_broadcast_stdout_len) or (len(accumulated_stderr) > last_broadcast_stderr_len):
                try:
                    # Controllo dimensione massima output
                    if len(accumulated_stdout) > settings.MAX_OUTPUT_BUFFER_SIZE or len(accumulated_stderr) > settings.MAX_OUTPUT_BUFFER_SIZE:
                        # Tronca l'output se supera la dimensione massima
                        if len(accumulated_stdout) > settings.MAX_OUTPUT_BUFFER_SIZE:
                            accumulated_stdout = accumulated_stdout[:settings.MAX_OUTPUT_BUFFER_SIZE] + "\n... [Output troncato per dimensione massima]"
                        if len(accumulated_stderr) > settings.MAX_OUTPUT_BUFFER_SIZE:
                            accumulated_stderr = accumulated_stderr[:settings.MAX_OUTPUT_BUFFER_SIZE] + "\n... [Output troncato per dimensione massima]"
                        # Termina il processo se l'output è troppo grande
                        self._terminate_process(process)
                        task.fail(
                            stdout=accumulated_stdout.strip(), 
                            stderr=f"{accumulated_stderr.strip()}Task terminato per output troppo grande (max {settings.MAX_OUTPUT_BUFFER_SIZE} caratteri)"
                        )
                        self._ws_broadcast(task)
                        task_interrupted = True
                        
                        # Avvia il prossimo task in coda se disponibile
                        self._start_next_pending_task()
                        break
                    
                    task.stdout = accumulated_stdout
                    task.stderr = accumulated_stderr
                    # Non cambiamo lo status qui: resta 'running'
                    task.save(update_fields=["stdout", "stderr"])  # riduce scritture inutili
                    self._ws_broadcast(task)
                except Exception:
                    # Non interrompere il loop in caso di errori di I/O/WS
                    pass
                last_broadcast_stdout_len = len(accumulated_stdout)
                last_broadcast_stderr_len = len(accumulated_stderr)
            
            # Controllo crediti ogni secondo (senza sleep bloccante)
            current_time = time.time()
            # Controllo timeout massimo di esecuzione
            elapsed_seconds = current_time - start_time
            if elapsed_seconds >= settings.MAX_TASK_EXECUTION_TIME:
                self._terminate_process(process)
                accumulated_stdout, accumulated_stderr = self._get_remaining_output(
                    process, accumulated_stdout, accumulated_stderr
                )
                task.fail(
                    stdout=accumulated_stdout.strip(), 
                    stderr=f"{accumulated_stderr.strip()}Task terminato per timeout massimo ({settings.MAX_TASK_EXECUTION_TIME}s)"
                )
                self._ws_broadcast(task)
                task_interrupted = True
                
                # Avvia il prossimo task in coda se disponibile
                self._start_next_pending_task()
                break
            
            if current_time - last_credit_check >= 1.0:
                task.user.refresh_from_db()
                task_interrupted = self._handle_credits_deduction(task, elapsed_seconds, process)
                if task_interrupted:
                    accumulated_stdout, accumulated_stderr = self._get_remaining_output(
                        process, accumulated_stdout, accumulated_stderr
                    )
                    task.interrupt(
                        stdout=accumulated_stdout.strip(), 
                        stderr=accumulated_stderr.strip()
                    )
                    self._ws_broadcast(task)
                    
                    # Avvia il prossimo task in coda se disponibile
                    self._start_next_pending_task()
                last_credit_check = current_time
            
            time.sleep(0.01)
        return {
            'stdout': accumulated_stdout,
            'stderr': accumulated_stderr,
            'interrupted': task_interrupted,
            'start_time': start_time
        }
    
    # Legge l'output del processo in modo non bloccante
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
    
    # Gestisce la deduzione dei crediti e l'interruzione se necessario
    def _handle_credits_deduction(self, task: Task, elapsed_seconds: float, process: subprocess.Popen) -> bool:
        credits_needed = int(elapsed_seconds * settings.DEFAULT_CREDIT_COST_PER_SECOND)
        
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
    
    # Termina il processo in modo sicuro
    def _terminate_process(self, process: subprocess.Popen) -> None:
        process.terminate()
        try:
            process.wait(timeout=min(0.5, settings.PROGRAM_EXECUTION_TIMEOUT))
        except subprocess.TimeoutExpired:
            process.kill()
    
    # Ottiene l'output rimanente dal processo terminato
    def _get_remaining_output(self, process: subprocess.Popen, stdout: str, stderr: str) -> tuple:
        try:
            remaining_stdout, remaining_stderr = process.communicate(timeout=min(0.5, settings.PROGRAM_EXECUTION_TIMEOUT))
            stdout += remaining_stdout
            stderr += remaining_stderr
        except subprocess.TimeoutExpired:
            pass
        return stdout, stderr
    
    # Finalizza il task con l'output completo
    def _finalize_task(self, task: Task, process: subprocess.Popen, output_data: Dict[str, Any]) -> None:
        
        # Ottiene l'output rimanente dal processo terminato
        remaining_stdout, remaining_stderr = process.communicate()
        final_stdout = output_data['stdout'] + remaining_stdout
        final_stderr = output_data['stderr'] + remaining_stderr
        
        # Calcolo tempo di esecuzione e crediti utilizzati
        total_seconds = time.time() - output_data['start_time']
        total_credits_used = int(total_seconds * settings.DEFAULT_CREDIT_COST_PER_SECOND)
        
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
        
        # Avvia il prossimo task in coda se disponibile
        self._start_next_pending_task()
    
    # Pulisce il file temporaneo
    def _cleanup_temp_file(self, tmp_path: Optional[str]) -> None:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
    
    # Avvia il prossimo task in coda se disponibile
    def _start_next_pending_task(self) -> None:
        """Avvia il prossimo task in coda se c'è spazio disponibile"""
        if Task.can_start_new_task():
            next_task = Task.get_next_pending_task()
            if next_task:
                self._start_task_execution(next_task)

    # =============================
    # WebSocket helpers
    # =============================
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
            # Evita che errori WS interrompano l'esecuzione
            pass

# =============================================================================
# TASK QUERY & RETRIEVAL
# =============================================================================

### Lista task dell'utente ###
class TaskListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:10]
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


### Dettagli di un task specifico ###
class TaskDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id: int) -> Response:
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({'error': 'Task non trovato'}, status=status.HTTP_404_NOT_FOUND)
