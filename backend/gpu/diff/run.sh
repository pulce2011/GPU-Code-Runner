#!/usr/bin/env bash
set -e
cd gpu/diff
nvcc main.cu -DTEMP_FILE_PATH="\"$1\"" -o temp_exe
./temp_exe
rm -f temp_exe
