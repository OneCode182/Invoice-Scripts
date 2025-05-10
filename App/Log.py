import os
import logging


class Log:
    def __init__(self, dir_log, file_log):
        # Definir el directorio y archivo de log
        self.directorio_log = dir_log  # Cambia esta ruta según tu entorno
        self.nombre_archivo_log = f"{file_log}.txt"
        self.configurar_log()

    def configurar_log(self):
        """
        Configura el log para que se guarde en un archivo de texto.
        Si el directorio no existe, lo crea. El archivo se sobrescribe si ya existe.
        """
        # Crear el directorio si no existe
        if not os.path.exists(self.directorio_log):
            os.makedirs(self.directorio_log)

        # Configurar el logger
        log_path = os.path.join(self.directorio_log, self.nombre_archivo_log)

        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,  # Puedes cambiar el nivel según tus necesidades
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='w'  # 'w' sobrescribe el archivo si ya existe
        )

        # Mensaje de inicio
        logging.info("Iniciando el registro de la aplicación.")

    def log_message(self, mensaje):
        """
        Escribe un mensaje en el archivo de log.
        """
        logging.info(mensaje)

    def log_error(self, error):
        """
        Escribe un error en el archivo de log.
        """
        logging.error(error)

    def log_warning(self, warning):
        """
        Escribe una advertencia en el archivo de log.
        """
        logging.warning(warning)

    def print_with_log(self, mensaje):
        """
        Imprime el mensaje y también lo escribe en el archivo de log.
        """
        print(mensaje)
        self.log_message(mensaje)




"""


    def buscar_valtolfac(self):
        if not self.lineas_xml:
            error_message = "El archivo XML no está cargado."
            self.log_error(error_message)
            print(error_message)
            return None

        # Realizamos la búsqueda y extracción como antes
        patron = r"ValTolFac:\s*([0-9]+(?:\.[0-9]+)?)"
        for linea in self.lineas_xml:
            match = re.search(patron, linea)
            if match:
                valor = match.group(1)
                valor_entero = int(float(valor))  # Convertirlo a entero
                self.log_message(f"Valor ValTolFac encontrado: {valor_entero}")
                return valor_entero

        error_message = "No se encontró 'ValTolFac' en el archivo XML."
        self.log_error(error_message)
        print(error_message)
        return None

"""


