from django.contrib import admin
from .models import Course, User, Exercise, Task


# Configurazione admin per gestire i corsi universitari
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


# Configurazione admin per gestire gli utenti con email e matricola
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'matr', 'first_name', 'last_name', 'course', 'credits', 'is_active']
    list_filter = ['course', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'matr', 'first_name', 'last_name']
    ordering = ['email']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'matr', 'course', 'credits')}),
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
    ordering = ['name']
    
    def get_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])
    get_courses.short_description = 'Courses'


# Configurazione admin per gestire i task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user_matr', 'get_exercise_name', 'status', 'credits_cost', 'get_execution_time', 'created_at']
    list_filter = ['status', 'created_at', 'user__course', 'exercise']
    search_fields = ['user__email', 'user__matr', 'user__first_name', 'user__last_name', 'exercise__name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'started_at', 'finished_at', 'total_execution_time', 'stdout', 'stderr', 'process_id', 'credits_cost']
    
    fieldsets = (
        ('Info', {'fields': ('id', 'user', 'exercise', 'status', 'credits_cost')}),
        ('Output', {'fields': ('stdout', 'stderr', 'message')}),
        ('Timestamps', {'fields': ('created_at', 'started_at', 'finished_at', 'total_execution_time')}),
    )
    
    def get_user_matr(self, obj):
        return obj.user.matr
    get_user_matr.short_description = 'Matricola'
    get_user_matr.admin_order_field = 'user__matr'
    
    def get_exercise_name(self, obj):
        return obj.exercise.name
    get_exercise_name.short_description = 'Exercise'
    get_exercise_name.admin_order_field = 'exercise__name'
    
    def get_execution_time(self, obj):
        if obj.total_execution_time:
            return str(obj.total_execution_time)
        return '-'
    get_execution_time.short_description = 'Execution Time'
    get_execution_time.admin_order_field = 'total_execution_time'
