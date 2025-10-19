#!/usr/bin/env bash

# =============================================================================
# RUNTIME SAFETY OPTIONS
# =============================================================================
set -euo pipefail

# =============================================================================
# LOGGING (colors and helpers)
# =============================================================================
NC='\033[0m'; BOLD='\033[1m'; BLUE='\033[34m'; CYAN='\033[36m'; GREEN='\033[32m'
YELLOW='\033[33m'; RED='\033[31m'; MAGENTA='\033[35m'; GRAY='\033[90m'

log_section() { echo;echo -e "${MAGENTA}${BOLD}== $* ==${NC}"; }
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
log_section SETUP
VENV_ACTIVATED=0
check_venv() {
    for _venv_dir in "$BACKEND_DIR/.venv" "$ROOT_DIR/.venv" "$BACKEND_DIR/venv" "$ROOT_DIR/venv"; do
        if [ -f "${_venv_dir}/bin/activate" ]; then
            return 0
        fi
    done
    return 1
}

for _venv_dir in "$BACKEND_DIR/.venv" "$ROOT_DIR/.venv" "$BACKEND_DIR/venv" "$ROOT_DIR/venv"; do
    if [ -f "${_venv_dir}/bin/activate" ]; then
        log_info "Activating Python venv at ${_venv_dir}"
        source "${_venv_dir}/bin/activate"
        VENV_ACTIVATED=1
        if command -v python >/dev/null 2>&1; then
            PY_VER=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' 2>/dev/null || echo "?")
            PY_BIN=$(command -v python || echo "python")
            log_ready "Python venv active (python=${PY_BIN}, version=${PY_VER})"
        else
            log_warn "Python not found after venv activation"
        fi
        break
    fi
done

if check_venv; then
    log_info "Installing backend requirements from '$BACKEND_DIR/requirements.txt'"
    if nohup pip install -r "$BACKEND_DIR/requirements.txt" >/dev/null 2>&1 < /dev/null; then
        log_ready "Requirements installed successfully"
    else
        log_error "Failed to install requirements"
        exit 1
    fi
else
    log_error "No Python virtual environment found"
    exit 1
fi

# =============================================================================
# PATHS
# =============================================================================
log_section PATHS
log_info "ROOT_DIR= '$ROOT_DIR'"
log_info "BACKEND_DIR= '$BACKEND_DIR'"
log_info "FRONTEND_DIR= '$FRONTEND_DIR'"
log_debug "VENV_ACTIVATED= '$(check_venv && echo "yes" || echo "no")'"

# =============================================================================
# USER CONFIRMATION
# =============================================================================

if [ "$VENV_ACTIVATED" = "0" ]; then
    log_error "No Python virtual environment found"
    exit 1
fi

echo; echo
read -r -p "Proceed to start backend and frontend? (Y/n) " RESP
RESP=${RESP:-Y}
if [[ "$RESP" != "Y" && "$RESP" != "y" ]]; then
    log_info "Aborted by user."
    exit 0
fi
clear

# =============================================================================
# PRE-CLEANUP PORTS
# =============================================================================
kill_port() {
    local port="$1"
    log_debug "Pre-cleanup: killing any process on :${port} ..."
    if command -v lsof >/dev/null 2>&1; then
        local pids
        pids=$(lsof -ti TCP:"${port}" -sTCP:LISTEN 2>/dev/null || true)
        if [ -n "${pids}" ]; then
            log_warn "Found PIDs on :${port}: ${pids} — sending SIGKILL"
            kill -9 ${pids} 2>/dev/null || true
        fi
    fi
    if command -v fuser >/dev/null 2>&1; then
        fuser -k -n tcp "${port}" 2>/dev/null || true
    fi
}

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
log_info "Starting Uvicorn on :8000 (reload)"
pushd "$BACKEND_DIR" >/dev/null
"${UVICORN_CMD[@]}" backend.asgi:application --host 0.0.0.0 --port 8000 --reload &
BACK_PID=$!
popd >/dev/null

wait_for_port() {
    local host="$1"; local port="$2"; local timeout="${3:-60}"; local start
    start=$(date +%s)
    while true; do
        if command -v nc >/dev/null 2>&1; then
            nc -z -w1 "$host" "$port" >/dev/null 2>&1 && return 0
        else
            # Use a nested bash to avoid set -e effects and silence errors completely
            bash -c ">/dev/tcp/${host}/${port}" >/dev/null 2>&1 && return 0
        fi
        sleep 0.5
        [[ $(( $(date +%s) - start )) -ge $timeout ]] && return 1
    done
}

if wait_for_port 127.0.0.1 8000 10; then
    log_ready "Backend listening on :8000"
else
    log_error "Backend not reachable on :8000 after 10s"
fi

# =============================================================================
# FRONTEND STARTUP
# =============================================================================
log_section FRONTEND
log_info "Starting React dev server on :3000 (in background)"
pushd "$FRONTEND_DIR" >/dev/null
nohup npm start >/tmp/frontend.log 2>&1 </dev/null &
FRONT_PID=$!
popd >/dev/null
log_ready "Frontend running in background (pid=$FRONT_PID), logs in /tmp/frontend.log"

# =============================================================================
# SIGNAL TRAPS
# =============================================================================
cleanup() {
    log_section SHUTDOWN
    log_warn "Stopping processes ..."
    [ -n "${BACK_PID:-}" ] && log_warn "Stopping backend (pid=$BACK_PID)" && kill "$BACK_PID" 2>/dev/null || true
    [ -n "${FRONT_PID:-}" ] && log_warn "Stopping frontend (pid=$FRONT_PID)" && kill "$FRONT_PID" 2>/dev/null || true
    echo
}

on_exit() {
    [ "$VENV_ACTIVATED" = "1" ] && type deactivate >/dev/null 2>&1 && deactivate || true
    cleanup
}

trap on_exit EXIT
trap cleanup INT TERM

wait "$BACK_PID"
