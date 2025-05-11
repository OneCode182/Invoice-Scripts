import os
import json
import pandas as pd
import re


def procesar_directorios_actualizar_excel(directorio_base, excel_path):
    """
    Procesa los directorios con archivos de facturación y actualiza un archivo Excel con la información extraída.

    Args:
        directorio_base (str): Ruta al directorio que contiene los subdirectorios a procesar
        excel_path (str): Ruta al archivo Excel que se actualizará
    """
    # Leer el archivo Excel
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return

    # Obtener la lista de subdirectorios
    try:
        subdirectorios = [d for d in os.listdir(directorio_base)
                          if os.path.isdir(os.path.join(directorio_base, d))]
    except Exception as e:
        print(f"Error al leer el directorio base: {e}")
        return

    i = 1
    for subdir in subdirectorios:
        try:
            # Extraer información del nombre del directorio
            partes = subdir.split('-')
            if len(partes) < 4:
                print(f" {i}) -X- Directorio '{subdir}' no tiene el formato esperado")
                i += 1
                continue

            # Extraer valores del nombre del directorio
            id_value = partes[0]
            fv_value = partes[1]
            doc_paciente = partes[2]
            nombre_paciente = '-'.join(partes[3:])

            # Ruta completa al subdirectorio
            ruta_subdir = os.path.join(directorio_base, subdir)

            # Buscar el archivo ResultadosMSPS
            archivos = os.listdir(ruta_subdir)
            archivo_resultados = None

            for archivo in archivos:
                if archivo.startswith("ResultadosMSPS"):
                    archivo_resultados = os.path.join(ruta_subdir, archivo)
                    break

            if not archivo_resultados:
                print(f" {i}) -X- Factura '{fv_value}' no tiene archivo ResultadosMSPS")
                i += 1
                continue

            # Leer y parsear el archivo de resultados
            with open(archivo_resultados, 'r', encoding='utf-8') as f:
                contenido = f.read()

            # Parsear el JSON del contenido
            try:
                datos = json.loads(contenido)

                # Extraer los valores necesarios
                codigo_unico_validacion = datos.get("CodigoUnicoValidacion", "")
                fecha_radicacion = datos.get("FechaRadicacion", "")
                proceso_id = datos.get("ProcesoId", "")

                # Buscar la fila correspondiente en el Excel y actualizar
                mask = df["FV_VALUE"] == fv_value

                if mask.any():
                    # Actualizar valores en el Excel
                    df.loc[mask, "Estado Subida"] = "SUBIDO"
                    df.loc[mask, "CUV Hash"] = codigo_unico_validacion
                    df.loc[mask, "Fecha Radicacion"] = fecha_radicacion
                    df.loc[mask, "Proceso ID"] = proceso_id

                    print(f" {i}) ✓ Factura '{fv_value}' insertada en Excel!")
                else:
                    print(f" {i}) -X- Factura '{fv_value}' no encontrada en Excel")

            except json.JSONDecodeError:
                print(f" {i}) -X- Factura '{fv_value}' tiene un archivo de resultados con formato JSON inválido")

        except Exception as e:
            print(
                f" {i}) -X- Factura '{fv_value if 'fv_value' in locals() else subdir}' no se pudo insertar en Excel: {str(e)}")

        i += 1

    # Guardar el Excel actualizado
    try:
        df.to_excel(excel_path, index=False)
        print(f"\nArchivo Excel actualizado correctamente en: {excel_path}")
    except Exception as e:
        print(f"\nError al guardar el archivo Excel: {e}")

# Ejemplo de uso:
# procesar_directorios_actualizar_excel("C:/ruta/al/directorio", "C:/ruta/al/excel.xlsx")