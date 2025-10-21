#!/usr/bin/env bash

# =============================================================================
# RUNTIME SAFETY OPTIONS
# =============================================================================
set -euo pipefail #exit on error, undefined variables, pipefail

# =============================================================================
# LOGGING (colors and helpers)
# =============================================================================
NC='\033[0m'; BOLD='\033[1m'; BLUE='\033[34m'; CYAN='\033[36m'; GREEN='\033[32m'
YELLOW='\033[33m'; RED='\033[31m'; MAGENTA='\033[35m'; GRAY='\033[90m'

# Log functions
log_section() { echo; echo -e "${MAGENTA}${BOLD}== $* ==${NC}"; }
log_subsection() { echo -e "${RED}$*${NC}"; }
log_info()    { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ready()   { echo -e "${GREEN}[READY]${NC} $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $*"; }
log_debug()   { echo -e "${GRAY}[DEBUG]${NC} $*"; }

# =============================================================================
# PROJECT PATHS
# =============================================================================
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# =============================================================================
# PYTHON VIRTUAL ENVIRONMENT
# =============================================================================
log_section CONFIGURAZIONE
VENV_ACTIVATED=0 #0: no venv, 1: venv found

# Check if a venv is available; set VENV_DIR when found
check_venv() {
    for _venv_dir in "$BACKEND_DIR/venv"; do
        if [ -f "${_venv_dir}/bin/activate" ]; then
            VENV_DIR="${_venv_dir}"
            return 0
        fi
    done
    return 1
}

# Create venv if not exists
if ! check_venv; then
    target_venv_dir="$BACKEND_DIR/venv"
    log_warn "Nessun ambiente virtuale trovato. Creo un venv in '${target_venv_dir}'"
    py_sys=""
    if command -v python3 >/dev/null 2>&1; then
        py_sys=$(command -v python3)
    elif command -v python >/dev/null 2>&1; then
        py_sys=$(command -v python)
    else
        log_error "Python non trovato nel sistema: impossibile creare il venv"
        exit 1
    fi
    if "$py_sys" -m venv "$target_venv_dir" >/dev/null 2>&1; then
        log_ready "Creato ambiente virtuale in '${target_venv_dir}'"
        VENV_DIR="$target_venv_dir"
    else
        log_error "Creazione del venv fallita in '${target_venv_dir}'"
        exit 1
    fi
fi

# Activate the venv
if check_venv; then
    log_info "Attivazione ambiente virtuale Python '${VENV_DIR}'"
    source "${VENV_DIR}/bin/activate"
    VENV_ACTIVATED=1
    if command -v python >/dev/null 2>&1; then
        PY_VER=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' 2>/dev/null || echo "?")
        PY_BIN=$(command -v python || echo "python")
        log_ready "Ambiente virtuale Python attivo (versione=${PY_VER})"
    else
        log_warn "Python non trovato dopo l'attivazione del venv"
    fi
else
    log_error "Nessun ambiente virtuale Python trovato"
    exit 1
fi

# =============================================================================
# DEPENDENCIES
# =============================================================================
log_section DIPENDENZE

# NVCC
log_info "Controllo se CUDA-Toolkit è installato"
if command -v nvcc >/dev/null 2>&1; then
    log_ready "NVCC installato (versione=$(nvcc --version | grep "release" | awk '{print $6}' | sed 's/,//'))"
else
    log_error "Installazione NVCC (CUDA Toolkit)..."
fi

# Backend
if check_venv; then
    log_info "Installazione dipendenze backend da '$BACKEND_DIR/requirements.txt'"
    if nohup pip install -r "$BACKEND_DIR/requirements.txt" >/dev/null 2>&1 < /dev/null; then
        log_ready "Dipendenze backend installate correttamente"
    else
        log_error "Installazione dipendenze backend fallita"
        exit 1
    fi
else
    log_error "Nessun ambiente virtuale Python trovato"
    exit 1
fi

# Frontend
if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    log_info "Installazione dipendenze frontend da '$FRONTEND_DIR/package.json'"
    pushd "$FRONTEND_DIR" >/dev/null
    if nohup npm install >/dev/null 2>&1 < /dev/null; then
        log_ready "Dipendenze frontend installate correttamente"
    else
        log_error "Installazione dipendenze frontend fallita"
        popd >/dev/null
        exit 1
    fi
    popd >/dev/null
else
    log_warn "Node.js o npm non trovato: salto installazione dipendenze frontend"
fi


# =============================================================================
# PATHS
# =============================================================================
log_section PERCORSI
log_info "ROOT_DIR = '$ROOT_DIR'"
log_info "BACKEND_DIR = '$BACKEND_DIR'"
log_info "FRONTEND_DIR = '$FRONTEND_DIR'"
log_info "VENV_ACTIVATED= '$(check_venv && echo "yes" || echo "no")'"

# =============================================================================
# .ENV
# =============================================================================
log_section "VARIABILI '.env'"

ENV_FILE="$BACKEND_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    # Carica tutte le variabili di configurazione
    export $(grep -E "^(SECRET_KEY|DEBUG|ALLOWED_HOSTS|CORS_ALLOWED_ORIGINS|USER_INITIAL_CREDITS|DAILY_CREDITS_RESET_AMOUNT|TASK_START_COST|DEFAULT_CREDIT_COST_PER_SECOND|DEFAULT_FILE_EXTENSION|MAX_TASK_EXECUTION_TIME|MAX_SOURCE_CODE_LENGTH|MAX_OUTPUT_BUFFER_SIZE|CODE_COMPILATION_TIMEOUT|PROGRAM_EXECUTION_TIMEOUT|MAX_CONCURRENT_TASKS|JWT_ACCESS_TOKEN_LIFETIME|JWT_REFRESH_TOKEN_LIFETIME|CSRF_TRUSTED_ORIGINS|SCRIPT_DEBUG)=" "$ENV_FILE" | xargs)
else
    log_error "File $ENV_FILE non trovato"
fi

# Log dei valori caricati
log_subsection "DJANGO CORE SETTINGS"
log_info "DEBUG = ${DEBUG:-'not set'}"
log_info "ALLOWED_HOSTS = ${ALLOWED_HOSTS:-'not set'}"
log_info "CORS_ALLOWED_ORIGINS = ${CORS_ALLOWED_ORIGINS:-'not set'}"

log_subsection "CREDIT SYSTEM CONFIGURATION"
log_info "USER_INITIAL_CREDITS = ${USER_INITIAL_CREDITS:-'not set'}"
log_info "DAILY_CREDITS_RESET_AMOUNT = ${DAILY_CREDITS_RESET_AMOUNT:-'not set'}"
log_info "TASK_START_COST = ${TASK_START_COST:-'not set'}"
log_info "DEFAULT_CREDIT_COST_PER_SECOND = ${DEFAULT_CREDIT_COST_PER_SECOND:-'not set'}"

log_subsection "CODE EXECUTION & COMPILATION"
log_info "DEFAULT_FILE_EXTENSION = '${DEFAULT_FILE_EXTENSION:-'not set'}'"
log_info "MAX_TASK_EXECUTION_TIME = ${MAX_TASK_EXECUTION_TIME:-'not set'}"
log_info "MAX_SOURCE_CODE_LENGTH = ${MAX_SOURCE_CODE_LENGTH:-'not set'}"
log_info "MAX_OUTPUT_BUFFER_SIZE = ${MAX_OUTPUT_BUFFER_SIZE:-'not set'}"
log_info "CODE_COMPILATION_TIMEOUT = ${CODE_COMPILATION_TIMEOUT:-'not set'}"
log_info "PROGRAM_EXECUTION_TIMEOUT = ${PROGRAM_EXECUTION_TIMEOUT:-'not set'}"
log_info "MAX_CONCURRENT_TASKS = ${MAX_CONCURRENT_TASKS:-'not set'}"
log_info "SCRIPT_DEBUG = ${SCRIPT_DEBUG:-'not set'}"

log_subsection "AUTHENTICATION & SECURITY"
log_info "JWT_ACCESS_TOKEN_LIFETIME = ${JWT_ACCESS_TOKEN_LIFETIME:-'not set'}"
log_info "JWT_REFRESH_TOKEN_LIFETIME = ${JWT_REFRESH_TOKEN_LIFETIME:-'not set'}"
log_info "CSRF_TRUSTED_ORIGINS = ${CSRF_TRUSTED_ORIGINS:-'not set'}"

# =============================================================================
# USER CONFIRMATION
# =============================================================================

if [ "$VENV_ACTIVATED" = "0" ]; then
    log_error "Nessun ambiente virtuale Python trovato"
    exit 1
fi

echo; echo
read -r -p "Procedere con l'avvio di backend e frontend? (S/n) " RESP
RESP=${RESP:-S}
if [[ "$RESP" != "Y" && "$RESP" != "y" && "$RESP" != "S" && "$RESP" != "s" ]]; then
    log_info "Operazione annullata dall'utente."
    exit 0
fi
clear

# =============================================================================
# DAILY CREDIT RESET @ 00:00
# =============================================================================
log_section CRON
log_info "Configuro il reset giornaliero dei crediti alle 00:00"

CRON_TAG="# GPU-Code-Runner:reset_daily_credits"
CRON_LINE="0 0 * * * cd \"$BACKEND_DIR\" && \"$PY_BIN\" manage.py reset_daily_credits --credits=${DAILY_CREDITS_RESET_AMOUNT:-10} > /dev/null 2>> /tmp/reset_daily_credits.err.log ${CRON_TAG}"

# Add or update the cron job
_existing_cron=$(crontab -l 2>/dev/null || true)
if echo "$_existing_cron" | grep -F "${CRON_TAG}" >/dev/null 2>&1; then
    {
        echo "$_existing_cron" | grep -vF "${CRON_TAG}"
        echo "$CRON_LINE"
    } | crontab -
    log_ready "Voce cron aggiornata (ogni giorno alle 00:00)"
else
    {
        echo "$_existing_cron"
        echo "$CRON_LINE"
    } | crontab -
    log_ready "Voce cron aggiunta (ogni giorno alle 00:00)"
fi

# =============================================================================
# PRE-CLEANUP PORTS
# =============================================================================

# Kill processes running on a port
kill_port() {
    local port="$1"
    log_debug "Terminazione di eventuali processi su :${port}..."
    if command -v lsof >/dev/null 2>&1; then
        local pids
        pids=$(lsof -ti TCP:"${port}" -sTCP:LISTEN 2>/dev/null || true)
        if [ -n "${pids}" ]; then
            log_warn "Trovati PID su :${port}: ${pids} — invio SIGKILL"
            kill -9 ${pids} 2>/dev/null || true
        else
            log_ready "Nessun processo su :${port}"
        fi
    fi
    if command -v fuser >/dev/null 2>&1; then
        fuser -k -n tcp "${port}" 2>/dev/null || true
    fi
}

log_section PULIZIA
kill_port 8000
kill_port 3000

# =============================================================================
# UVICORN COMMAND RESOLUTION
# =============================================================================
if command -v uvicorn >/dev/null 2>&1; then
    UVICORN_CMD=(uvicorn)
else
    UVICORN_CMD=(python -m uvicorn)
fi

# =============================================================================
# BACKEND STARTUP
# =============================================================================
log_section BACKEND
log_info "Avvio backend su :8000 (uvicorn)"

# Start the backend
pushd "$BACKEND_DIR" >/dev/null
"${UVICORN_CMD[@]}" backend.asgi:application --host 0.0.0.0 --port 8000 --reload &
BACK_PID=$!
popd >/dev/null

# Wait for the backend to be ready
wait_for_port() {
    local host="$1"; local port="$2"; local timeout="${3:-60}"; local start
    start=$(date +%s)
    while true; do
        if command -v nc >/dev/null 2>&1; then
            nc -z -w1 "$host" "$port" >/dev/null 2>&1 && return 0
        else
            bash -c ">/dev/tcp/${host}/${port}" >/dev/null 2>&1 && return 0
        fi
        sleep 0.5
        [[ $(( $(date +%s) - start )) -ge $timeout ]] && return 1
    done
}

# Wait for the backend to be ready
if wait_for_port 127.0.0.1 8000 10; then
    log_ready "Backend in esecuzione su :8000"
else
    log_error "Backend non raggiungibile su :8000 dopo 10s"
fi

# =============================================================================
# FRONTEND STARTUP
# =============================================================================
log_section FRONTEND
log_info "Avvio frontend su :3000"

# Start the frontend
pushd "$FRONTEND_DIR" >/dev/null
REACT_APP_API_URL=${REACT_APP_API_URL:-http://127.0.0.1:8000/api} \
REACT_APP_WS_BASE=${REACT_APP_WS_BASE:-ws://127.0.0.1:8000} \
nohup npm start >/tmp/frontend.log 2>&1 </dev/null &
FRONT_PID=$!
popd >/dev/null

# Wait for the frontend to be ready
if wait_for_port 127.0.0.1 3000 10; then
    log_ready "Frontend in esecuzione su :3000"
else
    log_error "Frontend non raggiungibile su :3000 dopo 10s"
fi

log_section ESECUZIONE

# =============================================================================
# SIGNAL TRAPS
# =============================================================================
CLEANED_UP=0

# Cleanup function
cleanup() {
    log_section CHIUSURA
    if [ "${CLEANED_UP}" = "1" ]; then
        return 0
    fi
    CLEANED_UP=1
    [ -n "${BACK_PID:-}" ] && log_warn "Arresto backend (pid=$BACK_PID)" && kill "$BACK_PID" 2>/dev/null || true
    [ -n "${FRONT_PID:-}" ] && log_warn "Arresto frontend (pid=$FRONT_PID)" && kill "$FRONT_PID" 2>/dev/null || true
	# Rimuove la voce cron creata in precedenza (se presente)
	if crontab -l >/dev/null 2>&1; then
		_existing_cron=$(crontab -l 2>/dev/null || true)
		if echo "$_existing_cron" | grep -F "${CRON_TAG}" >/dev/null 2>&1; then
			echo "$_existing_cron" | grep -vF "${CRON_TAG}" | crontab -
			log_warn "Arresto cron ('${CRON_TAG}')"
		fi
	fi
}

# Exit handler
on_exit() {
    [ "$VENV_ACTIVATED" = "1" ] && type deactivate >/dev/null 2>&1 && deactivate || true
    cleanup
}

trap on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

wait "$BACK_PID"
