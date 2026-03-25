@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creando entorno virtual...
  python -m venv .venv
)

echo [INFO] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo [INFO] Levantando cotizador en http://localhost:8585/admin.html
start "" http://localhost:8585/admin.html
".venv\Scripts\python.exe" -m uvicorn main:app --host localhost --port 8585 --reload

endlocal