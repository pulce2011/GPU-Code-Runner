from django.core.management.base import BaseCommand
from core.models import Course

class Command(BaseCommand):
    help = 'Genera corsi di studio di esempio'

    def handle(self, *args, **kwargs):
        courses = ['Informatica', 'Matematica', 'Fisica', 'Ingegneria', 'Biologia']

        for name in courses:
            obj, created = Course.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Creato corso: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Corso già esistente: {name}'))

        self.stdout.write(self.style.SUCCESS('Generazione corsi completata!'))
