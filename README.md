# GPU Code Runner

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-19.1.1-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Panoramica

**GPU Code Runner** è un'applicazione web educativa avanzata che permette agli studenti di:
- Registrarsi e autenticarsi nel sistema con email e password
- Selezionare esercizi di programmazione C/C++ basati sul proprio corso di laurea
- Scrivere e testare codice in un editor integrato con syntax highlighting
- Visualizzare i risultati dell'esecuzione in tempo reale tramite simulazione GPU
- Gestire esercizi e utenti tramite interfaccia amministrativa Django (superuser)
- Sistema di crediti intelligente per l'esecuzione dei task con deduzione automatica
- Monitoraggio in tempo reale dello stato dei task tramite WebSocket
- Gestione intelligente dei crediti con interruzione automatica quando esauriti
- Reset giornaliero automatico dei crediti tramite cron job
- Esecuzione asincrona dei task con threading e gestione processi
- Streaming real-time dell'output durante l'esecuzione
- Interruzione automatica dei task alla disconnessione del client
- Gestione sicura dei file temporanei per l'esecuzione del codice

## 🛠️ Tecnologie Utilizzate

### Backend
- **Django 5.2.6** - Framework web Python con architettura MVC
- **Django REST Framework 3.16.1** - API REST con serializzazione automatica
- **JWT Authentication** (SimpleJWT 5.5.1) - Autenticazione sicura con token
- **SQLite** - Database di sviluppo con migrazioni automatiche
- **Django CORS Headers 4.9.0** - Gestione cross-origin requests
- **Django Channels 4.1.0** - WebSocket per aggiornamenti realtime
- **Channels Redis 4.2.0** - Backend Redis per Django Channels
- **Uvicorn 0.37.0 (ASGI)** - Application server ad alte prestazioni
- **Python Decouple 3.8** - Gestione configurazioni e variabili d'ambiente
- **Bash Scripting** - Simulazione esecuzione GPU con script personalizzati
- **Threading** - Esecuzione asincrona dei task con gestione processi
- **Subprocess** - Gestione sicura dei processi esterni
- **Select** - Lettura non bloccante dell'output dei processi
- **Signal** - Gestione segnali per interruzione processi
- **Tempfile** - Creazione sicura di file temporanei
- **Cron Jobs** - Reset automatico giornaliero dei crediti

### Frontend
- **React 19.1.1** - Libreria UI moderna con hooks e context
- **React Router DOM 7.9.1** - Navigazione tra pagine con routing dinamico
- **Tailwind CSS 3.4.17** - Framework CSS utility-first per design moderno
- **Monaco Editor 4.7.0** - Editor di codice integrato con syntax highlighting C/C++
- **Axios 1.12.2** - Client HTTP per comunicazione con API REST
- **WebSocket Client** - Connessione real-time per aggiornamenti task
- **React Hooks** - Gestione stato e lifecycle dei componenti
- **Protected Routes** - Sistema di autenticazione e autorizzazione

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.10+
- Node.js 18+
- npm
- Redis (per Django Channels WebSocket)

### Configurazione iniziale (da fare solo una volta)

1. **Clona il repository:**
```bash
git clone https://github.com/pulce2011/GPU-Code-Runner.git
cd GPU-Code-Runner/
```

2. **Configura il database:**
```bash
cd backend/
python manage.py makemigrations
python manage.py migrate
```

3. **Crea un utente amministratore:**
```bash
python manage.py createsuperuser
```

4. **Popola il database con dati di esempio:**
```bash
python manage.py generate_courses
python manage.py generate_exercises
```

5. **Installa le dipendenze React (frontend):**
```bash
cd frontend/
npm install
```

### Avvio dell'applicazione

#### Metodo 1: Script automatico (Raccomandato)
```bash
# Dalla root del progetto
chmod +x run.sh
./run.sh
```

