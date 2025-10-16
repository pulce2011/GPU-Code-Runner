#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

echo "> [INFO] Script args:"
for arg in "$@"; do
    echo "> [INFO] $arg"
done
echo "> [INFO] Total args: $#"

# Simulazione output progressivo (stdout e stderr) con attese
for i in {1..5}; do
    echo "> [STDOUT] step $i at $(date +%H:%M:%S)"
    echo "> [STDERR] step $i at $(date +%H:%M:%S)" >&2
    sleep 1
done

echo "> [STDOUT] finishing at $(date +%H:%M:%S)"
echo "> [STDERR] finishing at $(date +%H:%M:%S)" >&2

# Genera un numero casuale per determinare se il task è riuscito o fallito
exit $((RANDOM % 2))