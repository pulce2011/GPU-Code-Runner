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
                'comment': 'Somma due numeri interi'
            },
            {
                'name': 'multiply',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'x'}, {'type': 'int', 'name': 'y'}],
                'comment': 'Moltiplica due numeri interi'
            },
            {
                'name': 'factorial',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola il fattoriale di n (n!)'
            },
            {
                'name': 'fibonacci',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola l\'n-esimo numero di Fibonacci'
            },
            {
                'name': 'is_prime',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Verifica se un numero è primo (1 se vero, 0 se falso)'
            },
            {
                'name': 'gcd',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}],
                'comment': 'Calcola il massimo comun divisore tra due numeri'
            },
            {
                'name': 'power',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'base'}, {'type': 'int', 'name': 'exp'}],
                'comment': 'Calcola base elevato a exp'
            },
            {
                'name': 'reverse_number',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Inverte le cifre di un numero'
            },
            {
                'name': 'count_digits',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Conta il numero di cifre di un numero'
            },
            {
                'name': 'sum_digits',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola la somma delle cifre di un numero'
            },
            {
                'name': 'is_palindrome',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Verifica se un numero è palindromo (1 se vero, 0 se falso)'
            },
            {
                'name': 'lcm',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}],
                'comment': 'Calcola il minimo comune multiplo tra due numeri'
            },
            {
                'name': 'max_of_three',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}, {'type': 'int', 'name': 'c'}],
                'comment': 'Trova il massimo tra tre numeri'
            },
            {
                'name': 'min_of_three',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}, {'type': 'int', 'name': 'c'}],
                'comment': 'Trova il minimo tra tre numeri'
            },
            {
                'name': 'is_even',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Verifica se un numero è pari (1 se vero, 0 se falso)'
            },
            {
                'name': 'is_odd',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Verifica se un numero è dispari (1 se vero, 0 se falso)'
            },
            {
                'name': 'square',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola il quadrato di un numero'
            },
            {
                'name': 'cube',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola il cubo di un numero'
            },
            {
                'name': 'absolute_value',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Calcola il valore assoluto di un numero'
            },
            {
                'name': 'sum_squares',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}],
                'comment': 'Calcola la somma dei quadrati di due numeri'
            },
            {
                'name': 'difference_squares',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'a'}, {'type': 'int', 'name': 'b'}],
                'comment': 'Calcola la differenza dei quadrati di due numeri'
            },
            {
                'name': 'is_perfect_square',
                'return_type': 'int',
                'params': [{'type': 'int', 'name': 'n'}],
                'comment': 'Verifica se un numero è un quadrato perfetto (1 se vero, 0 se falso)'
            }
        ]

        created_count = 0
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
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Esercizio già esistente: {ex.name}'))

        self.stdout.write(self.style.SUCCESS(f'Generazione esercizi completata! Creati {created_count} nuovi esercizi.'))
