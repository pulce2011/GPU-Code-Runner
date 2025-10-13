from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


### Manager personalizzato per creare utenti con email e matricola invece di username ###
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


### Modello per rappresentare un corso universitario ###
class Course(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


### Modello utente personalizzato con email come login e matricola unica ###
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
    
    # Verifica se l'utente ha abbastanza crediti
    def has_credits(self, amount=1):
        if self.is_superuser or self.is_staff:
            return True
        return self.credits >= amount
    
    # Riduce i crediti dell'utente
    def reduce_credits(self, amount=1):
        if self.is_superuser or self.is_staff:
            return True
        if self.has_credits(amount):
            self.credits -= amount
            self.save()
            return True
        return False


### Modello per esercizi di programmazione con parametri JSON e firma funzione ###
class Exercise(models.Model):
    name = models.CharField(max_length=200)          # Nome funzione
    return_type = models.CharField(max_length=50)    # Tipo di ritorno
    params = models.JSONField(default=list, blank=True)
    comment = models.TextField(blank=True)           # Commento/consegna
    courses = models.ManyToManyField(Course, related_name='exercises')

    def __str__(self):
        return self.name

    # Costruisce la firma della funzione con commenti e parametri
    def build_signature(self):
        comment_block = f"/*\n{self.comment}\n*/" if self.comment else ""
        param_list = ', '.join([f"{p['type']} {p['name']}" for p in self.params])
        signature_line = f"{self.return_type} {self.name}({param_list})"
        
        if comment_block:
            return f"{comment_block}\n\n{signature_line} {'{'}\n\n{'}'}\n"
        else:
            return signature_line


### Modello per rappresentare un task (Richiesta di esecuzione di un esercizio) ###  
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'In attesa'),
        ('running', 'In esecuzione'),
        ('completed', 'Completato'),
        ('failed', 'Fallito'),
        ('interrupted', 'Interrotto'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    code = models.TextField(default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    total_execution_time = models.DurationField(null=True, blank=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    credits_cost = models.IntegerField(default=1)
    process_id = models.IntegerField(null=True, blank=True)
    message = models.TextField(default='', blank=True)

    def __str__(self):
        return f"Task {self.id} - {self.user.matr} - {self.status}"
    
    # Avvia il task
    def start(self):
        self.status = 'running'
        self.started_at = timezone.now()
        self.message = "Task in esecuzione..."
        self.save()

    # Segna il task come in attesa
    def pending(self):
        self.status = 'pending'
        self.message = "Task in attesa di esecuzione..."
        self.save()
    
    # Completa il task con successo
    def complete(self, stdout='', stderr=''):
        self.status = 'completed'
        self.finished_at = timezone.now()
        if self.started_at is not None:
            self.total_execution_time = self.finished_at - self.started_at
        self.stdout = stdout
        self.stderr = stderr
        self.message = "Task completato con successo."
        self.save()
    
    # Segna il task come fallito
    def fail(self, stdout='', stderr=''):
        self.status = 'failed'
        self.finished_at = timezone.now()
        if self.started_at is not None:
            self.total_execution_time = self.finished_at - self.started_at
        self.stdout = stdout
        self.stderr = stderr
        self.message = "Task fallito."
        self.save()
    
    # Interrompe il task per crediti esauriti
    def interrupt(self, stdout='', stderr=''):
        self.status = 'interrupted'
        self.finished_at = timezone.now()
        if self.started_at is not None:
            self.total_execution_time = self.finished_at - self.started_at
        self.stdout = stdout
        self.stderr = stderr
        self.message = "Task interrotto (crediti esauriti)."
        self.save()
