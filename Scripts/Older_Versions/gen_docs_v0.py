import re
import shutil
from pathlib import Path

# —————— CONFIGURACIÓN ——————
# Ajusta estas rutas según tu entorno:
CRDOWNLOAD_DIR = Path(r"C:\Users\Sergio Silva\Desktop\CRDOWNLOADS")
JSON_SOURCE_PATH = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\template.json")
MASTER_OUTPUT_DIR = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\Docs")
# —————————————————————————

def extract_id(filename: str) -> str:
    """Extrae el ID numérico del nombre '... <ID>.crdownload'."""
    m = re.search(r'(\d+)\.crdownload$', filename)
    return m.group(1) if m else None

def extract_fv_value(text: str) -> str:
    """Busca el valor FV dentro de <cbc:ParentDocumentID>...</cbc:ParentDocumentID>."""
    m = re.search(r'<cbc:ParentDocumentID>\s*([^<\s]+)\s*</cbc:ParentDocumentID>', text)
    return m.group(1) if m else None

def process_crdownload(path: Path):
    id_ = extract_id(path.name)
    if not id_:
        print(f"– Saltando '{path.name}': no contiene un ID válido.")
        return

    # Lee todo el contenido
    content = path.read_text(encoding='utf-8', errors='ignore')

    fv = extract_fv_value(content)
    if not fv:
        print(f"– Saltando '{path.name}': no se encontró ParentDocumentID.")
        return

    # Crea carpeta de salida: MASTER_OUTPUT_DIR / "{ID}-{FV}"
    out_dir = MASTER_OUTPUT_DIR / f"{id_}-{fv}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Escribe el .xml con todo el contenido original
    xml_path = out_dir / f"{fv}.xml"
    xml_path.write_text(content, encoding='utf-8')

    # 2) Copia el JSON fuente renombrándolo
    json_dest = out_dir / f"{fv}.json"
    shutil.copy(JSON_SOURCE_PATH, json_dest)

    print(f"✓ Procesado '{path.name}' → carpeta '{out_dir.name}'")

def main():
    # Verifica que las rutas existan
    for p in (CRDOWNLOAD_DIR, JSON_SOURCE_PATH.parent, MASTER_OUTPUT_DIR):
        if not p.exists():
            print(f"ERROR: La ruta no existe: {p}")
            return

    # Procesa cada .crdownload
    for cr in CRDOWNLOAD_DIR.glob("*.crdownload"):
        process_crdownload(cr)

if __name__ == "__main__":
    main()
