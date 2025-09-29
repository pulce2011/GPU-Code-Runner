# GPU Code Runner

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-19.1.1-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Panoramica

**GPU Code Runner** è un'applicazione web educativa che permette agli studenti di:
- Registrarsi e autenticarsi nel sistema con email e password
- Selezionare esercizi di programmazione C/C++ basati sul proprio corso di laurea
- Scrivere e testare codice in un editor integrato con syntax highlighting
- Visualizzare i risultati dell'esecuzione in tempo reale tramite simulazione GPU
- Gestire esercizi e utenti tramite interfaccia amministrativa (superuser)
- Sistema di crediti per l'esecuzione dei task
- Monitoraggio in tempo reale dello stato dei task
- Gestione intelligente dei crediti con interruzione automatica

## 🛠️ Tecnologie Utilizzate

### Backend
- **Django 5.2.6** - Framework web Python
- **Django REST Framework** - API REST
- **JWT Authentication** (SimpleJWT) - Autenticazione sicura
- **SQLite** - Database di sviluppo
- **CORS** - Gestione cross-origin requests
- **Bash Scripting** - Simulazione esecuzione GPU
- **Threading** - Esecuzione asincrona dei task
- **Subprocess** - Gestione processi esterni

### Frontend
- **React 19.1.1** - Libreria UI moderna
- **React Router DOM 7.9.1** - Navigazione tra pagine
- **Tailwind CSS 3.4.17** - Framework CSS per design moderno e professionale
- **Monaco Editor 4.7.0** - Editor di codice integrato con syntax highlighting
- **Axios 1.12.2** - Client HTTP per comunicazione con API

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.10+
- Node.js 18+
- npm

### Configurazione iniziale (da fare solo una volta)

1. **Clona il repository e crea l'ambiente virtuale:**
```bash
git clone https://github.com/pulce2011/GPU-Code-Runner.git
cd GPUCodeRunner
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

2. **Installa le dipendenze:**
```bash
pip install -r requirements.txt
```

3. **Configura il database:**
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

4. **Crea un utente amministratore:**
```bash
python manage.py createsuperuser
```

5. **Popola il database con dati di esempio:**
```bash
python manage.py generate_courses
python manage.py generate_exercises
```

6. **Avvia il server backend:**
```bash
python manage.py runserver 0.0.0.0:8000
```

7. **Accedi all'interfaccia amministrativa:**
   - Vai su `http://localhost:8000/admin`
   - Effettua l'accesso con le credenziali dell'utente ```superuser```
   - Gestisci Corsi, Esercizi ed Utenti tramite l'interfaccia Django

8. **Installa le dipendenze React (frontend):**
```bash
cd frontend
npm install
```

9. **Avvia il server frontend:**
```bash
npm start
```

### Comandi di gestione database

#### Per eliminare automaticamente tutti i Corsi ed Esercizi:
```bash 
cd backend
python manage.py clear_courses
python manage.py clear_exercises
```

### Avvio dell'applicazione

#### Backend:
```bash 
source venv/bin/activate
cd backend
python manage.py runserver 0.0.0.0:8000
```

#### Frontend:
```bash 
cd frontend
npm start
```

L'applicazione sarà disponibile su `http://localhost:3000`

## 🔐 Autenticazione e Autorizzazione

Il sistema utilizza JWT (JSON Web Tokens) per l'autenticazione:
- **Access Token**: Valido per 60 minuti
- **Refresh Token**: Valido per 24 ore
- **Auto-refresh**: Rinnovo automatico dei token
- **User Model Personalizzato**: Email come username, matricola unica

### Tipi di Utenti
- **Studenti**: Possono accedere solo agli esercizi del proprio corso
- **Superuser**: Accesso completo a tutti gli esercizi e interfaccia amministrativa

## 💰 Sistema di Crediti

### Gestione Crediti
- **Crediti iniziali**: Ogni utente ha un numero limitato di crediti
- **Costo operazione**: 1 credito per avviare un task + 1 secondo bonus
- **Deduzione automatica**: 1 credito ogni secondo di esecuzione
- **Interruzione automatica**: Il task viene interrotto automaticamente quando i crediti si esauriscono
- **Crediti illimitati**: Superuser e staff hanno crediti infiniti (∞)

## 📱 Pagine Principali

### Login (`/login`)
- Form di accesso con email e password
- Link alla registrazione
- Validazione lato client
- Stato di caricamento durante l'autenticazione

