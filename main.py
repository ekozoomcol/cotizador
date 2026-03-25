import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import app as api_app

print("DEBUG: main.py is being loaded")
app = api_app
print(f"DEBUG: app instance: {id(app)}")

@app.get("/lista-de-fondos")
def list_fondos_new():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fondos_dir = os.path.join(base_dir, "static", "fondos")
    if not os.path.exists(fondos_dir):
        return []
    valid_exts = ('.png', '.jpg', '.jpeg', '.webp')
    files = [f for f in os.listdir(fondos_dir) if f.lower().endswith(valid_exts)]
    return sorted(files)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/fondos", StaticFiles(directory=os.path.join(BASE_DIR, "static", "fondos")), name="fondos")

app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True), name="static")