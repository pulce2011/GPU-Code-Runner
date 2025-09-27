#!/bin/bash
# simulate_gpu.sh
# $1 = percorso file codice da eseguire (temporaneo)

echo "> Avvio simulazione GPU..."
sleep $((RANDOM % 4))
echo "> Simulazione completata"
echo "> File: $1"
echo "> Questo è l output anche se il processo fallisce" >&2

exit $((RANDOM % 2))