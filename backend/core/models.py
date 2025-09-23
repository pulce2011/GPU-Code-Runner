from django.db import models
from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)  # Make email unique since it's USERNAME_FIELD
    matr = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['matr', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matr})"


class Exercise(models.Model):
    name = models.CharField(max_length=200)          # Nome funzione
    return_type = models.CharField(max_length=50)    # Tipo di ritorno
    params = models.JSONField(default=list, blank=True)
    comment = models.TextField(blank=True)           # Commento/consegna
    courses = models.ManyToManyField(Course, related_name='exercises')

    def __str__(self):
        return self.name

    def build_signature(self):
        # Commento multi-linea
        comment_block = f"/*\n{self.comment}\n*/" if self.comment else ""

        # Parametri
        param_list = ', '.join([f"{p['type']} {p['name']}" for p in self.params])

        # Firma funzione
        signature_line = f"{self.return_type} {self.name}({param_list})"
        
        # Combina tutto
        if comment_block:
            return f"{comment_block}\n{signature_line}"
        else:
            return signature_line
