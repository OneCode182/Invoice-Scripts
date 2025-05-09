import re
import shutil
import pandas as pd
from pathlib import Path



# —————— CONFIGURACIÓN ——————
CRDOWNLOAD_DIR    = Path(r"C:\Users\Sergio Silva\Desktop\CRDOWNLOADS")
JSON_SOURCE_PATH  = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\template.json")
MASTER_OUTPUT_DIR = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\Docs")
EXCEL_OUTPUT_PATH = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\output.xlsx")  # Ruta del archivo Excel



# —————————————————————————

def normalize_spaces(s: str) -> str:
    """Reduce cualquier secuencia de espacios a uno solo y quita espacios al inicio y final."""
    return " ".join(str(s).split())

def extract_id(filename: str) -> str:
    """Extrae el ID numérico del nombre '... <ID>.crdownload'."""
    m = re.search(r'(\d+)\.crdownload$', filename)
    return m.group(1) if m else None

def extract_fv_value(text: str) -> str:
    """Extrae el valor FV dentro de <cbc:ParentDocumentID>...</cbc:ParentDocumentID>."""
    m = re.search(r'<cbc:ParentDocumentID>\s*([^<]+)\s*</cbc:ParentDocumentID>', text)
    return m.group(1) if m else None

def extract_receiver_block(text: str) -> str:
    """Extrae el bloque <cac:ReceiverParty>...</cac:ReceiverParty>."""
    m = re.search(r'<cac:ReceiverParty>(.*?)</cac:ReceiverParty>', text, re.DOTALL)
    return m.group(1) if m else ""

def extract_registration_name(block: str) -> str:
    """Extrae el nombre dentro de <cbc:RegistrationName>...</cbc:RegistrationName> del bloque."""
    m = re.search(r'<cbc:RegistrationName>\s*([^<]+)\s*</cbc:RegistrationName>', block)
    return m.group(1) if m else None

def extract_company_id(block: str) -> str:
    """Extrae el documento dentro de <cbc:CompanyID ...>...</cbc:CompanyID> del bloque."""
    m = re.search(r'<cbc:CompanyID[^>]*>\s*([^<]+)\s*</cbc:CompanyID>', block)
    return m.group(1) if m else None

def clear_master_output():
    """Elimina todo el contenido de MASTER_OUTPUT_DIR sin borrar la carpeta principal."""
    for item in MASTER_OUTPUT_DIR.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except Exception as e:
            print(f"⚠️ Error al eliminar {item}: {e}")

def process_crdownload(path: Path, records: list):
    id_ = extract_id(path.name)
    if not id_:
        print(f"– Saltando '{path.name}': no contiene un ID válido.")
        return

    content = path.read_text(encoding='utf-8', errors='ignore')

    # Extrae FV y bloque de receiver
    fv = extract_fv_value(content)
    receiver_block = extract_receiver_block(content)

    if not fv:
        print(f"– Saltando '{path.name}': no se encontró ParentDocumentID.")
        return
    if not receiver_block:
        print(f"– Saltando '{path.name}': no se encontró bloque ReceiverParty.")
        return

    reg_name = extract_registration_name(receiver_block)
    company_id = extract_company_id(receiver_block)

    if not reg_name:
        print(f"– Saltando '{path.name}': no se encontró RegistrationName.")
        return
    if not company_id:
        print(f"– Saltando '{path.name}': no se encontró CompanyID.")
        return

    # Sanitiza nombre para carpeta
    name_clean = normalize_spaces(reg_name).replace(" ", "_")
    folder_name = f"{id_}-{fv}-{company_id}-{name_clean}"
    out_dir = MASTER_OUTPUT_DIR / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Escribe el .xml
    xml_path = out_dir / f"{fv}.xml"
    xml_path.write_text(content, encoding='utf-8')

    # 2) Copia el JSON
    json_dest = out_dir / f"{fv}.json"
    shutil.copy(JSON_SOURCE_PATH, json_dest)

    print(f"✓ Procesado '{path.name}' → carpeta '{folder_name}'")

    # Agregar el registro al listado para el Excel
    records.append({
        "ID": id_,
        "FV_VALUE": fv,
        "Doc Paciente": company_id,
        "Nombre Paciente": reg_name,
        "Estado Subida": "No se ha Subido",
        "Resultado Ministerio": "NN"
    })

def save_to_excel(records: list):
    """Guarda los registros en un archivo Excel."""
    df = pd.DataFrame(records)
    df.to_excel(EXCEL_OUTPUT_PATH, index=False)
    print(f"✓ Archivo Excel generado en: {EXCEL_OUTPUT_PATH}")

def main():
    # Verifica rutas
    for p in (CRDOWNLOAD_DIR, JSON_SOURCE_PATH.parent, MASTER_OUTPUT_DIR):
        if not p.exists():
            print(f"ERROR: La ruta no existe: {p}")
            return

    # Limpia ejecuciones previas
    clear_master_output()

    # Lista para almacenar los registros que luego se guardarán en Excel
    records = []

    # Procesa cada .crdownload
    for cr in CRDOWNLOAD_DIR.glob("*.crdownload"):
        process_crdownload(cr, records)

    # Guarda todos los registros en el archivo Excel
    if records:
        save_to_excel(records)

if __name__ == "__main__":
    main()
