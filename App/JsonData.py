import json


class JsonData:
    def __init__(self, ruta_json, excel_obj, log):
        self.ruta_json = ruta_json
        self.excel_obj = excel_obj
        self.datos_json = self.cargar_json()
        self.log = log




    def cargar_json(self):
        # Cargar el archivo JSON
        try:
            with open(self.ruta_json, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            self.log.log_message(f"Error: El archivo '{self.ruta_json}' no fue encontrado.")
            return None
        except json.JSONDecodeError:
            self.log.log_message(f"Error: El archivo '{self.ruta_json}' no tiene un formato JSON válido.")
            return None


    def guardar_json(self):
        # Guardar los cambios en el archivo original
        try:
            with open(self.ruta_json, 'w', encoding='utf-8') as archivo:
                json.dump(self.datos_json, archivo, indent=2, ensure_ascii=False)
            self.log.log_message(f"Archivo '{self.ruta_json}' modificado exitosamente.")
        except Exception as e:
            self.log.log_message(f"Error al guardar el archivo: {e}")



    def getNumFac(self):
        return self.datos_json["numFactura"]


    def modificar_json(self, data):

        # Modificar los valores específicos según la estructura real del JSON
        try:
            # 1) "numFactura": VAR (Linea 3)
            self.datos_json["numFactura"] = data["numFactura"]

            # 2) "tipoDocumentoIdentificacion": VAR (Linea 8)
            self.datos_json["usuarios"][0]["tipoDocumentoIdentificacion"] = data["tipoDoc"]

            # 3) "numDocumentoIdentificacion": VAR (Linea 9)
            self.datos_json["usuarios"][0]["numDocumentoIdentificacion"] = data["numDoc"]

            # 4) "fechaNacimiento": VAR (Linea 11)
            self.datos_json["usuarios"][0]["fechaNacimiento"] = data["fechaNac"]

            # 5) "codSexo": VAR (Linea 12)
            self.datos_json["usuarios"][0]["codSexo"] = data["genero"]

            # 6) "fechaInicioAtencion": VAR (Linea 23)
            self.datos_json["usuarios"][0]["servicios"]["procedimientos"][0]["fechaInicioAtencion"] = data["fechaIni"]

            # 7) "codProcedimiento": VAR (Linea 26)
            self.datos_json["usuarios"][0]["servicios"]["procedimientos"][0]["codProcedimiento"] = data["codProc"]

            # 8) "vrServicio": VAR (Linea 37)
            self.datos_json["usuarios"][0]["servicios"]["procedimientos"][0]["vrServicio"] = data["valorServ"]


        except KeyError as e:
            self.log.log_message(f"Error: No se encontró la clave {e} en el archivo JSON.")
            return


