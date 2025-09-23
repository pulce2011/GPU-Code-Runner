from django.core.management.base import BaseCommand
from core.models import Course

class Command(BaseCommand):
    help = 'Svuota il database da tutti i corsi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Conferma l\'operazione di cancellazione',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING('ATTENZIONE: Questo comando cancellerà TUTTI i corsi!')
            )
            self.stdout.write(
                self.style.WARNING('Usa --confirm per confermare l\'operazione')
            )
            return

        # Conta i corsi prima della cancellazione
        course_count = Course.objects.count()
        
        if course_count == 0:
            self.stdout.write(self.style.WARNING('Nessun corso presente nel database'))
            return

        # Cancella tutti i corsi
        Course.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Cancellati {course_count} corsi dal database')
        )