Lo script `run.sh` si occupa automaticamente di:
- Creazione e attivazione dell'ambiente virtuale Python
- Installazione delle dipendenze backend
- Configurazione del cron job per il reset giornaliero dei crediti
- Pulizia delle porte 8000 e 3000
- Avvio del backend Django con Uvicorn
- Avvio del frontend React
- Gestione della terminazione pulita dei processi

#### Metodo 2: Avvio manuale

**Backend:**
```bash 
cd backend
source backend/venv/bin/activate
uvicorn backend.asgi:application --host 0.0.0.0 --port 8000 --reload
```

**Frontend (in un altro terminale):**
```bash 
cd frontend
npm start
```

### Comandi di gestione database

#### Per eliminare automaticamente tutti i Corsi ed Esercizi:
```bash 
cd backend
python manage.py clear_courses
python manage.py clear_exercises
```

#### Per resettare i crediti di tutti gli utenti:
```bash
cd backend
python manage.py reset_daily_credits
```

### Interfaccia amministrativa
- Vai su `http://localhost:8000/admin`
- Effettua l'accesso con le credenziali dell'utente superuser
- Gestisci Corsi, Esercizi ed Utenti tramite l'interfaccia Django

##### L'applicazione sarà disponibile su `http://localhost:3000`

## 🔐 Autenticazione e Autorizzazione

Il sistema utilizza JWT (JSON Web Tokens) per l'autenticazione:
- **Access Token**: Valido per 60 minuti
- **Refresh Token**: Valido per 24 ore
- **Auto-refresh**: Rinnovo automatico dei token
- **User Model Personalizzato**: Email come username, matricola unica

### Endpoints Autenticazione (SimpleJWT)
- `POST /api/token/` - Ottieni access e refresh token
- `POST /api/token/refresh/` - Rinnova l'access token
- `GET /api/user/` - Informazioni utente corrente (autenticato)

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
- **Reset**: Ogni giorno alle ore 00:00 i crediti degli utenti vengono impostati a 10

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
- Caricamento dinamico degli esercizi dal backend con filtri per corso
- Editor Monaco Editor con syntax highlighting C/C++ avanzato
- Generazione automatica template funzione con commenti e parametri
- Supporto per file di inclusione personalizzati (`#include`)
- File extra opzionali per esercizi complessi
- Estensioni file configurabili (.c, .cpp, etc.)
- Componenti modulari React per migliore manutenibilità
- Selezione esercizi basata sul corso di laurea dell'utente

### Esecuzione Codice Avanzata
- Invio codice al backend per compilazione e esecuzione
- Simulazione GPU tramite script bash personalizzati (`simulate_gpu.sh`)
- Esecuzione asincrona con threading per non bloccare l'interfaccia
- Visualizzazione stdout e stderr in tempo reale tramite WebSocket streaming
- File temporanei sicuri per esecuzione isolata del codice
- Gestione errori di compilazione ed esecuzione con messaggi dettagliati
- Interruzione automatica dei task alla disconnessione del client
- Terminazione sicura dei processi con timeout e fallback SIGKILL
- Monitoraggio continuo dei processi con lettura non bloccante dell'output

### Sistema di Crediti Intelligente
- Crediti iniziali configurabili per ogni utente (default: 100)
- Deduzione automatica: 1 credito per avviare + 1 credito ogni secondo di esecuzione
- Interruzione automatica quando i crediti si esauriscono
- Crediti illimitati per superuser e staff
- Reset giornaliero automatico tramite cron job alle 00:00
- Visualizzazione crediti in tempo reale nell'interfaccia
- Gestione crediti thread-safe con aggiornamenti atomici

### Monitoraggio Real-time
- WebSocket per aggiornamenti istantanei dello stato dei task
- Streaming dell'output durante l'esecuzione (stdout/stderr incrementali)
- Stati dei task: `pending`, `running`, `completed`, `failed`, `interrupted`
- Visualizzazione durata di esecuzione in tempo reale
- Messaggi di stato dettagliati per ogni fase del task
- Scroll automatico ai messaggi di stato nell'interfaccia
- Connessione WebSocket resiliente con riconnessione automatica

