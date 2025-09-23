# 🎓 GPU Code Runner Web App

Questa web-app, sviluppata come progetto di tesi, permette agli studenti di:

- Registrarsi e autenticarsi tramite **email e matricola**.  
- Selezionare il proprio **corso di studi**.  
- Visualizzare e scegliere una **consegna di esercizio** associata al corso.  
- Scrivere il corpo di una funzione in un **editor online** (Monaco Editor) con firma e commento autocompilati.  
- Eseguire il codice (simulazione GPU tramite **script bash**) e visualizzare **stdout** e **stderr**.  
- Fare **logout** e mantenere la sessione attiva anche al refresh del browser grazie a JWT.

---

## 📐 Architettura

L’applicazione è composta da due parti principali:

### Frontend (React)

- Gestione login e logout.  
- Dashboard con selezione esercizi filtrati per corso.  
- Monaco Editor con autocompletamento della **firma della funzione** (tipo, nome e parametri).  
- Bottone *RUN* per inviare il codice al backend.  
- Visualizzazione dell’output (stdout/stderr).  
- Persistenza dei token JWT in `localStorage` per mantenere la sessione attiva al refresh.  

### Backend (Django + DRF)

- API per autenticazione via **JWT** (access + refresh token).  
- API per gestione utenti, corsi ed esercizi (solo quelli del corso dello studente).  
- API per esecuzione codice:  
  - Salvataggio codice in file temporaneo.  
  - Esecuzione tramite **script bash** (`simulate_gpu.sh`).  
  - Restituzione stdout/stderr.  
- Database (PostgreSQL o SQLite in locale) gestito tramite ORM Django.  
- Admin panel per gestione corsi ed esercizi.

---

## 🗂️ Modello Dati

### Utente (`User`)
- `id`  
- `email` (login)  
- `matr` (matricola, unica)  
- `first_name`  
- `last_name`  
- `password` (hash)  
- `course` (FK → Course)

### Corso (`Course`)
- `id`  
- `name`  

### Esercizio (`Exercise`)
- `id`  
- `name` (nome funzione)  
- `return_type` (tipo di ritorno)  
- `params` (lista JSON dei parametri)  
- `comment` (consegna)  
- `courses` (ManyToMany con corsi)

---

## 🔄 Flusso Utente

1. Registrazione dello studente con selezione del **corso di studi**.  
2. Login (persistenza JWT).  
3. Dashboard: visualizzazione solo degli esercizi del proprio corso.  
4. Selezione esercizio → **firma della funzione e commento autocompilati** nell’editor.  
5. Scrittura del **body** della funzione.  
6. Clic su *RUN* → backend salva codice su file temporaneo e chiama `simulate_gpu.sh`.  
7. Output (`stdout` e `stderr`) visualizzato nel frontend.  
8. Logout → rimozione token e ritorno al login.

---

## 🛠️ Stack Tecnologico

**Frontend**
- React + TailwindCSS  
- Monaco Editor  
- Axios per chiamate API  
- Autenticazione via JWT (persistenza token in localStorage)  

**Backend**
- Django + Django REST Framework  
- Autenticazione e gestione utenti con JWT  
- Modelli per utenti, corsi ed esercizi  
- `subprocess` per esecuzione codice simulata  
- Admin panel per gestione contenuti

**Database**
- SQLite (locale) / PostgreSQL (produzione)

**Altri strumenti**
- Docker (opzionale, per container backend + DB)  
- Nginx (reverse proxy in produzione)

---

## 🚀 Setup Locale

### Requisiti
- Node.js ≥ 18  
- Python ≥ 3.10  
- PostgreSQL ≥ 14 (opzionale per SQLite)  
- Docker (opzionale)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # opzionale, per admin
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

- Il frontend gira su `http://localhost:3000`  
- Il backend gira su `http://127.0.0.1:8000`  

---

## 📌 Note Aggiuntive

- Script di simulazione GPU: `simulate_gpu.sh` (deve essere eseguibile).  
- JWT: access token ha durata breve (~5 minuti), refresh token gestisce il rinnovo automatico.  
- Logout: rimuove token da memoria e `localStorage`, resetta stato React.  
- Il codice scritto dall’utente non viene salvato in DB, solo eseguito temporaneamente.

