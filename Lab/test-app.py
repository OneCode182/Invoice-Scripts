import os


def buscar_archivos_por_documento(directorio_base, documento_paciente):
    # Recorremos todos los directorios dentro del directorio base
    for directorio in os.listdir(directorio_base):
        ruta_directorio = os.path.join(directorio_base, directorio)

        # Verificamos si es un directorio
        if os.path.isdir(ruta_directorio):
            # Extraemos el número de documento del nombre del directorio
            partes = directorio.split('-')
            if len(partes) >= 4:
                numero_documento = partes[2]  # El tercer elemento es el número de documento

                # Si el número de documento coincide con el proporcionado, retornamos las rutas
                if numero_documento == documento_paciente:
                    ruta_xml = os.path.join(ruta_directorio, f"{partes[1]}.xml")
                    ruta_json = os.path.join(ruta_directorio, f"{partes[1]}.json")

                    # Verificamos si los archivos existen
                    if os.path.exists(ruta_xml) and os.path.exists(ruta_json):
                        return {
                            'directorio': ruta_directorio,
                            'xml': ruta_xml,
                            'json': ruta_json
                        }
    # Si no encontramos nada
    return None


if __name__ == '__main__':
    # Ejemplo de uso
    directorio_base = r"C:\Users\Sergio Silva\Desktop\Invoice-Scripts\Test Facts"  # Aquí debes colocar la ruta de tu directorio base
    documento_paciente = '79956301'  # El documento del paciente que estamos buscando

    resultado = buscar_archivos_por_documento(directorio_base, documento_paciente)

    if resultado:
        print(f"Directorio: {resultado['directorio']}")
        print(f"Archivo XML: {resultado['xml']}")
        print(f"Archivo JSON: {resultado['json']}")
    else:
        print("No se encontraron archivos para el documento proporcionado.")
