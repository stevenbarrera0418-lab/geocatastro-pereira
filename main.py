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

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GEOCATASTRO PEREIRA - Servidor Nube Sismo 2026</title>
    <script src="https://cdn.jsdelivr.net/npm/tailwindcss-cdn@3.4.10/tailwindcss.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script>
        tailwind.config = { theme: { extend: { fontFamily: { sans: ['Outfit', 'sans-serif'], display: ['Space Grotesk', 'sans-serif'] } } } }
    </script>
    <style>
        .custom-scroll::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scroll::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.05); border-radius: 8px; }
        .custom-scroll::-webkit-scrollbar-thumb { background: rgba(16, 185, 129, 0.3); border-radius: 8px; }
        .grid-bg { background-color: rgba(11, 19, 41, 0.7); background-image: linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px); background-size: 40px 40px; }
        .bg-workspace { background-image: linear-gradient(to bottom, rgba(15, 23, 42, 0.45), rgba(11, 19, 41, 0.60)), url('https://images.unsplash.com/photo-1584646098378-0874589d76b1?q=80&w=1920&auto=format&fit=crop'); background-size: cover; background-position: center; background-attachment: fixed; }
        @media print { .no-print { display: none !important; } }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans flex flex-col selection:bg-emerald-500 selection:text-white bg-workspace relative">
    <div id="toast-container" class="fixed top-4 right-4 z-50 flex flex-col gap-3 pointer-events-none max-w-sm w-full"></div>
    <div class="fixed bottom-3 left-4 z-40 bg-slate-950/70 backdrop-blur-md border border-slate-700/80 px-4 py-1.5 rounded-full shadow-2xl pointer-events-none">
        <p class="text-[10px] text-emerald-400 font-bold uppercase tracking-wider"><i class="fa-solid fa-copyright mr-1"></i>Diseño: Ing. Steven Alonso Barrera Nieves • Cloud API</p>
    </div>

    <div id="login-screen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-cover bg-center" style="background-image: linear-gradient(to bottom, rgba(2, 6, 23, 0.50), rgba(15, 23, 42, 0.65)), url('https://images.unsplash.com/photo-1584646098378-0874589d76b1?q=80&w=1920&auto=format&fit=crop');">
        <div class="bg-slate-950/75 backdrop-blur-md border border-slate-700/80 p-8 rounded-3xl max-w-md w-full shadow-2xl relative overflow-hidden">
            <div class="text-center mb-6">
                <span class="inline-flex p-4 bg-emerald-500/20 rounded-2xl text-emerald-400 text-4xl mb-3 border border-emerald-500/30"><i class="fa-solid fa-cloud"></i></span>
                <h1 class="text-2xl font-black tracking-tight text-white font-display">GEOCATASTRO CLOUD</h1>
                <p class="text-sm text-slate-300 mt-1">Conexión Servidor Nube • Sismo 10 Ago 2026</p>
            </div>
            <form id="login-form" class="space-y-4" onsubmit="iniciarSesion(event)">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1">Operador / Topógrafo</label>
                    <input type="text" id="apprentice-name" value="Ing. Steven Barrera" required class="w-full bg-slate-950/60 border border-slate-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-500 transition font-medium">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-1">Cédula o Ficha</label>
                    <input type="text" id="apprentice-ficha" value="2671890" required class="w-full bg-slate-950/60 border border-slate-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-500 transition font-mono">
                </div>
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 px-6 rounded-xl shadow-lg transition duration-150 flex justify-center items-center gap-2 mt-2 cursor-pointer">
                    <span>Ingresar al Sistema Nube</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
                <button type="button" onclick="accesoDirecto()" class="w-full bg-cyan-700 hover:bg-cyan-600 text-white font-bold py-2.5 px-6 rounded-xl transition duration-150 flex justify-center items-center gap-2 text-xs cursor-pointer">
                    <i class="fa-solid fa-bolt"></i> Acceso Rápido Directo
                </button>
            </form>
        </div>
    </div>

    <header class="bg-slate-950/60 backdrop-blur-md border-b border-slate-700/80 px-6 py-4 flex flex-col lg:flex-row justify-between items-center gap-4 relative z-10 shadow-md">
        <div class="flex items-center gap-3">
            <span class="text-2xl text-emerald-400"><i class="fa-solid fa-globe"></i></span>
            <div>
                <h1 class="text-lg font-black text-white font-display uppercase tracking-tight">GEOCATASTRO PEREIRA • CLOUD EDITION</h1>
                <p class="text-xs text-slate-300" id="header-apprentice">Operador: Cargando...</p>
            </div>
        </div>
        <div class="flex flex-wrap items-center bg-slate-950/50 border border-slate-700/80 p-1 rounded-xl gap-1">
            <button onclick="cambiarModulo('catastro')" id="btn-tab-catastro" class="px-3 py-1.5 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow cursor-pointer"><i class="fa-solid fa-map mr-1"></i> Fichas Prediales</button>
            <button onclick="cambiarModulo('topografia-general')" id="btn-tab-topografia-general" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-300 hover:text-white cursor-pointer"><i class="fa-solid fa-compass-drafting mr-1"></i> Topografía KML</button>
            <button onclick="cambiarModulo('afectados')" id="btn-tab-afectados" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-300 hover:text-white cursor-pointer"><i class="fa-solid fa-users-rectangle mr-1"></i> Censo & Afectados</button>
            <button onclick="cambiarModulo('google-earth')" id="btn-tab-google-earth" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-300 hover:text-white cursor-pointer"><i class="fa-solid fa-earth-americas mr-1"></i> Visor Polígono Earth</button>
            <button onclick="cambiarModulo('colombia-mapas')" id="btn-tab-colombia-mapas" class="px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-300 hover:text-white cursor-pointer"><i class="fa-solid fa-map-location-dot mr-1"></i> Colombia en Mapas</button>
        </div>
        <div class="flex items-center gap-3">
            <button onclick="cerrarSesion()" class="text-xs text-slate-300 hover:text-red-400 transition font-bold uppercase tracking-wider ml-2 cursor-pointer">Salir</button>
        </div>
    </header>

    <main id="modulo-catastro" class="flex-grow grid grid-cols-1 lg:grid-cols-12 gap-6 p-6 max-w-[1700px] w-full mx-auto relative z-10 pb-12">
        <section class="lg:col-span-4 bg-slate-950/50 backdrop-blur-md border border-slate-700/80 rounded-3xl p-5 flex flex-col h-[calc(100vh-185px)] min-h-[500px]">
            <div class="mb-4 space-y-3">
                <div class="flex justify-between items-center mb-1">
                    <h2 class="text-md font-bold text-white uppercase tracking-wider flex items-center gap-2 font-display"><i class="fa-solid fa-database"></i> Predios Nube (45)</h2>
                    <span class="text-xs bg-emerald-950/80 text-emerald-400 border border-emerald-700/50 px-2 py-0.5 rounded-full font-bold" id="progress-percent">0%</span>
                </div>
                <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"><i class="fa-solid fa-search text-xs"></i></span>
                    <input type="text" id="input-busqueda-predios" oninput="filtrarPredios(this.value)" placeholder="Buscar predio..." class="w-full bg-slate-900/80 border border-slate-700 text-white text-xs rounded-xl pl-9 pr-3 py-2.5 focus:outline-none focus:border-cyan-400 transition font-mono placeholder:text-slate-500">
                </div>
                <div class="w-full bg-slate-900/60 h-1.5 rounded-full overflow-hidden">
                    <div id="progress-bar-fill" class="bg-emerald-500 h-full w-0 transition-all duration-300"></div>
                </div>
            </div>
            <div class="flex-grow overflow-y-auto custom-scroll pr-1">
                <div class="grid grid-cols-5 gap-2.5" id="predios-grid"></div>
            </div>
        </section>
        <section class="lg:col-span-8 bg-slate-950/50 backdrop-blur-md border border-slate-700/80 rounded-3xl p-6 flex flex-col h-[calc(100vh-185px)] min-h-[500px]">
            <div id="no-selection-message" class="flex-grow flex flex-col items-center justify-center text-center p-6">
                <span class="text-6xl text-slate-400 mb-4 animate-pulse"><i class="fa-solid fa-map-pin"></i></span>
                <h3 class="text-lg font-bold text-slate-200">Ningún Predio Seleccionado</h3>
                <p class="text-xs text-slate-300 max-w-sm mt-1">Seleccione un lote para ver y editar su expediente en la nube.</p>
            </div>
            <div id="ficha-container" class="hidden flex-col h-full overflow-hidden">
                <div class="border-b border-slate-800/80 pb-3 mb-4 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-bold text-emerald-400 uppercase tracking-widest font-display" id="ficha-subtitle">PREDIO N°</span>
                        <h2 class="text-lg font-bold text-white font-display" id="ficha-title">Expediente Nube & Sismo 2026</h2>
                    </div>
                    <button type="button" onclick="exportarFichaPDF()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-1.5 rounded-full text-xs transition flex items-center gap-1.5 shadow cursor-pointer">
                        <i class="fa-solid fa-file-pdf"></i> Exportar Ficha PDF
                    </button>
                </div>
                <form id="ficha-form" class="flex-grow overflow-y-auto custom-scroll pr-2 space-y-4" onsubmit="guardarPredioAPI(event)">
                    <input type="hidden" id="form-predio-id">
                    <div class="bg-slate-900/40 border border-slate-700/70 p-4 rounded-2xl space-y-3">
                        <h4 class="text-xs font-bold uppercase tracking-wider text-emerald-400"><i class="fa-solid fa-cloud mr-1"></i> Información Jurídica y Daños Terremoto</h4>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Propietario</label><input type="text" id="form-propietario" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-3 py-2 text-white text-xs"></div>
                            <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Cédula / NIT</label><input type="text" id="form-documento" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-3 py-2 text-white font-mono text-xs"></div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Estado Estructural Sismo</label>
                                <select id="form-estado-sismo" class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-3 py-2 text-white text-xs font-bold text-amber-400">
                                    <option value="Sin Daños Graves">Sin Daños Graves</option>
                                    <option value="Avería Moderada (Reparable)">Avería Moderada (Reparable)</option>
                                    <option value="Colapsado / Demolición Controlada">Colapsado / Demolición Controlada</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Número Predial (NUPRE)</label><input type="text" id="form-numero-predial" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-3 py-2 text-white font-mono text-xs"></div>
                            <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Matrícula Inmobiliaria</label><input type="text" id="form-matricula" required class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-3 py-2 text-white font-mono text-xs"></div>
                        </div>
                        <div>
                            <label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Evaluación Técnica Nube</label>
                            <textarea id="form-observaciones" rows="2" class="w-full bg-slate-950/60 border border-slate-700 rounded-xl px-3 py-2 text-white text-xs"></textarea>
                        </div>
                    </div>
                    <div class="flex justify-end gap-2">
                        <button type="submit" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-6 py-2.5 rounded-xl text-xs uppercase cursor-pointer flex items-center gap-1"><i class="fa-solid fa-floppy-disk"></i> Guardar en Nube</button>
                    </div>
                </form>
            </div>
        </section>
    </main>

    <main id="modulo-topografia-general" class="flex-grow hidden flex-col w-full h-[calc(100vh-80px)] relative pb-8">
        <header class="bg-slate-950/60 backdrop-blur-md border-b border-slate-700/80 px-6 py-3 flex justify-between items-center z-20 shadow-xl">
            <h1 class="text-xs font-black text-white font-display uppercase tracking-wider">TOPOGRAFÍA GENERAL MULTIPOLÍGONO - NUBE</h1>
        </header>
        <div class="flex-grow flex w-full h-[calc(100vh-140px)] relative">
            <aside class="w-80 bg-slate-950/50 backdrop-blur-md border-r border-slate-700/80 flex flex-col h-full overflow-hidden p-4"><span class="text-cyan-400 font-bold uppercase text-[10px]">Capas KML Nube</span></aside>
            <main class="flex-grow bg-slate-950/40 relative p-4 flex flex-col">
                <div class="w-full flex-grow bg-slate-950/60 border border-slate-700/80 rounded-2xl overflow-hidden relative grid-bg"><canvas id="canvas-workspace-general" class="w-full h-full"></canvas></div>
            </main>
        </div>
    </main>

    <main id="modulo-afectados" class="flex-grow hidden flex-col w-full h-[calc(100vh-80px)] relative p-6 max-w-[1700px] mx-auto gap-6 overflow-y-auto custom-scroll">
        <div class="bg-slate-950/70 backdrop-blur-md border border-slate-700/80 p-5 rounded-3xl shadow-xl flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
                <h2 class="text-md font-bold text-white uppercase tracking-wider flex items-center gap-2 font-display"><i class="fa-solid fa-users-rectangle text-amber-400"></i> Censo & Damnificados (Nube /api/v1/afectados)</h2>
                <p class="text-xs text-slate-300 mt-1">Base de datos sincronizada en tiempo real con el servidor web.</p>
            </div>
            <div class="flex items-center gap-2">
                <input type="text" id="input-buscar-afectado" oninput="filtrarAfectados(this.value)" placeholder="Buscar en nube..." class="bg-slate-900 border border-slate-700 text-white text-xs rounded-xl px-4 py-2.5 w-72 font-mono focus:outline-none focus:border-cyan-400 placeholder:text-slate-500">
                <button onclick="abrirModalNuevoAfectado()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition flex items-center gap-2 shadow cursor-pointer"><i class="fa-solid fa-user-plus"></i> Registrar Afectado</button>
            </div>
        </div>
        <div class="bg-slate-950/60 border border-slate-700/80 rounded-3xl p-6 shadow-2xl flex-grow overflow-hidden flex flex-col">
            <div class="flex justify-between items-center mb-4 pb-2 border-b border-slate-800">
                <h3 class="text-xs font-bold uppercase tracking-wider text-cyan-400 font-display">Registros en Servidor Cloud</h3>
                <span id="contador-afectados" class="text-xs text-slate-400 font-mono">Total Registros: 0</span>
            </div>
            <div class="flex-grow overflow-y-auto custom-scroll">
                <table class="w-full text-left text-xs font-mono">
                    <thead>
                        <tr class="border-b border-slate-800 text-slate-400 uppercase text-[10px]">
                            <th class="py-3 px-4">Cédula</th>
                            <th class="py-3 px-4">Nombre Completo</th>
                            <th class="py-3 px-4">Lote / Predio</th>
                            <th class="py-3 px-4">Área Estimada</th>
                            <th class="py-3 px-4">Coordenadas (Lat, Lon)</th>
                            <th class="py-3 px-4">Daño Sismo</th>
                            <th class="py-3 px-4 text-center">Acciones Nube</th>
                        </tr>
                    </thead>
                    <tbody id="tabla-afectados-body" class="divide-y divide-slate-800/60 text-slate-200"></tbody>
                </table>
            </div>
        </div>
    </main>

    <main id="modulo-google-earth" class="flex-grow hidden flex-col w-full h-[calc(100vh-80px)] relative p-6 max-w-[1700px] mx-auto gap-6 overflow-y-auto custom-scroll">
        <div class="bg-slate-950/70 backdrop-blur-md border border-slate-700/80 p-5 rounded-3xl shadow-xl flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
                <h2 class="text-md font-bold text-white uppercase tracking-wider flex items-center gap-2 font-display"><i class="fa-solid fa-earth-americas text-emerald-400 animate-pulse"></i> Visor de Polígono & Entorno (Pereira - Sismo 2026)</h2>
                <p class="text-xs text-slate-300 mt-1" id="earth-subtitle">Generación geométrica del lote seleccionado vía Cloud API.</p>
            </div>
            <div class="flex items-center gap-3">
                <span class="text-xs font-mono bg-slate-900 border border-slate-700 px-3 py-2 rounded-xl text-cyan-300" id="earth-badge-lote">Lote No Seleccionado</span>
                <a id="btn-abrir-earth-externo" href="https://earth.google.com/web/@4.8133,-75.6961,1411a,890d,35y,0h,0t,0r" target="_blank" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition flex items-center gap-2 shadow cursor-pointer"><i class="fa-solid fa-earth-americas"></i> Ver Lote en Google Earth</a>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-grow min-h-[500px]">
            <div class="lg:col-span-8 bg-slate-950/60 border border-slate-700/80 rounded-3xl p-5 flex flex-col relative overflow-hidden shadow-2xl">
                <div class="absolute top-6 left-6 z-10 bg-slate-950/90 backdrop-blur-md border border-slate-700 px-3 py-1.5 rounded-xl flex items-center gap-2 text-xs font-mono">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                    <span class="text-emerald-400 font-bold">Polígono Vectorial Nube Activo</span>
                </div>
                <div class="flex-grow w-full h-[450px] relative rounded-2xl overflow-hidden border border-slate-800 grid-bg flex flex-col items-center justify-center">
                    <canvas id="canvas-poligono-lote" class="w-full h-full cursor-crosshair"></canvas>
                </div>
            </div>
            <div class="lg:col-span-4 bg-slate-950/60 border border-slate-700/80 rounded-3xl p-5 flex flex-col space-y-4 shadow-2xl">
                <h3 class="text-xs font-bold uppercase tracking-wider text-cyan-400 font-display border-b border-slate-800 pb-2"><i class="fa-solid fa-chart-pie mr-1"></i> Parámetros Geodésicos Cloud</h3>
                <div class="space-y-3 text-xs font-mono">
                    <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/80"><span class="text-slate-400 block text-[10px] uppercase font-bold">Propietario:</span><span id="panel-prop" class="text-white font-bold">N/A</span></div>
                    <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/80"><span class="text-slate-400 block text-[10px] uppercase font-bold">Área Geométrica:</span><span id="panel-area" class="text-emerald-400 font-bold">0.00 m²</span></div>
                    <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/80"><span class="text-slate-400 block text-[10px] uppercase font-bold">Centroide WGS84:</span><span id="panel-coords" class="text-cyan-300">Lat: 0.00000, Lon: 0.00000</span></div>
                    <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/80"><span class="text-slate-400 block text-[10px] uppercase font-bold">Evaluación Post-Sismo:</span><span id="panel-danio" class="text-amber-400 font-bold">Pendiente</span></div>
                </div>
            </div>
        </div>
    </main>

    <main id="modulo-colombia-mapas" class="flex-grow hidden flex-col w-full h-[calc(100vh-73px)] relative m-0 p-0 overflow-hidden">
        <iframe src="https://www.colombiaenmapas.gov.co/" class="w-full h-full border-0 absolute inset-0" title="Colombia en Mapas" allowfullscreen></iframe>
    </main>

    <div id="modal-afectado" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
        <div class="bg-slate-950 border border-slate-700 p-6 rounded-3xl max-w-lg w-full shadow-2xl space-y-4">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white uppercase font-display" id="modal-titulo-afectado">Registrar Damnificado Nube</h3>
                <button onclick="cerrarModalAfectado()" class="text-slate-400 hover:text-white cursor-pointer"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <form id="form-afectado" onsubmit="guardarAfectadoAPI(event)" class="space-y-3 text-xs">
                <input type="hidden" id="afectado-id">
                <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Cédula de Ciudadanía</label><input type="text" id="afectado-cedula" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-3 py-2 font-mono"></div>
                <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Nombre Completo</label><input type="text" id="afectado-nombre" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-3 py-2"></div>
                <div class="grid grid-cols-2 gap-3">
                    <div><label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">N° de Lote / Predio (1-45)</label><input type="number" id="afectado-lote" min="1" max="45" required class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-3 py-2"></div>
                    <div>
                        <label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Daño Estructural Sismo</label>
                        <select id="afectado-danio" class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-3 py-2 text-xs">
                            <option value="Sin Daños">Sin Daños</option>
                            <option value="Avería Moderada (Reparable)">Avería Moderada (Reparable)</option>
                            <option value="Colapsado / Demolición">Colapsado / Demolición</option>
                        </select>
                    </div>
                </div>
                <div>
                    <label class="block text-[10px] font-bold uppercase text-slate-300 mb-1">Estado de Ayuda / Albergue</label>
                    <select id="afectado-albergue" class="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-3 py-2 text-xs">
                        <option value="Pendiente de Asistencia">Pendiente de Asistencia</option>
                        <option value="En Albergue Temporal Plaza Cívica">En Albergue Temporal Plaza Cívica</option>
                        <option value="Subsidio de Arrendamiento Asignado">Subsidio de Arrendamiento Asignado</option>
                        <option value="Ayuda Humanitaria Entregada">Ayuda Humanitaria Entregada</option>
                    </select>
                </div>
                <div class="flex justify-end gap-2 pt-3 border-t border-slate-800">
                    <button type="button" onclick="cerrarModalAfectado()" class="bg-slate-900 text-slate-300 px-4 py-2 rounded-xl uppercase font-bold cursor-pointer">Cancelar</button>
                    <button type="submit" class="bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2 rounded-xl uppercase font-bold cursor-pointer">Guardar en Servidor</button>
                </div>
            </form>
        </div>
    </div>

    <div id="pdf-export-template" class="hidden bg-white text-slate-900 p-6 font-sans max-w-4xl mx-auto border-2 border-slate-400 space-y-3.5 text-[9.5px]">
        <div class="border-2 border-slate-900 p-2 flex justify-between items-center bg-slate-50 mb-3">
            <div>
                <h4 class="text-[8.5px] font-bold tracking-widest uppercase text-slate-500">REPÚBLICA DE COLOMBIA • CLOUD CATASTRO PEREIRA</h4>
                <h2 class="text-base font-black text-slate-900 font-display uppercase">INFORME TÉCNICO • EVALUACIÓN POST-TERREMOTO</h2>
            </div>
        </div>
        <p><strong>Propietario:</strong> <span id="pdf-propietario">N/A</span></p>
        <p><strong>Estado Sismo 2026:</strong> <span id="pdf-estado-sismo">N/A</span></p>
        <p><strong>Observaciones:</strong> <span id="pdf-observaciones">N/A</span></p>
    </div>

    <script>
        let currentApprentice = { name: "Ing. Steven Barrera", ficha: "2671890" };
        let loteActualSeleccionado = null;
        let prediosCache = [];
        let afectadosCache = [];

        function cambiarModulo(mod) {
            ['catastro', 'topografia-general', 'afectados', 'google-earth', 'colombia-mapas'].forEach(m => {
                const el = document.getElementById(`modulo-${m}`);
                const btn = document.getElementById(`btn-tab-${m}`);
                if (el) el.classList.add('hidden');
                if (btn) btn.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition text-slate-300 hover:text-white cursor-pointer";
            });
            const targetMod = document.getElementById(`modulo-${mod}`);
            const targetBtn = document.getElementById(`btn-tab-${mod}`);
            if (targetMod) targetMod.classList.remove('hidden');
            if (targetBtn) targetBtn.className = "px-3 py-1.5 rounded-lg text-xs font-bold transition bg-emerald-600 text-white shadow cursor-pointer";
            if (mod === 'afectados') cargarAfectadosAPI();
            if (mod === 'google-earth') setTimeout(renderizarPoligonoLoteCanvas, 50);
        }

        async function iniciarSesion(event) {
            if (event) event.preventDefault();
            const nameInput = document.getElementById('apprentice-name');
            const fichaInput = document.getElementById('apprentice-ficha');
            currentApprentice.name = nameInput ? nameInput.value.trim() : "Ing. Steven Barrera";
            currentApprentice.ficha = fichaInput ? fichaInput.value.trim() : "2671890";
            document.getElementById('header-apprentice').textContent = `Operador: ${currentApprentice.name} • Ficha: ${currentApprentice.ficha}`;
            document.getElementById('login-screen').classList.add('hidden');
            await actualizarFichasMapaAPI();
            actualizarProgresoGeneral();
            mostrarNotificacion("Conectado", "Sistema sincronizado con el servidor Cloud.", "success");
        }

        function accesoDirecto() { iniciarSesion(null); }
        function cerrarSesion() { document.getElementById('login-screen').classList.remove('hidden'); }

        function mostrarNotificacion(titulo, mensaje) {
            const container = document.getElementById('toast-container');
            if (!container) return;
            const toast = document.createElement('div');
            toast.className = `p-4 rounded-xl border shadow-xl flex gap-3 items-start backdrop-blur-md transition-all duration-300 bg-emerald-950/90 border-emerald-500 text-emerald-200`;
            toast.innerHTML = `<div class="flex-grow"><h4 class="text-xs font-bold uppercase text-white">${titulo}</h4><p class="text-xs opacity-90">${mensaje}</p></div>`;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 4000);
        }

        function filtrarPredios(q) { actualizarFichasMapaAPI(q.toLowerCase()); }

        async function actualizarFichasMapaAPI(filtro = '') {
            try {
                const res = await fetch('/api/v1/predios');
                prediosCache = await res.json();
                const grid = document.getElementById('predios-grid');
                if(!grid) return;
                grid.innerHTML = '';
                prediosCache.forEach(predio => {
                    if (filtro && !predio.propietario.toLowerCase().includes(filtro) && !predio.id.toString().includes(filtro)) return;
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.onclick = () => seleccionarPredioAPI(predio.id);
                    btn.className = `p-4 rounded-2xl border transition-all flex flex-col items-center justify-center cursor-pointer ${predio.completado ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300' : 'bg-slate-950/60 border-slate-700/80 text-slate-300'}`;
                    btn.innerHTML = `<span class="text-[10px] opacity-70">LOTE</span><span class="text-lg font-black">${predio.id}</span>`;
                    grid.appendChild(btn);
                });
                actualizarProgresoGeneral();
            } catch(e) { console.error(e); }
        }

        function actualizarProgresoGeneral() {
            const comps = prediosCache.filter(p => p.completado).length;
            const pct = prediosCache.length ? Math.round((comps / prediosCache.length) * 100) : 0;
            const fill = document.getElementById('progress-bar-fill');
            const percent = document.getElementById('progress-percent');
            if(fill) fill.style.width = `${pct}%`;
            if(percent) percent.textContent = `${pct}%`;
        }

        async function seleccionarPredioAPI(id) {
            try {
                const res = await fetch(`/api/v1/predios/${id}`);
                const p = await res.json();
                document.getElementById('no-selection-message').classList.add('hidden');
                const cont = document.getElementById('ficha-container');
                cont.classList.remove('hidden'); cont.classList.add('flex');
                document.getElementById('form-predio-id').value = p.id;
                document.getElementById('ficha-subtitle').textContent = `PREDIO N° ${p.id} - PEREIRA`;
                document.getElementById('form-propietario').value = p.propietario;
                document.getElementById('form-documento').value = p.documento;
                document.getElementById('form-numero-predial').value = p.numeroPredial;
                document.getElementById('form-matricula').value = p.matricula;
                document.getElementById('form-estado-sismo').value = p.estadoSismo;
                document.getElementById('form-observaciones').value = p.observaciones;
            } catch(e) { console.error(e); }
        }

        async function guardarPredioAPI(e) {
            e.preventDefault();
            const id = parseInt(document.getElementById('form-predio-id').value);
            const payload = {
                propietario: document.getElementById('form-propietario').value,
                estadoSismo: document.getElementById('form-estado-sismo').value,
                observaciones: document.getElementById('form-observaciones').value
            };
            const res = await fetch(`/api/v1/predios/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if(res.ok) {
                await actualizarFichasMapaAPI();
                mostrarNotificacion("Guardado", `Ficha del Lote ${id} actualizada en la nube.`, "success");
            }
        }

        async function cargarAfectadosAPI(filtro = '') {
            try {
                const res = await fetch('/api/v1/afectados');
                afectadosCache = await res.json();
                const tbody = document.getElementById('tabla-afectados-body');
                if(!tbody) return;
                tbody.innerHTML = '';
                const filtrados = afectadosCache.filter(a => a.nombre.toLowerCase().includes(filtro) || a.cedula.includes(filtro));
                document.getElementById('contador-afectados').textContent = `Total Registros: ${filtrados.length}`;
                filtrados.forEach((af) => {
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-slate-900/50 transition';
                    tr.innerHTML = `
                        <td class="py-3 px-4 font-mono text-cyan-300">${af.cedula}</td>
                        <td class="py-3 px-4 font-bold text-white">${af.nombre}</td>
                        <td class="py-3 px-4">Lote N° ${af.lote}</td>
                        <td class="py-3 px-4 font-bold text-emerald-400">${af.area}</td>
                        <td class="py-3 px-4 text-xs font-mono text-slate-300">${af.lat}, ${af.lon}</td>
                        <td class="py-3 px-4 text-amber-400">${af.danio}</td>
                        <td class="py-3 px-4 text-center flex justify-center gap-1.5">
                            <button onclick="verEnGoogleEarth(${af.lote}, '${af.lat}', '${af.lon}', '${af.area}', '${af.nombre}', '${af.danio}')" class="bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700 px-3 py-1 rounded-lg text-[10px] uppercase font-bold cursor-pointer flex items-center gap-1 shadow"><i class="fa-solid fa-earth-americas"></i> Polígono</button>
                            <button onclick="editarAfectadoAPI('${af.id}')" class="bg-cyan-950/80 hover:bg-cyan-900 text-cyan-300 border border-cyan-800 px-2.5 py-1 rounded-lg text-[10px] font-bold cursor-pointer"><i class="fa-solid fa-pen"></i></button>
                            <button onclick="eliminarAfectadoAPI('${af.id}')" class="bg-rose-950/80 hover:bg-rose-900 text-rose-300 border border-rose-800 px-2.5 py-1 rounded-lg text-[10px] font-bold cursor-pointer"><i class="fa-solid fa-trash"></i></button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(e) { console.error(e); }
        }

        function verEnGoogleEarth(loteId, lat, lon, area, nombre, danio) {
            loteActualSeleccionado = { loteId, lat, lon, area, nombre, danio };
            cambiarModulo('google-earth');
            document.getElementById('earth-badge-lote').textContent = `Lote N° ${loteId} (Área: ${area})`;
            document.getElementById('earth-subtitle').textContent = `Coordenadas: Lat ${lat}, Lon ${lon} — Polígono Post-Terremoto.`;
            document.getElementById('btn-abrir-earth-externo').href = `https://earth.google.com/web/@${lat},${lon},500a,800d,35y,0h,0t,0r`;
            document.getElementById('panel-prop').textContent = nombre;
            document.getElementById('panel-area').textContent = area;
            document.getElementById('panel-coords').textContent = `Lat: ${lat}, Lon: ${lon}`;
            document.getElementById('panel-danio').textContent = danio;
            renderizarPoligonoLoteCanvas();
        }

        function renderizarPoligonoLoteCanvas() {
            const canvas = document.getElementById('canvas-poligono-lote');
            if(!canvas) return;
            const ctx = canvas.getContext('2d');
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight || 450;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0b1329'; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = 'rgba(34, 211, 238, 0.1)'; ctx.lineWidth = 1;
            for(let x=0; x<canvas.width; x+=30) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }
            for(let y=0; y<canvas.height; y+=30) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }
            if (!loteActualSeleccionado) return;
            const cx = canvas.width / 2, cy = canvas.height / 2;
            const pts = [{x: cx - 80, y: cy - 60}, {x: cx + 90, y: cy - 70}, {x: cx + 100, y: cy + 70}, {x: cx - 70, y: cy + 80}];
            const isColapsado = loteActualSeleccionado.danio.includes('Colapsado');
            ctx.fillStyle = isColapsado ? 'rgba(239, 68, 68, 0.4)' : 'rgba(16, 185, 129, 0.4)';
            ctx.strokeStyle = isColapsado ? '#ef4444' : '#10b981';
            ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y);
            pts.forEach((p, idx) => { if(idx>0) ctx.lineTo(p.x, p.y); });
            ctx.closePath(); ctx.fill(); ctx.stroke();
        }

        function filtrarAfectados(q) { cargarAfectadosAPI(q.toLowerCase()); }
        function abrirModalNuevoAfectado() {
            document.getElementById('modal-titulo-afectado').textContent = "Registrar Damnificado Nube";
            document.getElementById('afectado-id').value = "";
            document.getElementById('afectado-cedula').value = "";
            document.getElementById('afectado-nombre').value = "";
            document.getElementById('afectado-lote').value = "1";
            document.getElementById('modal-afectado').classList.remove('hidden');
        }
        function cerrarModalAfectado() { document.getElementById('modal-afectado').classList.add('hidden'); }

        async function guardarAfectadoAPI(e) {
            e.preventDefault();
            const id = document.getElementById('afectado-id').value;
            const loteNum = parseInt(document.getElementById('afectado-lote').value);
            const payload = {
                id: id || null,
                cedula: document.getElementById('afectado-cedula').value,
                nombre: document.getElementById('afectado-nombre').value,
                lote: loteNum,
                area: `${(120 + (loteNum * 15.5)).toFixed(2)} m²`,
                lat: `${(4.8133 + (loteNum * 0.0012)).toFixed(5)}`,
                lon: `${(-75.6961 - (loteNum * 0.0011)).toFixed(5)}`,
                danio: document.getElementById('afectado-danio').value,
                albergue: document.getElementById('afectado-albergue').value
            };
            await fetch('/api/v1/afectados', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
            cerrarModalAfectado();
            await cargarAfectadosAPI();
            mostrarNotificacion("Guardado", "Registro sincronizado en la nube.", "success");
        }

        async function editarAfectadoAPI(id) {
            const af = afectadosCache.find(a => a.id === id);
            if(!af) return;
            document.getElementById('modal-titulo-afectado').textContent = "Editar Damnificado";
            document.getElementById('afectado-id').value = af.id;
            document.getElementById('afectado-cedula').value = af.cedula;
            document.getElementById('afectado-nombre').value = af.nombre;
            document.getElementById('afectado-lote').value = af.lote;
            document.getElementById('afectado-danio').value = af.danio;
            document.getElementById('afectado-albergue').value = af.albergue;
            document.getElementById('modal-afectado').classList.remove('hidden');
        }

        async function eliminarAfectadoAPI(id) {
            if(confirm("¿Desea eliminar este registro del servidor cloud?")) {
                await fetch(`/api/v1/afectados/${id}`, { method: 'DELETE' });
                await cargarAfectadosAPI();
                mostrarNotificacion("Eliminado", "Registro removido del servidor.", "warning");
            }
        }

        async function exportarFichaPDF() {
            const id = parseInt(document.getElementById('form-predio-id').value);
            if(!id) return;
            const res = await fetch(`/api/v1/predios/${id}`);
            const p = await res.json();
            document.getElementById('pdf-propietario').textContent = p.propietario;
            document.getElementById('pdf-estado-sismo').textContent = p.estadoSismo;
            document.getElementById('pdf-observaciones').textContent = p.observaciones;
            const el = document.getElementById('pdf-export-template');
            el.classList.remove('hidden');
            html2pdf().from(el).save().then(() => el.classList.add('hidden'));
        }
    </script>
</body>
</html>