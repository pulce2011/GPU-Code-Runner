#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

echo "> [INFO]Script args:"
for arg in "$@"; do
    echo "> [INFO] $arg"
done
echo "> [INFO]Total args: $#"

echo "> [DEBUG] Standard output"
echo "> [DEBUG] Standard error" >&2

# Genera un numero casuale per determinare se il task è riuscito o fallito
exit $((RANDOM % 2))