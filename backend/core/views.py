import tempfile
import subprocess
import threading
import time
import os
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Exercise, Course, User, Task
from .serializers import ExerciseSerializer, UserSerializer, CourseSerializer, TaskSerializer



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

        # opzionale: puoi anche generare qui JWT se vuoi login automatico
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Lista corsi
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]  # accessibile anche senza login


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

        # Controllo crediti prima dell'esecuzione
        if not user.has_credits():
            return Response({
                'error': 'Crediti insufficienti per eseguire il lavoro',
                'credits_available': user.credits
            }, status=status.HTTP_402_PAYMENT_REQUIRED)

        try:
            # Ottieni l'esercizio
            exercise = Exercise.objects.get(id=exercise_id)
            
            # Crea un nuovo task
            task = Task.objects.create(
                user=user,
                exercise=exercise,
                code=code,
                credits_cost=1,
            )
            
            #Segna il task come in attesa
            task.pending()

            # Avvia il task in un thread separato
            thread = threading.Thread(target=self._execute_task, args=(task,))
            thread.daemon = True
            thread.start()

            return Response({
                'task_id': task.id,
                'status': task.status,
                'message': 'Lavoro avviato con successo',
                'credits_remaining': user.credits - 1
            })
            
        except Exercise.DoesNotExist:
            return Response({'error': 'Esercizio non trovato'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _execute_task(self, task):
        """Esegue il task in background con controllo crediti"""
        try:
            # Sottrae i crediti all'inizio
            if not task.user.reduce_credits(task.credits_cost):
                task.fail('Crediti insufficienti')
                return

            #Avvia il task
            task.start()

            # Salva codice su file temporaneo
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(task.code)
                tmp_path = f.name

            # Avvia processo con Popen per controllo asincrono
            process = subprocess.Popen(
                ['bash', 'simulate_gpu.sh', tmp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            #Salva l'ID del processo (PID)
            task.process_id = process.pid
            task.save()

            # Loop di controllo crediti durante l'esecuzione
            while process.poll() is None:
                time.sleep(1)
                task.user.refresh_from_db()
                
                if task.user.credits <= 0:
                    process.terminate()
                    task.interrupt()
                    return
                
                if task.user.credits > 0:
                    task.user.reduce_credits(1)

            # Se arriva qui, il processo è terminato normalmente
            stdout, stderr = process.communicate()
            
            # Controlla se è stato interrotto o completato
            if process.returncode == 0:
                task.complete(stdout=stdout.strip(), stderr=stderr.strip())
            else:
                task.fail(stderr=stderr.strip())

            # Pulisci il file temporaneo
            try:
                os.unlink(tmp_path)
            except:
                pass

        except Exception as e:
            task.fail(f'Errore durante l\'esecuzione: {str(e)}')


### Commentati per ora per evitare di aggiungere troppe API

# Lista task dell'utente
# class TaskListView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
# 
#     def get(self, request):
#         user = request.user
#         tasks = Task.objects.filter(user=user).order_by('-created_at')[:10]
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)


# Dettagli di un task specifico
# class TaskDetailView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
# 
#     def get(self, request, task_id):
#         try:
#             task = Task.objects.get(id=task_id, user=request.user)
#             serializer = TaskSerializer(task)
#             return Response(serializer.data)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task non trovato'}, status=status.HTTP_404_NOT_FOUND)
