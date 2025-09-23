from django.core.management.base import BaseCommand
from core.models import Exercise

class Command(BaseCommand):
    help = 'Svuota il database da tutti gli esercizi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Conferma l\'operazione di cancellazione',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING('ATTENZIONE: Questo comando cancellerà TUTTI gli esercizi!')
            )
            self.stdout.write(
                self.style.WARNING('Usa --confirm per confermare l\'operazione')
            )
            return

        # Conta gli esercizi prima della cancellazione
        exercise_count = Exercise.objects.count()
        
        if exercise_count == 0:
            self.stdout.write(self.style.WARNING('Nessun esercizio presente nel database'))
            return

        # Cancella tutti gli esercizi
        Exercise.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Cancellati {exercise_count} esercizi dal database')
        )
