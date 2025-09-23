import tempfile
import subprocess
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Exercise, Course, User
from .serializers import ExerciseSerializer, UserSerializer, CourseSerializer



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
        if user.course:
            return Exercise.objects.filter(courses=user.course)
        return Exercise.objects.none()


# Esecuzione codice
class RunExerciseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'body is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Salva codice su file temporaneo
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                tmp_path = f.name

            # Esegui script bash simulato
            result = subprocess.run(
                ['bash', 'simulate_gpu.sh', tmp_path],
                capture_output=True, text=True
            )

            return Response({
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip()
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
