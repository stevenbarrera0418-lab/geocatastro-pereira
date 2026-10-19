from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

@app.get("/", response_class=HTMLResponse)
def serve_home():
    html_file = BASE_DIR / "index.html"
    if html_file.exists():
        return html_file.read_text(encoding="utf-8")
    return "<h1>Error: Falta el archivo index.html en el repositorio</h1>"
