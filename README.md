# GPU Code Runner

Sistema di valutazione esercizi di programmazione sviluppato per la tesi di laurea.

## 🎯 Panoramica

GPU Code Runner è un'applicazione web moderna che permette agli studenti di programmazione di:
- Registrarsi e autenticarsi nel sistema
- Selezionare esercizi di programmazione C/C++
- Scrivere e testare codice in un editor integrato
- Visualizzare i risultati dell'esecuzione in tempo reale

## 🛠️ Tecnologie Utilizzate

### Backend
- **Django 5.2.6** - Framework web Python
- **Django REST Framework** - API REST
- **JWT Authentication** - Autenticazione sicura
- **SQLite** - Database di sviluppo
- **CORS** - Gestione cross-origin requests

### Frontend
- **React 18** - Libreria UI
- **React Router** - Navigazione tra pagine
- **Tailwind CSS** - Framework CSS per design moderno e professionale
- **Monaco Editor** - Editor di codice integrato
- **Axios** - Client HTTP

## 🎨 Design

L'applicazione utilizza un design formale e professionale adatto per una presentazione accademica:

- **Palette colori**: Blu primario (#3b82f6) con grigi neutri
- **Tipografia**: Font Inter per leggibilità ottimale
- **Layout**: Design responsive con componenti card-based
- **UX**: Interfaccia intuitiva con feedback visivi chiari

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.8+
- Node.js 18+
- npm o yarn

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📁 Struttura del Progetto

```
GPUCodeRunner/
├── backend/
│   ├── core/
│   │   ├── models.py      # Modelli Django
│   │   ├── views.py       # API endpoints
│   │   ├── admin.py       # Configurazione admin
│   │   └── serializers.py # Serializzatori API
│   ├── backend/
│   │   └── settings.py    # Configurazione Django
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/         # Pagine principali
│   │   ├── components/    # Componenti riutilizzabili
│   │   ├── hooks/         # Custom hooks
│   │   └── services/      # Servizi API
│   ├── tailwind.config.js
│   └── package.json
└── README.md
```

## 🔐 Autenticazione

Il sistema utilizza JWT (JSON Web Tokens) per l'autenticazione:
- **Access Token**: Valido per 60 minuti
- **Refresh Token**: Valido per 24 ore
- **Auto-refresh**: Rinnovo automatico dei token

## 📱 Pagine Principali

### Login (`/login`)
- Form di accesso con validazione
- Design pulito e professionale
- Link alla registrazione

### Registrazione (`/register`)
- Form completo con tutti i campi necessari
- Selezione corso di laurea
- Validazione lato client e server

### Dashboard (`/dashboard`)
- Selezione esercizi disponibili
- Editor di codice Monaco integrato
- Esecuzione e visualizzazione risultati
- Header con logout

## 🎯 Funzionalità

### Gestione Esercizi
- Caricamento dinamico degli esercizi dal backend
- Visualizzazione firma funzione e consegna
- Editor con syntax highlighting C/C++

### Esecuzione Codice
- Invio codice al backend per compilazione
- Visualizzazione output standard e errori
- Gestione stati di caricamento

### Responsive Design
- Layout adattivo per desktop e mobile
- Componenti ottimizzati per diverse dimensioni schermo

## 🔧 Configurazione

### Variabili d'Ambiente
Il progetto supporta file `.env` per la configurazione:

**Backend** (`backend/.env`):
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

**Frontend** (`frontend/.env`):
```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
REACT_APP_APP_NAME=GPU Code Runner
```

## 📊 Modelli Dati

### User (Utente Personalizzato)
- Email come username
- Matricola unica
- Collegamento al corso di laurea

### Course (Corso)
- Nome del corso di laurea
- Collegamento agli esercizi

### Exercise (Esercizio)
- Nome e tipo di ritorno
- Parametri JSON
- Commento/consegna
- Collegamento ai corsi

## 🎓 Caratteristiche per Tesi

- **Design Professionale**: Interfaccia formale adatta per presentazioni accademiche
- **Codice Pulito**: Architettura modulare e ben documentata
- **Sicurezza**: Autenticazione JWT e validazione dati
- **Responsive**: Funziona su tutti i dispositivi
- **Documentazione**: Codice commentato e README completo

## 🤝 Contributi

Questo progetto è stato sviluppato per la tesi di laurea. Per eventuali miglioramenti o correzioni, contattare l'autore.

## 📄 Licenza

Progetto accademico - Tutti i diritti riservati.