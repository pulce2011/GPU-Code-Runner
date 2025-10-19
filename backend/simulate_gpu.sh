#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

echo "> [INFO] Script args:"
for arg in "$@"; do
    echo "> [INFO] $arg"
    sleep 1
done

sleep 1
echo "> [INFO] Total args: $#"

sleep 1
echo "> [STDOUT] finishing at $(date +%H:%M:%S)"
echo "> [STDERR] finishing at $(date +%H:%M:%S)" >&2

# Genera un numero casuale per determinare se il task è riuscito o fallito
exit $((RANDOM % 2))