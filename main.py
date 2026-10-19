from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import time

# PRIMERO se define app
app = FastAPI(title="Geocatastro Pereira API REST", version="1.0")

BASE_DIR = Path(__file__).resolve().parent

# (Aquí van tus clases, bases de datos y luego las rutas con @app.get)
