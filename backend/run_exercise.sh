#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

# Carica solo variabili specifiche da .env
if [ -f ".env" ]; then
    if grep -q "^INFO_DEBUG=" .env; then
        export $(grep "^INFO_DEBUG=" .env | xargs)
    fi
else
    echo "> [ERROR] File .env non trovato"
    INFO_DEBUG=false
fi

if [ "$INFO_DEBUG" = "true" ]; then
    echo "> === INFO DEBUG ==="
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

bash gpu/sum/run.sh $1

# Genera un numero casuale per determinare se il task è riuscito o fallito
exit $((RANDOM % 2))
