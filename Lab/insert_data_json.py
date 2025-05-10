import json


def modificar_json(ruta_archivo):
    # Valor que reemplazará los campos especificados
    VAR = "XXXXXXXXXXXXXXX"

    # Cargar el archivo JSON
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no fue encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo '{ruta_archivo}' no tiene un formato JSON válido.")
        return

    # Modificar los valores específicos según la estructura real del JSON
    try:
        # 1) "numFactura": VAR (Linea 3)
        datos["numFactura"] = VAR

        # 2) "tipoDocumentoIdentificacion": VAR (Linea 8)
        datos["usuarios"][0]["tipoDocumentoIdentificacion"] = VAR

        # 3) "numDocumentoIdentificacion": VAR (Linea 9)
        datos["usuarios"][0]["numDocumentoIdentificacion"] = VAR

        # 4) "fechaNacimiento": VAR (Linea 11)
        datos["usuarios"][0]["fechaNacimiento"] = VAR

        # 5) "codSexo": VAR (Linea 12)
        datos["usuarios"][0]["codSexo"] = VAR

        # 6) "fechaInicioAtencion": VAR (Linea 23)
        datos["usuarios"][0]["servicios"]["procedimientos"][0]["fechaInicioAtencion"] = VAR

        # 7) "codProcedimiento": VAR (Linea 26)
        datos["usuarios"][0]["servicios"]["procedimientos"][0]["codProcedimiento"] = VAR

        # 8) "vrServicio": VAR (Linea 37)
        datos["usuarios"][0]["servicios"]["procedimientos"][0]["vrServicio"] = VAR

    except KeyError as e:
        print(f"Error: No se encontró la clave {e} en el archivo JSON.")
        return

    # Guardar los cambios en el archivo original
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
        print(f"Archivo '{ruta_archivo}' modificado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    ruta_json = input("Ingrese la ruta al archivo JSON: ")
    modificar_json(ruta_json)
