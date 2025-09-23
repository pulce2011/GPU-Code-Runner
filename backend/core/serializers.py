from rest_framework import serializers
from .models import Exercise, User, Course

class ExerciseSerializer(serializers.ModelSerializer):
    signature = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'return_type', 'params', 'comment', 'signature']

    def get_signature(self, obj):
        return obj.build_signature()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'matr', 'first_name', 'last_name', 'course']
