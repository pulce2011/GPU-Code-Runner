# 🎓 GPU Code Runner Web App

Questo progetto è una web-app sviluppata come tesi, che permette agli studenti di:
- Autenticarsi (login/registrazione).
- Selezionare il proprio **corso di studi**.
- Visualizzare e scegliere una **consegna di esercizio** associata al corso.
- Scrivere il corpo di una funzione all’interno di un editor online.
- Eseguire il codice (simulando l’esecuzione su GPU) tramite uno **script bash**.
- Visualizzare **stdout** e **stderr** prodotti dall’esecuzione.

---

## 📐 Architettura

L’applicazione è composta da due parti principali:

- **Frontend (React)**  
  - Gestione login/registrazione.  
  - Dashboard con select per la scelta dell’esercizio.  
  - Editor integrato (Monaco Editor) con autocompletamento della firma della funzione.  
  - Bottone *RUN* per inviare il codice al backend.  
  - Visualizzazione dell’output (stdout/stderr).  

- **Backend (Django + Django REST Framework)**  
  - API per autenticazione e gestione utenti.  
  - API per corsi ed esercizi (solo quelli legati al corso dello studente).  
  - API per esecuzione codice → salvataggio in file temporaneo + chiamata a script bash con `subprocess`.  
  - Database PostgreSQL con gestione tramite ORM Django.  
  - Admin panel per inserimento e gestione corsi/esercizi.  

---

## 🗂️ Modello Dati (semplificato)

- **Utente**  
  - `id`  
  - `nome`  
  - `cognome`  
  - `email`
  - `matr`  
  - `password_hash`  
  - `corso_id` (FK → Corsi)  

- **Corso**  
  - `id`  
  - `nome`  

- **Esercizio**  
  - `id`  
  - `name`  
  - `params`  
  - `comment`  
  - `return_type`  
  - `corso_id`

---

## 🔄 Flusso Utente

1. Lo studente si registra scegliendo un **corso di studi**.  
2. Effettua il **login**.  
3. Accede alla **dashboard**, che mostra solo gli esercizi associati al proprio corso.  
4. Seleziona una consegna → l’editor autocompila la firma della funzione.  
5. Lo studente scrive il **body** della funzione.  
6. Clicca su *RUN* → il backend lancia lo script bash che esegue il codice.  
7. Viene mostrato **stdout** e **stderr** sul frontend.  

---

## 🛠️ Stack Tecnologico

- **Frontend:**  
  - React + TailwindCSS  
  - Monaco Editor  
  - Autenticazione via JWT  

- **Backend:**  
  - Django + Django REST Framework  
  - Autenticazione e gestione utenti con JWT  
  - `subprocess` per esecuzione codice  

- **Database:**  
  - SQLite  

- **Altri strumenti:**  
  - Docker (per containerizzare backend e DB)  
  - Nginx (reverse proxy in produzione)  

---

## 🚀 Setup Locale

### Requisiti
- Node.js ≥ 18  
- Python ≥ 3.10  
- PostgreSQL ≥ 14  
- Docker (opzionale)  

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
