# GPU-Code-Runner

## 📘 Descrizione del progetto

**GPU-Code-Runner** è una piattaforma web per l'esecuzione di codice su GPU in ambiente controllato.
#### Il sistema permette agli utenti di:

* scrivere ed eseguire esercizi CUDA direttamente da interfaccia web
* gestire i propri crediti giornalieri di esecuzione
* interagire con un backend Python/Django con supporto WebSocket
* visualizzare risultati e log in tempo reale

Il progetto integra **frontend React**, **backend Django** e **moduli CUDA**, con un'infrastruttura automatizzata per il reset dei crediti e l'esecuzione del codice su GPU.

---

## 🧱 Architettura generale

### **Frontend (React + TailwindCSS)**

* Gestisce l'interfaccia utente (login, editor, dashboard, risultati).
* Comunica con il backend tramite API REST e WebSocket.
* Contiene componenti modulari (CodeEditor, RunButton, ExerciseSelector, ecc.).

### **Backend (Django)**

* Gestisce autenticazione, utenti, crediti e tasks.
* Espone API REST per il frontend e comandi personalizzati per la manutenzione.
* Include funzionalità WebSocket per aggiornamenti real-time.
* Include esercizi CUDA nella cartella `gpu/` (esempi `sum/`, `diff/`).
* Sistema di coda per gestire task concorrenti.
* Comandi di gestione per reset crediti, generazione dati di esempio e pulizia database.

### **GPU / Esecuzione CUDA**

* Ogni task GPU viene eseguito tramite script shell (`run_exercise.sh`) che compila e lancia il codice CUDA.
* Gli output vengono gestiti dal backend e restituiti all'utente in tempo reale.
* Sistema di monitoraggio crediti con interruzione automatica se insufficienti.
* Supporto per diversi tipi di esercizi con configurazioni personalizzate.

---

## ⚙️ Installazione e requisiti software

### **Requisiti principali:**

* Python 3.10+
* Node.js 18+
* npm o yarn
* CUDA Toolkit installato e configurato

### **Installazione step-by-step**

1. **Clona il repository**

   ```bash
   git clone https://github.com/tuoutente/GPU-Code-Runner.git
   cd GPU-Code-Runner-main
   ```
   ---

2. **Configura il file `.env` per il backend**
    ###### DJANGO CORE SETTINGS
    - `DEBUG`: true
    - `ALLOWED_HOSTS`: 'localhost,127.0.0.1'
    - `CORS_ALLOWED_ORIGINS`: 'http://localhost:5173,http://localhost:3000'

    ###### CREDIT SYSTEM CONFIGURATION
    - `USER_INITIAL_CREDITS`: 100
    - `DAILY_CREDITS_RESET_AMOUNT`: 10
    - `TASK_START_COST`: 1
    - `REDUCE_CREDITS_TIME_AMOUNT`: 1.0
    - `DEFAULT_CREDIT_COST_PER_TIME_AMOUNT`: 1

    ###### CODE EXECUTION & COMPILATION
    - `DEFAULT_FILE_EXTENSION`: '.cu'
    - `MAX_TASK_EXECUTION_TIME`: 20
    - `MAX_SOURCE_CODE_LENGTH`: 10000
    - `MAX_OUTPUT_BUFFER_SIZE`: 50000
    - `MAX_CONCURRENT_TASKS`: 5
    - `CODE_COMPILATION_TIMEOUT`: 10
    - `PROGRAM_EXECUTION_TIMEOUT`: 20
    - `SCRIPT_DEBUG`: true

    ####### AUTHENTICATION & SECURITY
    - `JWT_ACCESS_TOKEN_LIFETIME`: 60
    - `JWT_REFRESH_TOKEN_LIFETIME`: 1440
    - `CSRF_TRUSTED_ORIGINS`: 'http://localhost:3000,http://localhost:5173'

---

3. **Avvia il sistema automaticamente**

   ```bash
   chmod +x launch.sh
   ./launch.sh
   ```

   #### Se si vuole saltare la fase di verifica:
   ```bash
   ./launch.sh -y
   ```

   Lo script si occuperà di:
   * creare e attivare ambiente virtuale Python (venv)
   * verificare se CUDA-Toolkit è installato nel sistema
   * installare dipendenze backend e frontend
   * mostrare variabili .env
   * configurare il cron per il reset giornaliero crediti
   * pulizia delle porte interessate
   * avviare i servizi di backend e frontend
   * eseguire una pulizia al termine dello script

