@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creando entorno virtual...
  python -m venv .venv
)

echo [INFO] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo [INFO] Levantando cotizador en http://127.0.0.1:8000/
start "" http://127.0.0.1:8000/
".venv\Scripts\python.exe" -m uvicorn main:app --reload

endlocal