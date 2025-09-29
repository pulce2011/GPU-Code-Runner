import tempfile
import subprocess
import threading
import time
import os
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Exercise, Course, User, Task
from .serializers import ExerciseSerializer, UserSerializer, CourseSerializer, TaskSerializer


# =============================================================================
# AUTHENTICATION & USER MANAGEMENT
# =============================================================================

# Informazioni utente corrente
class UserInfoView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Registrazione utente
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# =============================================================================
# COURSE & EXERCISE MANAGEMENT
# =============================================================================

# Lista corsi
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


# Lista esercizi filtrati per corso utente loggato
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

# Esecuzione codice con sistema crediti
class RunExerciseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        exercise_id = request.data.get('exercise_id')
        user = request.user
        
        if not code:
            return Response({'error': 'code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not exercise_id:
            return Response({'error': 'exercise_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.has_credits():
            return Response({'error': 'Crediti insufficienti.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

        try:
            exercise = Exercise.objects.get(id=exercise_id)
            
            if not user.reduce_credits(1):
                return Response({'error': 'Crediti insufficienti.'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            
            task = Task.objects.create(
                user=user,
                exercise=exercise,
                code=code,
                credits_cost=1,
            )
            
            task.pending()
            
            thread = threading.Thread(target=self._execute_task, args=(task,))
            thread.daemon = True
            thread.start()

            return Response({
                'task_id': task.id,
                'status': task.status,
                'message': 'Lavoro avviato con successo'
            })
            
        except Exercise.DoesNotExist:
            return Response({'error': 'Esercizio non trovato'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _execute_task(self, task):
        try:
            task.start()

            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(task.code)
                tmp_path = f.name

            process = subprocess.Popen(
                ['bash', 'simulate_gpu.sh', tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            accumulated_stdout = ""
            accumulated_stderr = ""
            
            task.process_id = process.pid
            task.save()

            start_time = time.time()
            task_interrupted = False
            
            while process.poll() is None and not task_interrupted:
                time.sleep(1)
                task.user.refresh_from_db()
                
                try:
                    import select
                    if select.select([process.stdout], [], [], 0)[0]:
                        line = process.stdout.readline()
                        if line:
                            accumulated_stdout += line
                    if select.select([process.stderr], [], [], 0)[0]:
                        line = process.stderr.readline()
                        if line:
                            accumulated_stderr += line
                except:
                    pass
                
                current_time = time.time()
                elapsed_seconds = current_time - start_time
                
                if elapsed_seconds >= 1.0:
                    credits_needed = int(elapsed_seconds)
                    if task.user.credits >= credits_needed - task.credits_cost:
                        credits_to_deduct = credits_needed - task.credits_cost
                        if credits_to_deduct > 0:
                            task.user.reduce_credits(credits_to_deduct)
                            task.credits_cost = credits_needed
                            task.save()
                    else:
                        process.terminate()
                        try:
                            process.wait(timeout=0.5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                        
                        try:
                            remaining_stdout, remaining_stderr = process.communicate(timeout=0.5)
                            accumulated_stdout += remaining_stdout
                            accumulated_stderr += remaining_stderr
                        except subprocess.TimeoutExpired:
                            pass
                        
                        task.interrupt(stdout=accumulated_stdout.strip(), stderr=accumulated_stderr.strip())
                        task_interrupted = True
                        break

            if task_interrupted:
                return
            
            remaining_stdout, remaining_stderr = process.communicate()
            accumulated_stdout += remaining_stdout
            accumulated_stderr += remaining_stderr
            
            end_time = time.time()
            total_seconds = end_time - start_time
            total_credits_used = int(total_seconds)
            
            if total_credits_used > task.credits_cost:
                remaining_credits = total_credits_used - task.credits_cost
                task.user.reduce_credits(remaining_credits)
                task.credits_cost = total_credits_used
                task.save()
            
            if process.returncode == 0:
                task.complete(stdout=accumulated_stdout.strip(), stderr=accumulated_stderr.strip())
            else:
                task.fail(stdout=accumulated_stdout.strip(), stderr=accumulated_stderr.strip())

            try:
                os.unlink(tmp_path)
            except:
                pass

        except Exception as e:
            task.fail(stdout='', stderr=f'Errore durante l\'esecuzione: {str(e)}')

# =============================================================================
# TASK QUERY & RETRIEVAL
# =============================================================================

# Lista task dell'utente
class TaskListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(user=user).order_by('-created_at')[:10]
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


# Dettagli di un task specifico
class TaskDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({'error': 'Task non trovato'}, status=status.HTTP_404_NOT_FOUND)
