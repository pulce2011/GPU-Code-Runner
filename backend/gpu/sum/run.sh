echo "> [INFO] Running exercise..."
echo "> [SUM] filename: $1"

sleep 1

nvcc main.cu  -o temp_exe #occhio a path che saranno relativi a dove viene lanciato il processo. Il nome dell'eseguibile non deve essere uguale all'eseguibile di altri processi
./temp_exe