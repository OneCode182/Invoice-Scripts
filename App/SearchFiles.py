
import os


class SearchFiles:
    def __init__(self):
        pass

    def mostrar_docs_dirs(self, directorio_base):
        # Obtenemos una lista de todos los elementos en el directorio base
        elementos = os.listdir(directorio_base)

        # Filtramos solo los directorios
        directorios = [d for d in elementos if os.path.isdir(os.path.join(directorio_base, d))]

        # Mostramos la cantidad de directorios
        print(f"Cantidad de documentos de pacientes: {len(directorios)}")

        # Recorremos los directorios y extraemos el número de documento
        for directorio in directorios:
            partes = directorio.split('-')
            if len(partes) >= 4:
                numero_documento = partes[2]  # El número de documento está en la tercera posición
                print(f"DOC: {numero_documento}")


    def mostrar_nombre_dirs(self, directorio_base):
        # Obtenemos una lista de todos los elementos en el directorio base
        elementos = os.listdir(directorio_base)

        # Filtramos solo los directorios
        directorios = [d for d in elementos if os.path.isdir(os.path.join(directorio_base, d))]

        # Mostramos la cantidad de directorios
        print(f"Cantidad de directorios: {len(directorios)}")

        # Mostramos los nombres de los directorios
        for directorio in directorios:
            print(directorio)

    def buscar_por_fv(self, directorio_base, fv_value):
        # Recorremos todos los directorios dentro del directorio base
        for directorio in os.listdir(directorio_base):
            ruta_directorio = os.path.join(directorio_base, directorio)

            # Verificamos si es un directorio
            if os.path.isdir(ruta_directorio):
                # Extraemos el número de documento del nombre del directorio
                partes = directorio.split('-')
                if len(partes) >= 4:
                    fv_val_dir = partes[1]  # El tercer elemento es el número de documento

                    # Si el número de documento coincide con el proporcionado, retornamos las rutas
                    if fv_val_dir == fv_value:
                        ruta_xml = os.path.join(ruta_directorio, f"{partes[1]}.xml")
                        ruta_json = os.path.join(ruta_directorio, f"{partes[1]}.json")

                        # Verificamos si los archivos existen
                        if os.path.exists(ruta_xml) and os.path.exists(ruta_json):
                            return {
                                'directorio': ruta_directorio,
                                'xml': ruta_xml,
                                'json': ruta_json,
                                'FV_VALUE': partes[1],
                                'dir_pac':directorio,
                                'doc':partes[2]
                            }
        # Si no encontramos nada
        return None

    def mostrar_paths_archivos(self, resultado):
        if resultado:
            print(f"Directorio: {resultado['directorio']}")
            print(f"Archivo XML: {resultado['xml']}")
            print(f"Archivo JSON: {resultado['json']}")
        else:
            print("No se encontraron archivos para el documento proporcionado.")


"""

if __name__ == '__main__':
    # Ejemplo de uso

    documento_paciente = '79956301'  # El documento del paciente que estamos buscando

    resultado = buscar_archivos_por_documento(directorio_base, documento_paciente)

    if resultado:
        print(f"Directorio: {resultado['directorio']}")
        print(f"Archivo XML: {resultado['xml']}")
        print(f"Archivo JSON: {resultado['json']}")
    else:
        print("No se encontraron archivos para el documento proporcionado.")


"""