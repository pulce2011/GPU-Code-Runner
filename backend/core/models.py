from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Manager personalizzato per creare utenti con email e matricola invece di username
class UserManager(BaseUserManager):
    def create_user(self, email, matr, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not matr:
            raise ValueError('The Matr field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            matr=matr,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, matr, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, matr, first_name, last_name, password, **extra_fields)


# Modello per rappresentare un corso universitario
class Course(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


# Modello utente personalizzato con email come login e matricola unica
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    matr = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    credits = models.IntegerField(default=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['matr', 'first_name', 'last_name']
    
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matr})"
    
    def has_credits(self, amount=1):
        return self.credits >= amount
    
    def reduce_credits(self, amount=1):
        if self.has_credits(amount):
            self.credits -= amount
            self.save()
            return True
        return False


# Modello per esercizi di programmazione con parametri JSON e firma funzione
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
            return f"{comment_block}\n\n{signature_line} {'{'}\n\n{'}'}\n"
        else:
            return signature_line
