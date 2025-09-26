from django.contrib import admin
from .models import Course, User, Exercise, Task


# Configurazione admin per gestire i corsi universitari
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


# Configurazione admin per gestire gli utenti con email e matricola
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'matr', 'first_name', 'last_name', 'course']
    list_filter = ['course', 'is_active', 'is_staff']
    search_fields = ['email', 'matr', 'first_name', 'last_name']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'matr', 'course')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


# Configurazione admin per gestire esercizi di programmazione con parametri JSON
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'return_type', 'get_courses']
    list_filter = ['return_type', 'courses']
    search_fields = ['name', 'comment']
    filter_horizontal = ['courses']
    
    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])
    get_courses.short_description = 'Courses'


# Configurazione admin per gestire i task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user__matr', 'exercise__name', 'status', 'created_at', 'started_at', 'finished_at']
    list_filter = ['status', 'created_at', 'started_at', 'finished_at', 'user__course', 'user__matr']
    search_fields = ['user__email', 'user__matr', 'user__first_name', 'user__last_name', 'exercise__name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'started_at', 'finished_at', 'total_execution_time', 'stdout', 'stderr', 'process_id', 'credits_cost']
    fieldsets = (
        ('Info', {'fields': ('id', 'user', 'exercise', 'status')}),
        ('Output', {'fields': ('stdout', 'stderr')}),
        ('Timestamps', {'fields': ('created_at', 'started_at', 'finished_at', 'total_execution_time')}),
    )
