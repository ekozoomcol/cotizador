# Usar la imagen ligera oficial base de Python (versión 3.11 recomendada)
FROM python:3.11-slim

# Evitar la creación de __pycache__ y mantener stdout limpio
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Establecer directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias primero para optimizar la caché de construcción
COPY requirements.txt .

# Instalar dependencias puras (FastAPI, Uvicorn, etc) sin caché cache de pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto por el que Cloud Run servirá la aplicación
# Cloud Run automáticamente inyecta la variable $PORT (usualmente 8080)
EXPOSE 8080

# Comando para iniciar Uvicorn en modo producción, escuchando en $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:=8080}"]
