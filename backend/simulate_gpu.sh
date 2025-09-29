#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

echo "> Avvio simulazione GPU..."
sleep_duration=$((RANDOM % 7))
echo "> Durata sleep: $sleep_duration secondi"

sleep $sleep_duration
echo "> Simulazione completata"
echo "> File: $1"
echo "> Questo è l output anche se il processo fallisce" >&2

exit $((RANDOM % 2))