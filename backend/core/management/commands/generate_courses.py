from django.core.management.base import BaseCommand
from core.models import Course

class Command(BaseCommand):
    help = 'Genera corsi di studio di esempio'

    def handle(self, *args, **kwargs):
        courses = [
            'Informatica',
            'Matematica', 
            'Fisica',
            'Ingegneria Informatica',
            'Ingegneria Elettronica',
            'Ingegneria Meccanica',
            'Biologia',
            'Chimica',
            'Medicina',
            'Economia',
            'Giurisprudenza',
            'Psicologia',
            'Lettere',
            'Filosofia',
            'Storia',
            'Geografia',
            'Scienze Politiche',
            'Architettura',
            'Design',
            'Lingue e Letterature Straniere'
        ]

        created_count = 0
        for name in courses:
            obj, created = Course.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Creato corso: {name}'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Corso già esistente: {name}'))

        self.stdout.write(self.style.SUCCESS(f'Generazione corsi completata! Creati {created_count} nuovi corsi.'))
