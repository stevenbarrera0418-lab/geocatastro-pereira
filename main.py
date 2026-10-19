from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI(title="Geocatastro Pereira API REST", version="1.0")

class PredioUpdate(BaseModel):
    propietario: str
    estadoSismo: str
    observaciones: str

class Afectado(BaseModel):
    id: Optional[str] = None
    cedula: str
    nombre: str
    lote: int
    area: str
    lat: str
    lon: str
    danio: str
    albergue: str

predios_db = [
    {
        "id": i + 1,
        "completado": False,
        "propietario": f"Propietario Lote API {i+1}",
        "documento": f"{10834500 + i}",
        "numeroPredial": f"6600101000000000200{(i+1):03d}00000000",
        "matricula": f"290-{200000 + i}",
        "estadoSismo": "Colapsado / Demolición Controlada" if i % 3 == 0 else "Avería Moderada (Reparable)",
        "observaciones": "Inspección técnica post-terremoto registrada vía API Python."
    }
    for i in range(45)
]

afectados_db = []
for i in range(25):
    lote_num = (i % 45) + 1
    lat = f"{4.8133 + (lote_num * 0.0012):.5f}"
    lon = f"{-75.6961 - (lote_num * 0.0011):.5f}"
    area = f"{120 + (lote_num * 15.5):.2f} m²"
    afectados_db.append({
        "id": f"afc-{i+1}",
        "cedula": f"{10592000 + i}",
        "nombre": f"Ciudadano API Python Afectado {i+1}",
        "lote": lote_num,
        "area": area,
        "lat": lat,
        "lon": lon,
        "danio": "Colapsado / Demolición" if i % 3 == 0 else "Avería Moderada (Reparable)",
        "albergue": "Subsidio de Arrendamiento Asignado" if i % 2 == 0 else "En Albergue Temporal Plaza Cívica"
    })

@app.get("/api/v1/predios")
def get_predios():
    return predios_db

@app.get("/api/v1/predios/{predio_id}")
def get_predio(predio_id: int):
    predio = next((p for p in predios_db if p["id"] == predio_id), None)
    if not predio:
        raise HTTPException(status_code=404, detail="Predio no encontrado")
    return predio

@app.put("/api/v1/predios/{predio_id}")
def update_predio(predio_id: int, data: PredioUpdate):
    predio = next((p for p in predios_db if p["id"] == predio_id), None)
    if not predio:
        raise HTTPException(status_code=404, detail="Predio no encontrado")
    predio["propietario"] = data.propietario
    predio["estadoSismo"] = data.estadoSismo
    predio["observaciones"] = data.observaciones
    predio["completado"] = True
    return {"status": 200, "message": "Actualizado exitosamente", "data": predio}

@app.get("/api/v1/afectados")
def get_afectados():
    return afectados_db

@app.post("/api/v1/afectados")
def create_or_update_afectado(afectado: Afectado):
    global afectados_db
    if afectado.id:
        idx = next((i for i, a in enumerate(afectados_db) if a["id"] == afectado.id), -1)
        if idx != -1:
            afectados_db[idx] = afectado.dict()
            return {"status": 200, "data": afectados_db[idx]}
    
    afectado.id = f"afc-{int(time.time()*1000)}"
    afectados_db.insert(0, afectado.dict())
    return {"status": 200, "data": afectado.dict()}

@app.delete("/api/v1/afectados/{afectado_id}")
def delete_afectado(afectado_id: str):
    global afectados_db
    afectados_db = [a for a in afectados_db if a["id"] != afectado_id]
    return {"status": 200, "message": "Eliminado con éxito"}

@app.get("/", response_class=HTMLResponse)
def serve_home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Geocatastro Pereira</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f6f9; color: #333; text-align: center; padding: 50px; }
            .card { background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            p { font-size: 16px; color: #555; }
            .btn { display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Geocatastro Pereira - Sistema Activo</h1>
            <p>La API de gestión catastral y sismológica está funcionando correctamente en Render.</p>
            <a class="btn" href="/api/v1/predios" target="_blank">Ver Datos de Predios (API)</a>
        </div>
    </body>
    </html>
    """