### Registrazione (`/register`)
- Form completo con email, matricola, nome, cognome e password
- Selezione corso di laurea
- Validazione lato client e server

### Dashboard (`/dashboard`)
- Selezione esercizi disponibili per il corso dell'utente (o tutti per superuser)
- Editor Monaco con syntax highlighting C/C++
- Sistema di crediti con visualizzazione in tempo reale
- Monitoraggio task con stati in tempo reale
- Header con informazioni utente e logout
- Visualizzazione "Utente amministratore" per superuser

## 🎯 Funzionalità

### Gestione Esercizi
- Caricamento dinamico degli esercizi dal backend
- Filtro esercizi per corso di laurea dell'utente
- Editor Monaco con syntax highlighting
- Generazione automatica template funzione
- Componenti modulari per migliore manutenibilità

### Esecuzione Codice
- Invio codice al backend per compilazione
- Simulazione GPU tramite script bash (`simulate_gpu.sh`)
- Esecuzione asincrona con threading
- Visualizzazione stdout e stderr in tempo reale
- File temporanei per esecuzione sicura
- Gestione errori di compilazione ed esecuzione

### Stati dei Task
- **Pending**: Task in attesa di esecuzione
- **Running**: Task in esecuzione
- **Completed**: Task completato con successo
- **Failed**: Task fallito
- **Interrupted**: Task interrotto per crediti esauriti
- **Insufficient Credits**: Crediti insufficienti per avviare il task

### Feedback Visivo
- **Spinner animato** per stati di attesa
- **Icone colorate** per ogni stato del task
- **Messaggi dedicati** per ogni situazione
- **Sezioni condizionali** per output e dettagli

### Responsive Design
- Layout adattivo per desktop e mobile
- Componenti ottimizzati per diverse dimensioni schermo

## 📊 Modelli Dati

### User (Utente Personalizzato)
- **Email**: Campo unico per login
- **Matricola**: Campo unico identificativo studente
- **Nome e Cognome**: Informazioni personali
- **Course**: Collegamento al corso di laurea
- **Credits**: Numero di crediti disponibili
- **has_credits()**: Metodo per verificare crediti disponibili
- **reduce_credits()**: Metodo per dedurre crediti

### Course (Corso)
- **Nome**: Nome del corso di laurea
- **Relazione**: Many-to-Many con Exercise

### Exercise (Esercizio)
- **Nome**: Nome della funzione
- **Return Type**: Tipo di ritorno della funzione
- **Params**: Parametri JSON con tipo e nome
- **Comment**: Consegna/commento dell'esercizio
- **Courses**: Collegamento ai corsi (Many-to-Many)
- **build_signature()**: Metodo per generare template funzione

### Task (Nuovo)
- **User**: Collegamento all'utente
- **Exercise**: Collegamento all'esercizio
- **Code**: Codice da eseguire
- **Status**: Stato del task (pending, running, completed, failed, interrupted)
- **Stdout/Stderr**: Output del processo
- **Credits Cost**: Crediti utilizzati
- **Execution Time**: Tempo di esecuzione
- **Process ID**: ID del processo in esecuzione
- **Message**: Messaggio di stato
- **Metodi**: start(), pending(), complete(), fail(), interrupt()

## 🔄 API Endpoints

### Autenticazione
- `POST /api/auth/register/` - Registrazione utente
- `POST /api/auth/login/` - Login utente
- `GET /api/auth/user/` - Informazioni utente corrente

### Esercizi e Corsi
- `GET /api/exercises/` - Lista esercizi per corso utente (tutti per superuser)
- `GET /api/courses/` - Lista corsi disponibili

### Esecuzione
- `POST /api/run/` - Esecuzione codice C/C++ (ritorna task_id)
- `GET /api/tasks/{id}/` - Stato e dettagli del task

## 🚀 Deployment

### Sviluppo
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Admin: `http://localhost:8000/admin`

### Produzione
Per il deployment in produzione, considera:
- Configurazione di un database PostgreSQL
- Impostazione di variabili d'ambiente per sicurezza
- Configurazione di nginx come reverse proxy
- Utilizzo di HTTPS con certificati SSL

## 🤝 Contributi

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file `LICENSE` per maggiori informazioni.

## 🆘 Supporto

Per problemi o domande:
- Apri una issue su GitHub
- Contatta il team di sviluppo
- Consulta la documentazione dell'API