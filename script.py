import pandas as pd
import os

FILENAME = "data.xlsx"
SHEETNAME = "informe_operacion_1745627271"

def normalize_spaces(s: str) -> str:
    """Reduce cualquier run de espacios a uno solo y quita espacios al inicio y final."""
    return " ".join(str(s).split())

def buscar_paciente(nombre: str, ruta_excel: str, hoja: str):
    # Comprueba que el archivo exista
    if not os.path.isfile(ruta_excel):
        print(f"El archivo no se encontró: {ruta_excel}")
        return

    # Lee la hoja indicada
    try:
        df = pd.read_excel(ruta_excel, sheet_name=hoja)
    except Exception as e:
        print(f"Error al leer el Excel: {e}")
        return

    # Normaliza el nombre de búsqueda
    nombre_norm = normalize_spaces(nombre).lower()

    # Crea columna temporal normalizada en el DataFrame
    df['__paciente_norm'] = (
        df['paciente']
        .astype(str)
        .apply(normalize_spaces)
        .str.lower()
    )

    # Filtra
    resultados = df[df['__paciente_norm'] == nombre_norm]

    # Muestra cada registro en formato de lista minimalista
    if resultados.empty:
        print(f"No se encontró ningún registro para «{nombre}».")
    else:
        for _, row in resultados.iterrows():
            print(f"Fecha: {row['fecha']}")
            print(f"Estado: {row['estado_cita']}")
            print(f"Documento: {row['cedula']}")
            print(f"Tipo Documento: {row['tipo_documento']}")
            print(f"Paciente: {normalize_spaces(row['paciente'])}")
            print(f"Edad: {row['edad']}")
            print(f"Fecha Nacimiento: {row['fecha_nacimiento']}")
            print(f"Genero: {row['genero']}")
            print(f"Codigo Servicio: {row['codigo_servicio']}")
            print(f"Servicio: {row['servicio']}")
            print()  # separador entre posibles múltiples registros

    # Elimina la columna temporal
    df.drop(columns="__paciente_norm", inplace=True)

if __name__ == "__main__":
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, FILENAME)
    nombre_paciente = input("Nombre del paciente a buscar: ")
    buscar_paciente(nombre_paciente, ruta, SHEETNAME)