### Interfaccia Utente Moderna
- Design responsive con Tailwind CSS
- Editor Monaco Editor integrato con IntelliSense
- Componenti React modulari e riutilizzabili
- Navigazione protetta con autenticazione JWT
- Form di login e registrazione con validazione client-side
- Dashboard personalizzata per ogni tipo di utente
- Header informativo con dati utente e logout
- Indicatori visivi per stato crediti e task

## 📊 Modelli Dati

### User (Utente Personalizzato)
- `email` (EmailField, unico, username per login)
- `matr` (CharField, matricola unica)
- `first_name`, `last_name` (CharField)
- `course` (ForeignKey opzionale a `Course`)
- `credits` (IntegerField, default 100)
- `is_staff`, `is_superuser` (BooleanField, crediti illimitati)
- Metodi: `has_credits(amount=1)`, `reduce_credits(amount=1)`
- Manager personalizzato: `UserManager` con creazione utenti via email

### Course (Corso)
- `name` (CharField, max_length=200)
- Relazioni: `exercises` (Many-to-Many da `Exercise`)
- Metodo: `__str__()` per rappresentazione stringa

### Exercise (Esercizio)
- `name` (CharField, max_length=200)
- `return_type` (CharField, max_length=50)
- `params` (JSONField, default lista vuota)
- `comment` (TextField, descrizione esercizio)
- `courses` (ManyToManyField con `Course`)
- `file_extension` (CharField, default da configurazione ".c")
- `extra_files` (JSONField, default lista vuota)
- `include_files` (JSONField, default lista vuota)
- Metodo: `build_signature()` - genera template funzione con commenti e include

### Task (Richiesta di Esecuzione)
- `user` (ForeignKey a `User`)
- `exercise` (ForeignKey a `Exercise`)
- `code` (TextField, codice da eseguire)
- `status` (CharField con scelte: `pending`, `running`, `completed`, `failed`, `interrupted`)
- `created_at` (DateTimeField, auto_now_add=True)
- `started_at` (DateTimeField, nullable)
- `finished_at` (DateTimeField, nullable)
- `total_execution_time` (DurationField, nullable)
- `stdout`, `stderr` (TextField, output dell'esecuzione)
- `credits_cost` (IntegerField, default 1)
- `process_id` (IntegerField, nullable, PID del processo)
- `message` (TextField, messaggio di stato)
- Metodi: `start()`, `pending()`, `complete(stdout, stderr)`, `fail(stdout, stderr)`, `interrupt(stdout, stderr)`

## 🔄 API Endpoints

### Autenticazione (SimpleJWT)
- `POST /api/token/` - Ottieni access e refresh token
- `POST /api/token/refresh/` - Rinnova l'access token
- `POST /api/register/` - Registrazione nuovo utente
- `GET /api/user/` - Informazioni utente corrente (autenticato)

### Esercizi e Corsi
- `GET /api/exercises/` - Lista esercizi per corso utente (tutti per superuser)
- `GET /api/courses/` - Lista corsi disponibili

### Esecuzione e Task Management
- `POST /api/run/` - Esecuzione codice C/C++ (ritorna `task_id`)
- `GET /api/tasks/{id}/` - Stato e dettagli del task specifico
- `GET /api/tasks/` - Lista ultimi 10 task dell'utente

### WebSocket Real-time
- `WS /ws/tasks/{id}/` - Connessione WebSocket per aggiornamenti realtime
  - Streaming stdout/stderr incrementali durante l'esecuzione
  - Aggiornamenti di stato: `pending` → `running` → `completed`/`failed`/`interrupted`
  - Interruzione automatica alla disconnessione del client

## 🚀 Deployment

### Sviluppo
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Admin: `http://localhost:8000/admin`

## 📚 Informazioni Progetto

**GPU Code Runner** è il progetto di tesi del corso di **Scienze Informatiche** presso l'**Università degli Studi di Modena e Reggio Emilia (Unimore)**.

### Autore
**Filippo Cerchi**