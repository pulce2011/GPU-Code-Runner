from django.core.management.base import BaseCommand
from core.models import Task, User
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Pulisce i task dal database con diverse opzioni'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Elimina TUTTI i task (richiede --confirm)',
        )
        parser.add_argument(
            '--completed',
            action='store_true',
            help='Elimina solo i task completati',
        )
        parser.add_argument(
            '--failed',
            action='store_true',
            help='Elimina solo i task falliti',
        )
        parser.add_argument(
            '--interrupted',
            action='store_true',
            help='Elimina solo i task interrotti',
        )
        parser.add_argument(
            '--older-than',
            type=int,
            help='Elimina task più vecchi di X giorni',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Elimina task di un utente specifico (matricola)',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Conferma l\'operazione di cancellazione',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Mostra solo le statistiche senza eliminare nulla',
        )

    def handle(self, *args, **options):
        # Mostra statistiche
        self.show_stats()
        
        if options['stats']:
            return
        
        # Determina quale operazione eseguire
        if options['all']:
            self.clear_all_tasks(options['confirm'])
        elif options['completed']:
            self.clear_completed_tasks()
        elif options['failed']:
            self.clear_failed_tasks()
        elif options['interrupted']:
            self.clear_interrupted_tasks()
        elif options['older_than']:
            self.clear_old_tasks(options['older_than'])
        elif options['user']:
            self.clear_user_tasks(options['user'])
        else:
            self.stdout.write(
                self.style.WARNING('Specifica un\'opzione. Usa --help per vedere le opzioni disponibili.')
            )

    def show_stats(self):
        """Mostra le statistiche dei task"""
        total = Task.objects.count()
        running = Task.objects.filter(status='running').count()
        pending = Task.objects.filter(status='pending').count()
        completed = Task.objects.filter(status='completed').count()
        failed = Task.objects.filter(status='failed').count()
        interrupted = Task.objects.filter(status='interrupted').count()
        
        self.stdout.write(self.style.SUCCESS('📊 Statistiche Task:'))
        self.stdout.write(f'  - Totali: {total}')
        self.stdout.write(f'  - In esecuzione: {running}')
        self.stdout.write(f'  - In attesa: {pending}')
        self.stdout.write(f'  - Completati: {completed}')
        self.stdout.write(f'  - Falliti: {failed}')
        self.stdout.write(f'  - Interrotti: {interrupted}')

    def clear_all_tasks(self, confirm):
        """Elimina tutti i task"""
        if not confirm:
            self.stdout.write(
                self.style.ERROR('ATTENZIONE: Questo eliminerà TUTTI i task!')
            )
            self.stdout.write(
                self.style.WARNING('Usa --confirm per confermare l\'operazione')
            )
            return
        
        count = Task.objects.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('Nessun task da eliminare'))
            return
        
        Task.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'✅ Eliminati {count} task')
        )

    def clear_completed_tasks(self):
        """Elimina solo i task completati"""
        count = Task.objects.filter(status='completed').count()
        if count == 0:
            self.stdout.write(self.style.WARNING('Nessun task completato da eliminare'))
            return
        
        Task.objects.filter(status='completed').delete()
        self.stdout.write(
            self.style.SUCCESS(f'✅ Eliminati {count} task completati')
        )

    def clear_failed_tasks(self):
        """Elimina solo i task falliti"""
        count = Task.objects.filter(status='failed').count()
        if count == 0:
            self.stdout.write(self.style.WARNING('Nessun task fallito da eliminare'))
            return
        
        Task.objects.filter(status='failed').delete()
        self.stdout.write(
            self.style.SUCCESS(f'✅ Eliminati {count} task falliti')
        )

    def clear_interrupted_tasks(self):
        """Elimina solo i task interrotti"""
        count = Task.objects.filter(status='interrupted').count()
        if count == 0:
            self.stdout.write(self.style.WARNING('Nessun task interrotto da eliminare'))
            return
        
        Task.objects.filter(status='interrupted').delete()
        self.stdout.write(
            self.style.SUCCESS(f'✅ Eliminati {count} task interrotti')
        )

    def clear_old_tasks(self, days):
        """Elimina task più vecchi di X giorni"""
        cutoff_date = timezone.now() - timedelta(days=days)
        old_tasks = Task.objects.filter(created_at__lt=cutoff_date)
        count = old_tasks.count()
        
        if count == 0:
            self.stdout.write(
                self.style.WARNING(f'Nessun task più vecchio di {days} giorni')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Eliminando {count} task più vecchi di {days} giorni...')
        )
        old_tasks.delete()
        self.stdout.write(
            self.style.SUCCESS(f'✅ Eliminati {count} task più vecchi di {days} giorni')
        )

    def clear_user_tasks(self, matr):
        """Elimina task di un utente specifico"""
        try:
            user = User.objects.get(matr=matr)
            count = Task.objects.filter(user=user).count()
            
            if count == 0:
                self.stdout.write(
                    self.style.WARNING(f'L\'utente {matr} non ha task')
                )
                return
            
            Task.objects.filter(user=user).delete()
            self.stdout.write(
                self.style.SUCCESS(f'✅ Eliminati {count} task dell\'utente {matr}')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Utente {matr} non trovato')
            )
