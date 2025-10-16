#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

#sleep_duration=$((RANDOM % 7))
sleep_duration=1
echo "> Durata sleep: $sleep_duration secondi"
sleep $sleep_duration

echo "> [INFO]Script args:"
for arg in "$@"; do
    sleep 1
    echo "> [INFO] $arg"
done
echo "> [INFO]Total args: $#"

echo "> [DEBUG] Standard output"
echo "> [DEBUG] Standard error" >&2

# Genera un numero casuale per determinare se il task è riuscito o fallito
exit $((RANDOM % 2))