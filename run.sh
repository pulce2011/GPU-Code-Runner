#!/usr/bin/env bash

# Modalità rigorosa:
# -e  → termina lo script se un comando fallisce
# -u  → errore se viene usata una variabile non definita
# -o pipefail → fallisce la pipeline se fallisce uno dei comandi
set -euo pipefail

# Risolve i percorsi assoluti delle directory principali del progetto
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Log dei percorsi per chiarezza
echo "[DEBUG] ROOT_DIR=$ROOT_DIR"
echo "[DEBUG] BACKEND_DIR=$BACKEND_DIR"
echo "[DEBUG] FRONTEND_DIR=$FRONTEND_DIR"

# Sceglie come invocare Uvicorn (binario diretto o modulo Python)
if command -v uvicorn >/dev/null 2>&1; then
    UVICORN_CMD=(uvicorn)
else
    UVICORN_CMD=(python -m uvicorn)
fi

# Avvia il backend (ASGI/Uvicorn) in background su porta 8000
echo "[DEBUG] Starting backend (Uvicorn) on :8000 ..."
pushd "$BACKEND_DIR" >/dev/null
"${UVICORN_CMD[@]}" backend.asgi:application --host 0.0.0.0 --port 8000 --reload &
BACK_PID=$!
popd >/dev/null

# Arresto ordinato del backend alla chiusura dello script
cleanup() {
    echo "[DEBUG] Stopping backend (pid=$BACK_PID) ..."
    kill "$BACK_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Avvia il frontend (npm start) in foreground su porta 3000
echo "[DEBUG] Starting frontend (npm start) on :3000 ..."
pushd "$FRONTEND_DIR" >/dev/null
npm start
popd >/dev/null

echo "[DEBUG] Frontend exited."

