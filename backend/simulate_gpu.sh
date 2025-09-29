#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

sleep_duration=$((RANDOM % 7))
echo "> Durata sleep: $sleep_duration secondi"

sleep $sleep_duration
echo "> [DEBUG] Standard output"
echo "> [DEBUG] Standard error" >&2

exit $((RANDOM % 2))