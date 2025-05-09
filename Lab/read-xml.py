#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LectorXML:
    """
    Clase para leer y realizar operaciones en archivos XML sin modificarlos.
    """

    def __init__(self, ruta_archivo):
        """
        Inicializa el lector con la ruta al archivo XML.

        Args:
            ruta_archivo (str): Ruta al archivo XML que se desea leer
        """
        self.ruta_archivo = ruta_archivo
        self.lineas = []
        self.contenido = ""
        self._cargar_archivo()

    def _cargar_archivo(self):
        """
        Carga el contenido del archivo XML en memoria.
        """
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.contenido = archivo.read()
                # Regresamos al principio del archivo y leemos línea por línea
                archivo.seek(0)
                self.lineas = archivo.readlines()
            print(f"Archivo '{self.ruta_archivo}' cargado correctamente.")
        except FileNotFoundError:
            print(f"Error: El archivo '{self.ruta_archivo}' no existe.")
        except PermissionError:
            print(f"Error: No tienes permisos para leer el archivo '{self.ruta_archivo}'.")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def buscar_palabra(self, palabra):
        """
        Busca una palabra en el contenido del archivo XML.

        Args:
            palabra (str): Palabra a buscar

        Returns:
            int: Número de ocurrencias de la palabra
            list: Lista de números de línea donde se encontró la palabra
        """
        if not self.contenido:
            return 0, []

        palabra = palabra.lower()
        ocurrencias = self.contenido.lower().count(palabra)

        # Encontrar en qué líneas aparece la palabra
        lineas_encontradas = []
        for i, linea in enumerate(self.lineas):
            if palabra in linea.lower():
                lineas_encontradas.append(i + 1)  # +1 para que empiece en 1 en lugar de 0

        return ocurrencias, lineas_encontradas

    def obtener_linea(self, numero_linea):
        """
        Obtiene una línea específica del archivo XML.

        Args:
            numero_linea (int): Número de línea a obtener (empezando en 1)

        Returns:
            str: Contenido de la línea solicitada o mensaje de error
        """
        if not self.lineas:
            return "El archivo no ha sido cargado o está vacío."

        if numero_linea < 1:
            return "El número de línea debe ser un número positivo."

        try:
            # Restamos 1 porque las listas en Python empiezan en 0
            return self.lineas[numero_linea - 1]
        except IndexError:
            return f"Error: El archivo solo tiene {len(self.lineas)} líneas."

    def obtener_total_lineas(self):
        """
        Devuelve el número total de líneas en el archivo.

        Returns:
            int: Número total de líneas
        """
        return len(self.lineas)


    def rango_xml(self, palabra_1, palabra_2):
        # Buscar rango de lineas por 2 palabras
        posicion = -1

        flag, pos_ini, pos_fin = False, 0, 0

        for i, linea in enumerate(self.lineas):
            if palabra_1 in linea:
                pos_ini = i

            elif palabra_2 in linea:
                pos_fin = i + 2
                flag = True
                break

        return flag, pos_ini, pos_fin

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de cómo usar la clase
    #ruta_xml = input("Introduce la ruta del archivo XML: ")
    ruta_xml = r"C:\Users\Sergio Silva\Desktop\Invoice-Scripts\Lab\file_2.xml"
    lector = LectorXML(ruta_xml)

    # Menú simple para interactuar con el lector
    while True:
        print("\n--- Operaciones disponibles ---")
        print("1. Buscar palabra en el documento")
        print("2. Obtener línea específica")
        print("3. Mostrar número total de líneas")
        print("4. Rango Lineas Ocurrencia")
        print("5. Salir")

        opcion = input("\nSelecciona una opción (1-4): ")

        if opcion == "1":
            palabra = input("Introduce la palabra a buscar: ")
            ocurrencias, lineas = lector.buscar_palabra(palabra)
            print(f"La palabra '{palabra}' aparece {ocurrencias} veces.")
            if lineas:
                print(f"Se encontró en las líneas: {lineas}")

        elif opcion == "2":
            try:
                num_linea = int(input("Introduce el número de línea: "))
                linea = lector.obtener_linea(num_linea)
                print(f"Línea {num_linea}: {linea}", end="")
            except ValueError:
                print("Por favor, introduce un número válido.")

        elif opcion == "3":
            total = lector.obtener_total_lineas()
            print(f"El archivo tiene {total} líneas.")

        elif opcion == "4":
            palabra_1 = "<cac:InvoicePeriod>"
            palabra_2 = "</cac:InvoicePeriod>"
            f, a, b = lector.rango_xml(palabra_1, palabra_2)
            print(f"LINEAS: INI -> {a + 1} | FIN -> {b - 1}")


        elif opcion == "5":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 4.")