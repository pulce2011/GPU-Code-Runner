import tempfile
import subprocess
import threading
import time
import os
import select
from typing import Dict, Any, Optional
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Exercise, Course, User, Task
from .serializers import ExerciseSerializer, UserSerializer, CourseSerializer, TaskSerializer

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
        user = serializer.save()
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
        if not user.has_credits():
            return self._error_response('Crediti insufficienti.', status.HTTP_402_PAYMENT_REQUIRED)

        # Recupero esercizio
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            
            # Deduce 1 credito per avviare il task
            if not user.reduce_credits(1):
                return self._error_response('Crediti insufficienti.', status.HTTP_402_PAYMENT_REQUIRED)
            
            # Crea il task e lo avvia in background
            task = self._create_task(user, exercise, code)
            self._start_task_execution(task)

            return Response({
                'task_id': task.id,
                'status': task.status,
                'message': 'Lavoro avviato con successo'
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
            credits_cost=1,
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
            tmp_path = self._create_temp_file(task.code, task.exercise)
            process = self._start_process(tmp_path)
            
            task.process_id = process.pid
            task.save()

            output_data = self._monitor_process(process, task)
            
            if not output_data['interrupted']:
                self._finalize_task(task, process, output_data)
            
        except Exception as e:
            task.fail(stdout='', stderr=f'Errore durante l\'esecuzione: {str(e)}')
        finally:
            self._cleanup_temp_file(tmp_path)
    
    # Crea un file temporaneo con il codice
    def _create_temp_file(self, code: str, exercise: Exercise) -> str:
        with tempfile.NamedTemporaryFile(mode='w', suffix=exercise.file_extension, delete=False, dir=".") as f:
            f.write(code)
            return f.name
    
    # Avvia il processo di esecuzione
    def _start_process(self, tmp_path: str) -> subprocess.Popen:
        return subprocess.Popen(
            ['bash', 'simulate_gpu.sh', tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    
    # Monitora il processo e gestisce i crediti
    def _monitor_process(self, process: subprocess.Popen, task: Task) -> Dict[str, Any]:
        accumulated_stdout = ""
        accumulated_stderr = ""
        start_time = time.time()
        task_interrupted = False
        
        while process.poll() is None and not task_interrupted:
            time.sleep(1)
            task.user.refresh_from_db()
            
            accumulated_stdout, accumulated_stderr = self._read_process_output(
                process, accumulated_stdout, accumulated_stderr
            )
            
            elapsed_seconds = time.time() - start_time
            if elapsed_seconds >= 1.0:
                task_interrupted = self._handle_credits_deduction(task, elapsed_seconds, process)
                if task_interrupted:
                    accumulated_stdout, accumulated_stderr = self._get_remaining_output(
                        process, accumulated_stdout, accumulated_stderr
                    )
                    task.interrupt(
                        stdout=accumulated_stdout.strip(), 
                        stderr=accumulated_stderr.strip()
                    )
        
        return {
            'stdout': accumulated_stdout,
            'stderr': accumulated_stderr,
            'interrupted': task_interrupted,
            'start_time': start_time
        }
    
    # Legge l'output del processo in modo non bloccante
    def _read_process_output(self, process: subprocess.Popen, stdout: str, stderr: str) -> tuple:
        try:
            if select.select([process.stdout], [], [], 0)[0]:
                line = process.stdout.readline()
                if line:
                    stdout += line
            if select.select([process.stderr], [], [], 0)[0]:
                line = process.stderr.readline()
                if line:
                    stderr += line
        except:
            pass
        return stdout, stderr
    
    # Gestisce la deduzione dei crediti e l'interruzione se necessario
    def _handle_credits_deduction(self, task: Task, elapsed_seconds: float, process: subprocess.Popen) -> bool:
        credits_needed = int(elapsed_seconds)
        
        if task.user.credits >= credits_needed - task.credits_cost:
            credits_to_deduct = credits_needed - task.credits_cost
            if credits_to_deduct > 0:
                task.user.reduce_credits(credits_to_deduct)
                task.credits_cost = credits_needed
                task.save()
            return False
        else:
            self._terminate_process(process)
            return True
    
    # Termina il processo in modo sicuro
    def _terminate_process(self, process: subprocess.Popen) -> None:
        process.terminate()
        try:
            process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            process.kill()
    
    # Ottiene l'output rimanente dal processo terminato
    def _get_remaining_output(self, process: subprocess.Popen, stdout: str, stderr: str) -> tuple:
        try:
            remaining_stdout, remaining_stderr = process.communicate(timeout=0.5)
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
        total_credits_used = int(total_seconds)
        
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
    
    # Pulisce il file temporaneo
    def _cleanup_temp_file(self, tmp_path: Optional[str]) -> None:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except:
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
