import pandas as pd
import sys
from datetime import datetime



class ExcelData:
    def __init__(self, ruta_excel):
        self.ruta_excel = ruta_excel
        self.data = self.cargar_excel()


    def setLog(self, log):
        self.log = log

    def getData(self):
        return self.data

    def cargar_excel(self):
        try:
            print(f"Intentando abrir el archivo: {self.ruta_excel}")
            df = pd.read_excel(self.ruta_excel)
            print(f"Archivo cargado exitosamente. Filas: {len(df)}")
            return df

        except FileNotFoundError:
            print(f"Error: El archivo '{self.ruta_excel}' no fue encontrado.")
            return []


    def get_data_by_doc(self, doc):
        registros = self.buscar_paciente_por_cedula(doc)
        primer_registro = registros[0]

        return {
            "tipoDoc": primer_registro['tipo_documento'],
            "numDoc": primer_registro['numero_documento'],
            "fechaNac": primer_registro['fecha_nacimiento'],
            "genero": primer_registro['genero']
        }

    def formato_fecha(self, fecha):
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



    def buscar_paciente_por_cedula(self, cedula):
        """
        Busca un paciente en un archivo Excel por su número de cédula y devuelve todos los registros encontrados.

        Args:
            ruta_archivo (str): Ruta al archivo Excel (.xlsx)
            cedula (str): Número de cédula del paciente a buscar

        Returns:
            list: Lista de diccionarios con la información de cada registro del paciente o lista vacía si no se encuentra
        """
        try:
            # Convertir cedula a string para asegurar la comparación correcta
            self.data['cedula'] = self.data['cedula'].astype(str)
            cedula = str(cedula)

            # Buscar todas las filas que coincidan con la cédula
            resultados = self.data[self.data['cedula'] == cedula]

            if len(resultados) == 0:
                self.log.log_message(f"No se encontró ningún paciente con cédula: {cedula}")
                return []

            self.log.log_message(f"Se encontraron {len(resultados)} registros para el paciente con cédula: {cedula}")

            # Extraer la información solicitada para cada registro
            registros_paciente = []
            for idx, paciente in resultados.iterrows():
                info_paciente = {
                    'paciente': paciente['paciente'],
                    'tipo_documento': paciente['tipo_documento'],
                    'numero_documento': paciente['cedula'],
                    'fecha_nacimiento': self.formato_fecha(paciente['fecha_nacimiento']),
                    'genero': paciente['genero'],
                    'fecha': self.formato_fecha(paciente['fecha']),
                    'codigo_cups': paciente['cups'],
                    # Incluir campos adicionales que pueden ser útiles para diferenciar registros
                    'estado_cita': paciente['estado_cita'],
                    'servicio': paciente['servicio'],
                    'codigo_diagnostico': paciente.get('codigo_diagnostico', ''),
                    'nombre_diagnostico': paciente.get('nombre_diagnostico', '')
                }
                registros_paciente.append(info_paciente)

            return registros_paciente

        except Exception as e:
            self.log.log_message(f"Error al procesar el archivo: {e}")
            import traceback
            traceback.print_exc()
            return []

    def mostrar_resultados(self, registros_paciente):
        """
        Muestra todos los registros encontrados para un paciente de forma legible
        """
        if not registros_paciente:
            self.log.log_message("No se encontraron registros para el paciente.")
            return

        # Imprimir información general (de un solo registro ya que es la misma para todos)
        primer_registro = registros_paciente[0]
        self.log.log_message("\n=== INFORMACIÓN GENERAL DEL PACIENTE ===")
        self.log.log_message(f"Nombre: {primer_registro['paciente']}")
        self.log.log_message(f"Tipo de Documento: {primer_registro['tipo_documento']}")
        self.log.log_message(f"Número de Documento: {primer_registro['numero_documento']}")
        self.log.log_message(f"Fecha Nacimiento: {primer_registro['fecha_nacimiento']}")
        self.log.log_message(f"Género: {primer_registro['genero']}")

        # Imprimir cada registro con su información específica
        self.log.log_message(f"\n=== REGISTROS ENCONTRADOS ({len(registros_paciente)}) ===")
        for i, registro in enumerate(registros_paciente, 1):
            self.log.log_message(f"\nRegistro #{i}:")
            self.log.log_message(f"1) Tipo de Documento: {registro['tipo_documento']}")
            self.log.log_message(f"2) Número de Documento: {registro['numero_documento']}")
            self.log.log_message(f"3) Fecha Nacimiento: {registro['fecha_nacimiento']}")
            self.log.log_message(f"4) Género: {registro['genero']}")
            self.log.log_message(f"5) Fecha: {registro['fecha']}")
            self.log.log_message(f"6) Código CUPS: {registro['codigo_cups']}")
            self.log.log_message(f"   Estado Cita: {registro['estado_cita']}")
            self.log.log_message(f"   Servicio: {registro['servicio']}")
            if registro['codigo_diagnostico'] or registro['nombre_diagnostico']:
                self.log.log_message(f"   Diagnóstico: {registro['codigo_diagnostico']} - {registro['nombre_diagnostico']}")



