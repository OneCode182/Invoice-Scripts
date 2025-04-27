import os
import re
from pathlib import Path

# —————— CONFIGURACIÓN ——————
CRDOWNLOAD_DIR    = Path(r"C:\Users\Sergio Silva\Desktop\CRDOWNLOADS")
JSON_SOURCE_PATH  = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\template.json")
MASTER_OUTPUT_DIR = Path(r"C:\Users\Sergio Silva\Desktop\Script\Generate Docs\Docs")
# —————————————————————————

def normalize_spaces(s: str) -> str:
    """Reduce cualquier secuencia de espacios a uno solo y quita espacios al inicio y final."""
    return " ".join(str(s).split()).strip()

def buscar_directorio(fvvalue: str):
    """Busca el directorio que contiene el FVVALUE."""
    for folder in MASTER_OUTPUT_DIR.iterdir():
        if fvvalue in folder.name:
            return folder
    return None

def leer_nombre_paciente(directorio: Path):
    """Extrae el nombre del paciente desde el nombre del directorio."""
    # El nombre del paciente es parte del nombre del directorio
    # Ejemplo: "10073-FV3003-1234566-MARIA_ALEJANDRA_GARCIA_CIFUENTES"
    parts = directorio.name.split('-')
    if len(parts) >= 4:
        return parts[3].replace("_", " ")
    return "Nombre no encontrado"

def modificar_archivo_xml(xml_path: Path, opcion: int, fecha: str = None):
    """Modifica el archivo XML como texto plano según la opción seleccionada."""
    with open(xml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if opcion == 1:
        # PASO 1: Añadir información adicional después de <AdditionalInformation> con CODIGO_PRESTADOR
        additional_info = """
        <AdditionalInformation>
            <Name>MODALIDAD_PAGO</Name>
            <Value schemeID="04" schemeName="salud_modalidad_pago.gc">Pago por evento</Value>
        </AdditionalInformation>
        <AdditionalInformation>
            <Name>COBERTURA_PLAN_BENEFICIOS</Name>
            <Value schemeID="15" schemeName="salud_cobertura.gc">Particular</Value>
        </AdditionalInformation>
        """

        # Insertamos el bloque debajo de <AdditionalInformation>
        content = content.replace('<AdditionalInformation>', '<AdditionalInformation>' + additional_info)

    elif opcion == 2 and fecha:
        # PASO 2: Añadir periodo de factura con la fecha solicitada
        invoice_period = f"""
        <cac:InvoicePeriod>
            <cbc:StartDate>2025-{fecha}</cbc:StartDate>
            <cbc:StartTime>12:00:00</cbc:StartTime>
            <cbc:EndDate>2025-{fecha}</cbc:EndDate>
            <cbc:EndTime>12:00:00</cbc:EndTime>
        </cac:InvoicePeriod>
        """
        
        # Buscamos <cbc:LineCountNumeric> y agregamos el bloque de InvoicePeriod debajo
        content = content.replace('<cbc:LineCountNumeric>', '<cbc:LineCountNumeric>' + invoice_period)

    # Guardamos los cambios en el archivo XML (tratado como .txt)
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Paso 1: Pide el FVVALUE
    fvvalue = input("Introduce el FVVALUE: ").strip()
    directorio = buscar_directorio(fvvalue)

    if not directorio:
        print(f"No se encontró ningún directorio con FVVALUE: {fvvalue}")
        return

    # El XML debería estar dentro del directorio encontrado
    xml_path = directorio / f"{fvvalue}.xml"
    if not xml_path.exists():
        print(f"No se encontró el archivo XML para el FVVALUE: {fvvalue}")
        return

    # Leer el nombre del paciente desde el nombre del directorio
    nombre_paciente = leer_nombre_paciente(directorio)
    print(f"Nombre del paciente: {nombre_paciente}")

    # Menú de opciones
    print("\nSeleccione una opción para modificar el XML:")
    print("1) Añadir información adicional (PASO 1)")
    print("2) Añadir periodo de factura (PASO 2)")

    opcion = int(input("Selecciona 1 o 2: ").strip())

    if opcion == 1:
        # PASO 1: Añadir información adicional
        modificar_archivo_xml(xml_path, opcion)
        print(f"Se ha añadido la información adicional al archivo {xml_path.name}.")

    elif opcion == 2:
        # PASO 2: Añadir periodo de factura
        fecha = input("Introduce la fecha (formato YYYY-MM-DD): ").strip()
        modificar_archivo_xml(xml_path, opcion, fecha)
        print(f"Se ha añadido el periodo de factura al archivo {xml_path.name}.")
    
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
