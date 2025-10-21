#!/bin/bash
# run_exercise.sh
# $1 = percorso file codice da eseguire (temporaneo)
# $2 = nome dell'esercizio

# Carica solo variabili specifiche da .env
if [ -f ".env" ]; then
    if grep -q "^SCRIPT_DEBUG=" .env; then
        export $(grep "^SCRIPT_DEBUG=" .env | xargs)
    fi
else
    echo "> [ERROR] File .env non trovato"
    SCRIPT_DEBUG=false
fi

if [ "$SCRIPT_DEBUG" = "true" ]; then
    echo "> === SCRIPT DEBUG ==="
    echo "> Script args:"
    c=1
    for arg in "$@"; do
        echo ">     $c. $arg"
        c=$((c + 1))
        sleep 0.1
    done
    echo "> Total args: $#"
    sleep 0.1
    echo "> === END DEBUG ==="

fi

EXERCISE_NAME="${2}"

bash "gpu/${EXERCISE_NAME}/run.sh" "$1"
exit $?