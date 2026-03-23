from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import app as api_app

app = api_app

app.mount("/", StaticFiles(directory="static", html=True), name="static")