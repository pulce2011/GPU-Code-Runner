#!/usr/bin/env bash
set -e

CODE_PATH="${1}"
EXERCISE_NAME="${2}"
USER_MATR="${3}"
TIMESTAMP=$(date +%s)
PID=$$
cd gpu/$EXERCISE_NAME

# Genera un nome univoco per l'eseguibile: <MATR>_<timestamp>_<pid>.out
EXECUTABLE_NAME="${USER_MATR}_${TIMESTAMP}_${PID}.out"

# Funzione di cleanup per assicurarsi che l'eseguibile venga sempre rimosso
cleanup() {
    rm -f "$EXECUTABLE_NAME"
}
trap cleanup EXIT

nvcc main.cu -DTEMP_FILE_PATH="\"$CODE_PATH\"" -o "$EXECUTABLE_NAME"
./"$EXECUTABLE_NAME"