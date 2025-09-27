from rest_framework import serializers
from .models import Exercise, User, Course, Task

# Serializzatore per gli esercizi
class ExerciseSerializer(serializers.ModelSerializer):
    signature = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'return_type', 'params', 'comment', 'signature']

    def get_signature(self, obj):
        return obj.build_signature()


# Serializzatore per i corsi
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']


# Serializzatore per gli utenti
class UserSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'matr', 'first_name', 'last_name', 'course', 'course_name', 'is_superuser', 'credits', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user


# Serializzatore per i task
class TaskSerializer(serializers.ModelSerializer):
    user_matr = serializers.CharField(source='user.matr', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'user_matr', 'user_name', 'exercise', 'exercise_name', 'code', 'status', 
                 'created_at', 'started_at', 'finished_at', 'total_execution_time', 
                 'stdout', 'stderr', 'credits_cost', 'process_id', 'message']
        read_only_fields = ['id', 'user', 'created_at', 'started_at', 'finished_at', 
                            'total_execution_time', 'stdout', 'stderr', 'process_id']