---

## 🚀 Avvio manuale

Se vuoi avviare i servizi manualmente (senza `launch.sh`):

### **Backend**

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### **Frontend**

```bash
cd frontend
npm start
```

---

## 🆕 Funzionalità Principali

### **Comunicazione Real-time**
* **WebSocket**: Aggiornamenti in tempo reale durante l'esecuzione dei task
* **Monitoraggio Live**: Visualizzazione output e stato di esecuzione senza refresh
* **Interruzione Automatica**: Stop immediato se crediti insufficienti

### **Sistema di Gestione**
* **Comandi Django**: Tool per amministrazione e manutenzione
* **Reset Automatico**: Cron job per reset giornaliero crediti alle 00:00
* **Coda Task**: Gestione intelligente di task concorrenti
* **Pulizia Database**: Comandi per reset completo o parziale dati

### **Editor Avanzato**
* **Monaco Editor**: Supporto completo per CUDA e altri linguaggi
* **Template Predefiniti**: Signature di funzioni per ogni esercizio
* **Sintassi Highlighting**: Evidenziazione codice in tempo reale

---

## 🔁 Reset giornaliero crediti (cron job)

Il sistema include un meccanismo automatico che resetta i crediti degli utenti ogni giorno alle **00:00**.


## 📂 Struttura delle directory

```
GPU-Code-Runner/
├── launch.sh
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── run_exercise.sh
│   ├── core/
│   │   ├── models.py, views.py, websocket.py, routing.py
│   │   ├── serializers.py, urls.py, admin.py
│   │   └── management/commands/ (comandi personalizzati)
│   │       ├── reset_daily_credits.py
│   │       ├── generate_courses.py
│   │       ├── generate_exercises.py
│   │       ├── clear_courses.py
│   │       ├── clear_exercises.py
│   │       └── clear_tasks.py
│   ├── gpu/
│   │   ├── sum/main.cu
│   │   └── diff/main.cu
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeEditor.js
│   │   │   ├── ExerciseSelector.js
│   │   │   ├── RunButton.js
│   │   │   ├── Login.js, Register.js
│   │   │   ├── ProtectedRoute.js
│   │   │   └── config/ (configurazioni editor)
│   │   ├── pages/
│   │   │   ├── DashboardPage.js
│   │   │   ├── LoginPage.js
│   │   │   └── RegisterPage.js
│   │   ├── services/ (API e WebSocket)
│   │   └── hooks/ (React hooks personalizzati)
├── docs/
│   ├── RunExerciseView_Private_Methods_rendered.md
│   ├── RunExerciseView_Private_Methods_rendered.pdf
│   ├── flowcharts/ (diagrammi Mermaid)
│   └── render_mermaid_to_svg.py
└── README.md
```

---

## 🛠️ Comandi di Gestione

Il sistema include diversi comandi Django per la gestione e manutenzione:

### **Comandi Disponibili**

```bash
# Reset crediti giornaliero
python manage.py reset_daily_credits

# Generazione dati di esempio
python manage.py generate_courses
python manage.py generate_exercises

# Pulizia database
python manage.py clear_courses
python manage.py clear_exercises
python manage.py clear_tasks
```

### **Utilizzo Comandi**

* **`reset_daily_credits`**: Ripristina i crediti di tutti gli utenti al valore configurato
* **`generate_courses`**: Crea corsi predefiniti nel database
* **`generate_exercises`**: Crea esercizi CUDA con template predefiniti
* **`clear_*`**: Rimuove tutti i record del tipo specificato dal database

---

## 🔗 Link utili

* [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
* [NVCV (NVIDIA CV Toolkit)](https://developer.nvidia.com/nvcv)
* [Django Documentation](https://docs.djangoproject.com/)
* [React Documentation](https://react.dev/)

---

## ✍️ Autore e licenza

Progetto sviluppato da **Cerchi Filippo** (UniMoRe – Scienze Informatiche).

---
