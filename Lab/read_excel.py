import pandas as pd
import sys
from datetime import datetime


def formato_fecha(fecha):
    """
    Convierte una fecha a formato YYYY-MM-DD independientemente de su tipo.
    Maneja fechas como datetime, string, o None.
    """
    if pd.isnull(fecha) or fecha is None:
        return None

    # Si ya es un string, intentamos parsearlo
    if isinstance(fecha, str):
        try:
            # Intentar parsear la fecha como string
            if ' ' in fecha:  # Si tiene formato datetime con hora
                fecha_obj = datetime.strptime(fecha.split(' ')[0], '%Y-%m-%d')
            else:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            return fecha_obj.strftime('%Y-%m-%d')
        except ValueError:
            # Si no se puede parsear, devolver como está
            return fecha

    # Si es un datetime u otro objeto con strftime
    try:
        return fecha.strftime('%Y-%m-%d')
    except AttributeError:
        # Si todo falla, convertir a string
        return str(fecha)


def buscar_paciente_por_cedula(ruta_archivo, cedula):
    """
    Busca un paciente en un archivo Excel por su número de cédula y devuelve todos los registros encontrados.

    Args:
        ruta_archivo (str): Ruta al archivo Excel (.xlsx)
        cedula (str): Número de cédula del paciente a buscar

    Returns:
        list: Lista de diccionarios con la información de cada registro del paciente o lista vacía si no se encuentra
    """
    try:
        # Cargar el archivo Excel
        print(f"Intentando abrir el archivo: {ruta_archivo}")
        df = pd.read_excel(ruta_archivo)
        print(f"Archivo cargado exitosamente. Filas: {len(df)}")

        # Convertir cedula a string para asegurar la comparación correcta
        df['cedula'] = df['cedula'].astype(str)
        cedula = str(cedula)

        # Buscar todas las filas que coincidan con la cédula
        resultados = df[df['cedula'] == cedula]

        if len(resultados) == 0:
            print(f"No se encontró ningún paciente con cédula: {cedula}")
            return []

        print(f"Se encontraron {len(resultados)} registros para el paciente con cédula: {cedula}")

        # Extraer la información solicitada para cada registro
        registros_paciente = []
        for idx, paciente in resultados.iterrows():
            info_paciente = {
                'paciente' : paciente['paciente'],
                'tipo_documento': paciente['tipo_documento'],
                'numero_documento': paciente['cedula'],
                'fecha_nacimiento': formato_fecha(paciente['fecha_nacimiento']),
                'genero': paciente['genero'],
                'fecha': formato_fecha(paciente['fecha']),
                'codigo_cups': paciente['cups'],
                # Incluir campos adicionales que pueden ser útiles para diferenciar registros
                'estado_cita': paciente['estado_cita'],
                'servicio': paciente['servicio'],
                'codigo_diagnostico': paciente.get('codigo_diagnostico', ''),
                'nombre_diagnostico': paciente.get('nombre_diagnostico', '')
            }
            registros_paciente.append(info_paciente)

        return registros_paciente

    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        import traceback
        traceback.print_exc()
        return []


def mostrar_resultados(registros_paciente):
    """
    Muestra todos los registros encontrados para un paciente de forma legible
    """
    if not registros_paciente:
        print("No se encontraron registros para el paciente.")
        return

    # Imprimir información general (de un solo registro ya que es la misma para todos)
    primer_registro = registros_paciente[0]
    print("\n=== INFORMACIÓN GENERAL DEL PACIENTE ===")
    print(f"Nombre: {primer_registro['paciente']}")
    print(f"Tipo de Documento: {primer_registro['tipo_documento']}")
    print(f"Número de Documento: {primer_registro['numero_documento']}")
    print(f"Fecha Nacimiento: {primer_registro['fecha_nacimiento']}")
    print(f"Género: {primer_registro['genero']}")

    # Imprimir cada registro con su información específica
    print(f"\n=== REGISTROS ENCONTRADOS ({len(registros_paciente)}) ===")
    for i, registro in enumerate(registros_paciente, 1):
        print(f"\nRegistro #{i}:")
        print(f"1) Tipo de Documento: {registro['tipo_documento']}")
        print(f"2) Número de Documento: {registro['numero_documento']}")
        print(f"3) Fecha Nacimiento: {registro['fecha_nacimiento']}")
        print(f"4) Género: {registro['genero']}")
        print(f"5) Fecha: {registro['fecha']}")
        print(f"6) Código CUPS: {registro['codigo_cups']}")
        print(f"   Estado Cita: {registro['estado_cita']}")
        print(f"   Servicio: {registro['servicio']}")
        if registro['codigo_diagnostico'] or registro['nombre_diagnostico']:
            print(f"   Diagnóstico: {registro['codigo_diagnostico']} - {registro['nombre_diagnostico']}")


if __name__ == "__main__":
    # Verificar si se proporcionaron argumentos de línea de comandos
    if len(sys.argv) > 2:
        ruta_archivo = sys.argv[1]
        cedula = sys.argv[2]
    else:
        # Si no hay argumentos, solicitar la información interactivamente
        ruta_archivo = r"C:\Users\Sergio Silva\Desktop\Pacientes atendidos 2 23-25.xlsx"
        cedula = input("Ingrese el número de cédula a buscar: ")

    # Buscar la información del paciente
    registros_paciente = buscar_paciente_por_cedula(ruta_archivo, cedula)

    # Mostrar los resultados
    mostrar_resultados(registros_paciente)


#ruta_archivo = r"C:\Users\Sergio Silva\Desktop\Pacientes atendidos 2 23-25.xlsx"