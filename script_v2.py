import pandas as pd
import os
from tabulate import tabulate

FILENAME = "data.xlsx"
SHEETNAME = "informe_operacion_1745627271"

def normalize_spaces(s: str) -> str:
    """Reduce cualquier secuencia de espacios a uno solo y quita espacios al inicio y final."""
    return " ".join(str(s).split())

def buscar_paciente(nombre: str, ruta_excel: str, hoja: str):
    # Verifica que el archivo exista
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

    # Normaliza la columna 'paciente' para comparar
    df['__paciente_norm'] = (
        df['paciente']
        .astype(str)
        .apply(normalize_spaces)
        .str.lower()
    )

    # Filtra los registros del paciente
    resultados = df[df['__paciente_norm'] == nombre_norm]

    if resultados.empty:
        print(f"No se encontró ningún registro para «{nombre}».")
    else:
        # Toma el primer registro para la información fija
        primero = resultados.iloc[0]
        print(f"Paciente: {normalize_spaces(primero['paciente'])}")
        print(f"Documento: {normalize_spaces(primero['tipo_documento'])} {normalize_spaces(primero['cedula'])}")
        print(f"Genero: {normalize_spaces(primero['genero'])}")
        print(f"Edad: {primero['edad']}")
        print(f"Fecha Nacimiento: {primero['fecha_nacimiento']}\n")

        # Prepara la tabla de citas
        tabla = resultados[['fecha', 'estado_cita', 'codigo_servicio', 'servicio']].copy()
        tabla.columns = ['Fecha', 'Estado', 'Codigo Servicio', 'Servicio']
        print(tabulate(tabla, headers='keys', tablefmt='psql', showindex=False))

    # Limpia la columna temporal
    df.drop(columns="__paciente_norm", inplace=True)

if __name__ == "__main__":
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, FILENAME)
    nombre_paciente = input("Nombre del paciente a buscar: ")
    buscar_paciente(nombre_paciente, ruta, SHEETNAME)
