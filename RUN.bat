@echo off
echo Starting Flask server...
start cmd /k "py server.py"

echo Starting Discord bot...
start cmd /k "py index.py"

echo Starting Ngrok...
start cmd /k "ngrok http 5000"

echo All processes started.
pause
