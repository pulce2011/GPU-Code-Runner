from django.core.management.base import BaseCommand
from core.models import Exercise, Course

class Command(BaseCommand):
    help = 'Genera esercizi di esempio per i corsi'

    def handle(self, *args, **kwargs):
        # Recupera tutti i corsi
        courses = list(Course.objects.all())
        if not courses:
            self.stdout.write(self.style.ERROR('Nessun corso presente!'))
            return

        exercises_data = [
            {
                'name': 'sum',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}],
                'comment': 'Somma due numeri'
            },
            {
                'name': 'multiply',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'x'}, {'type': 'int', 'name': 'y'}],
                'comment': 'Moltiplica due numeri'
            },
            {
                'name': 'factorial',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola il fattoriale di n'
            }
        ]

        for data in exercises_data:
            ex, created = Exercise.objects.get_or_create(
                name=data['name'],
                defaults={
                    'return_type': data['return_type'],
                    'params': data['params'],
                    'comment': data['comment']
                }
            )
            # Associa l'esercizio a tutti i corsi
            ex.courses.set(courses)
            ex.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Creato esercizio: {ex.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Esercizio già esistente: {ex.name}'))

        self.stdout.write(self.style.SUCCESS('Generazione esercizi completata!'))
