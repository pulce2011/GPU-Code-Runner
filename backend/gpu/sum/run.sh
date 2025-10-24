#!/usr/bin/env bash
CODE_PATH="$1"
EXERCISE_NAME="$2"
USER_MATR="$3"

set -e

# Genera un nome univoco per l'eseguibile: tmp_M<MATR>_<timestamp>_<pid>.out
TIMESTAMP=$(date +%s)
PID=$$
EXECUTABLE_NAME="tmp_M${USER_MATR}_${TIMESTAMP}_${PID}.out"

# Carica variabili di debug da .env
if [ -f ".env" ]; then
    if grep -q "^SCRIPT_DEBUG=" .env; then
        export $(grep "^SCRIPT_DEBUG=" .env | xargs)
    fi
else
    echo "> [ERROR] File .env non trovato"
    SCRIPT_DEBUG=false
fi

# Debug mode se abilitato
if [ "$SCRIPT_DEBUG" = "true" ]; then
    echo "> === SCRIPT DEBUG (run.sh) ==="; sleep 0.1
    echo ">     Executable name: '$EXECUTABLE_NAME'"; sleep 0.1
    echo "> === END DEBUG ==="; sleep 0.1
    echo
fi

# Funzione di cleanup per assicurarsi che l'eseguibile venga sempre rimosso
cleanup() {
    rm -f "$EXECUTABLE_NAME"
}
trap cleanup EXIT

# Compila e esegue il programma
cd gpu/${EXERCISE_NAME}
nvcc main.cu -DTEMP_FILE_PATH="\"$CODE_PATH\"" -o "$EXECUTABLE_NAME"
./"$EXECUTABLE_NAME"
