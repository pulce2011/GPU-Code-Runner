# GPU-Code-Runner

## 📘 Descrizione del progetto

**GPU-Code-Runner** è una piattaforma web per l'esecuzione di codice su GPU in ambiente controllato. Il sistema permette agli utenti di:

* scrivere ed eseguire esercizi CUDA direttamente da interfaccia web,
* gestire i propri crediti giornalieri di esecuzione,
* interagire con un backend Python/Django con supporto WebSocket,
* visualizzare risultati e log in tempo reale.

Il progetto integra **frontend React**, **backend Django** e **moduli CUDA**, con un'infrastruttura automatizzata per il reset dei crediti e l'esecuzione su GPU.

---

## 🧱 Architettura generale

### **Frontend (React + TailwindCSS)**

* Gestisce l'interfaccia utente (login, editor, dashboard, risultati).
* Comunica con il backend tramite API REST e WebSocket.
* Contiene componenti modulari (CodeEditor, RunButton, ExerciseSelector, ecc.).

### **Backend (Django)**

* Gestisce autenticazione, utenti, crediti e logiche di business.
* Espone API per il frontend e comandi personalizzati per la manutenzione (es. reset crediti, generazione esercizi).
* Include moduli CUDA nella cartella `gpu/` (esempi `sum/`, `diff/`).

### **GPU / Esecuzione CUDA**

* Ogni task GPU viene eseguito tramite script shell (`run.sh`) che compila e lancia il file `main.cu` corrispondente.
* Gli output vengono gestiti dal backend e restituiti all'utente.

---

## ⚙️ Installazione e requisiti software

### **Requisiti principali:**

* Python 3.10+
* Node.js 18+
* npm o yarn
* CUDA Toolkit installato e configurato
* (Opzionale) NVCV Toolkit per elaborazioni avanzate

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

## 🔁 Reset giornaliero crediti (cron job)

Il sistema include un meccanismo automatico che resetta i crediti degli utenti ogni giorno alle **00:00**.


## 📂 Struttura delle directory

```
GPU-Code-Runner-main/
├── launch.sh
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── core/
│   │   ├── models.py, views.py, websocket.py, ...
│   │   └── management/commands/ (comandi personalizzati)
│   ├── gpu/
│   │   ├── sum/main.cu
│   │   └── diff/main.cu
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/, pages/, hooks/, services/
│   │   └── App.js, index.js, ecc.
└── README.md
```

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
