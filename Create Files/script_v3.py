import pandas as pd
import os
from tabulate import tabulate

FILENAME = "data.xlsx"
SHEETNAME = "informe_operacion_1745627271"

def normalize_spaces(s: str) -> str:
    """Reduce cualquier secuencia de espacios a uno solo y quita espacios al inicio y final."""
    return " ".join(str(s).split()).strip()

def buscar_paciente(nombre: str, ruta_excel: str, hoja: str):
    # Verifica que el archivo exista
    if not os.path.isfile(ruta_excel):
        print(f"El archivo no se encontró: {ruta_excel}")
        return

    # Lee la hoja
    try:
        df = pd.read_excel(ruta_excel, sheet_name=hoja)
    except Exception as e:
        print(f"Error al leer el Excel: {e}")
        return

    # Normaliza el nombre de búsqueda
    nombre_norm = normalize_spaces(nombre).lower()
    print(f"Nombre normalizado a buscar: {nombre_norm}")  # Debug: Muestra el nombre que estamos buscando

    # Normaliza la columna 'paciente' en el DataFrame
    df['__paciente_norm'] = (
        df['paciente']
        .astype(str)
        .apply(normalize_spaces)
        .str.lower()
    )

    # Mostrar algunos nombres normalizados para depuración
    print("\nNombres de pacientes en el Excel (normalizados):")
    for paciente in df['__paciente_norm'].head(10):  # Solo muestra los primeros 10
        print(f"- {paciente}")

    # Filtra registros con coincidencias parciales
    resultados = df[df['__paciente_norm'].str.contains(nombre_norm, na=False)]

    if resultados.empty:
        print(f"No se encontró ningún registro para «{nombre}».")
    else:
        # Información fija: solo del primer registro
        primero = resultados.iloc[0]
        info = [
            ["Paciente", normalize_spaces(primero['paciente'])],
            ["Documento", f"{normalize_spaces(primero['tipo_documento'])} {normalize_spaces(primero['cedula'])}"],
            ["Genero", normalize_spaces(primero['genero'])],
            ["Edad", primero['edad']],
            ["Fecha Nacimiento", primero['fecha_nacimiento']],
        ]
        # Tabla minimalista para la info fija
        print("\n ***** Datos del paciente: *****")
        print(tabulate(info, tablefmt="grid", stralign="left"))
  
        # Ahora la tabla de citas
        citas = resultados[['fecha', 'estado_cita', 'codigo_servicio', 'servicio']].copy()
        citas.columns = ['Fecha', 'Estado', 'Codigo Servicio', 'Servicio']
        print("\n ***** Citas del paciente: *****")
        print(tabulate(citas, headers="keys", tablefmt="psql", showindex=False))

    # Limpia columna temporal
    df.drop(columns="__paciente_norm", inplace=True)

if __name__ == "__main__":
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, FILENAME)
    nombre_paciente = input("Nombre del paciente a buscar: ")
    buscar_paciente(nombre_paciente, ruta, SHEETNAME)
