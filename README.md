# GPU Code Runner

## 🎯 Panoramica

GPU Code Runner è un'applicazione web che permette agli studenti di:
- Registrarsi e autenticarsi nel sistema con email e password
- Selezionare esercizi di programmazione C/C++ basati sul proprio corso di laurea
- Scrivere e testare codice in un editor integrato
- Visualizzare i risultati dell'esecuzione in tempo reale tramite simulazione GPU

## 🛠️ Tecnologie Utilizzate

### Backend
- **Django 5.2.6** - Framework web Python
- **Django REST Framework** - API REST
- **JWT Authentication** (SimpleJWT) - Autenticazione sicura
- **SQLite** - Database di sviluppo
- **CORS** - Gestione cross-origin requests
- **Bash Scripting** - Simulazione esecuzione GPU

### Frontend
- **React 19.1.1** - Libreria UI moderna
- **React Router DOM 7.9.1** - Navigazione tra pagine
- **Tailwind CSS 3.4.17** - Framework CSS per design moderno e professionale
- **Monaco Editor 4.7.0** - Editor di codice integrato con syntax highlighting
- **Axios 1.12.2** - Client HTTP per comunicazione con API

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.8+
- Node.js 18+
- npm

### Backend
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🔐 Autenticazione

Il sistema utilizza JWT (JSON Web Tokens) per l'autenticazione:
- **Access Token**: Valido per 60 minuti
- **Refresh Token**: Valido per 24 ore
- **Auto-refresh**: Rinnovo automatico dei token
- **User Model Personalizzato**: Email come username, matricola unica

## 📱 Pagine Principali

### Login (`/login`)
- Form di accesso con email e password
- Link alla registrazione
- Validazione lato client

### Registrazione (`/register`)
- Form completo con email, matricola, nome, cognome e password
- Selezione corso di laurea
- Validazione lato client e server

### Dashboard (`/dashboard`)
- Selezione esercizi disponibili per il corso dell'utente
- Editor Monaco con syntax highlighting C/C++
- Esecuzione e visualizzazione risultati
- Header con informazioni utente e logout

## 🎯 Funzionalità

### Gestione Esercizi
- Caricamento dinamico degli esercizi dal backend
- Filtro esercizi per corso di laurea dell'utente
- Editor Monaco con syntax highlighting
- Generazione automatica template funzione

### Esecuzione Codice
- Invio codice al backend per compilazione
- Simulazione GPU tramite script bash
- Visualizzazione stdout e stderr
- File temporanei per esecuzione sicura

### Responsive Design
- Layout adattivo per desktop e mobile
- Componenti ottimizzati per diverse dimensioni schermo

## 📊 Modelli Dati

### User (Utente Personalizzato)
- **Email**: Campo unico per login
- **Matricola**: Campo unico identificativo studente
- **Nome e Cognome**: Informazioni personali
- **Course**: Collegamento al corso di laurea

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

## 🔄 API Endpoints

### Autenticazione
- `POST /api/auth/register/` - Registrazione utente
- `POST /api/auth/login/` - Login utente
- `GET /api/auth/user/` - Informazioni utente corrente

### Esercizi
- `GET /api/exercises/` - Lista esercizi per corso utente
- `GET /api/courses/` - Lista corsi disponibili

### Esecuzione
- `POST /api/run/` - Esecuzione codice C/C++
