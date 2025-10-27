#!/bin/bash
# run_exercise.sh
# $1 = percorso file codice da eseguire (temporaneo)
# $2 = nome dell'esercizio
# $3 = matricola utente

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
    echo "> === SCRIPT DEBUG ==="; sleep 0.1
    echo ">     Exercise: $2"; sleep 0.1
    echo ">     Code path: $1"; sleep 0.1
    echo ">     User matr: $3"; sleep 0.1
    echo "> === END DEBUG ==="; sleep 0.1
    echo
fi

# Esegue lo script specifico per l'esercizio
CODE_PATH="${1}"
EXERCISE_NAME="${2}"
USER_MATR="${3}"
bash "gpu/${EXERCISE_NAME}/run.sh" "$CODE_PATH" "$EXERCISE_NAME" "$USER_MATR"
exit $?