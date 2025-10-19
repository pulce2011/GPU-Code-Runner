from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils import timezone
from django.conf import settings
from core.models import User


class Command(BaseCommand):
    help = 'Reimposta i crediti per tutti gli utenti con crediti inferiori al valore specificato.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--credits',
            type=int,
            default=getattr(settings, 'DAILY_CREDITS', 10),
            help='Numero di crediti da assegnare (default: settings.DAILY_CREDITS)'
        )

    def handle(self, *args, **options):
        credits = options['credits']
        started_at = timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')
        self.stdout.write(f'[reset_daily_credits] Inizio reset crediti a {credits} — {started_at}')

        # Aggiorna solo gli utenti con crediti < credits
        updated = User.objects.filter(credits__lt=credits).update(credits=credits)

        finished_at = timezone.now().strftime('%Y-%m-%d %H:%M:%S %Z')
        self.stdout.write(self.style.SUCCESS(f'[reset_daily_credits] Completato — aggiornati {updated} utenti — {finished_at}'))
