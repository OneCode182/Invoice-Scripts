#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class EditorXML:
    """
    Clase para realizar operaciones específicas de edición en archivos XML.
    """

    def __init__(self, ruta_archivo):
        """
        Inicializa el editor con la ruta al archivo XML.

        Args:
            ruta_archivo (str): Ruta al archivo XML que se desea editar
        """
        self.ruta_archivo = ruta_archivo
        self.lineas = []
        self._cargar_archivo()

    def _cargar_archivo(self):
        """
        Carga el contenido del archivo XML en memoria como líneas.
        """
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.lineas = archivo.readlines()
            print(f"Archivo '{self.ruta_archivo}' cargado correctamente.")
        except FileNotFoundError:
            print(f"Error: El archivo '{self.ruta_archivo}' no existe.")
            self.lineas = []
        except PermissionError:
            print(f"Error: No tienes permisos para leer el archivo '{self.ruta_archivo}'.")
            self.lineas = []
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            self.lineas = []

    def guardar_archivo(self, ruta_salida=None):
        """
        Guarda el contenido modificado en un archivo.

        Args:
            ruta_salida (str, optional): Ruta donde guardar el archivo modificado.
                                         Si es None, se sobrescribe el archivo original.

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        if not self.lineas:
            print("No hay contenido para guardar.")
            return False

        ruta_destino = ruta_salida if ruta_salida else self.ruta_archivo

        try:
            with open(ruta_destino, 'w', encoding='utf-8') as archivo:
                archivo.writelines(self.lineas)
            print(f"Archivo guardado correctamente en '{ruta_destino}'.")
            return True
        except PermissionError:
            print(f"Error: No tienes permisos para escribir en '{ruta_destino}'.")
            return False
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            return False

    def insertar_despues_codigo_prestador(self):
        """
        Inserta bloques de AdditionalInformation después del bloque CODIGO_PRESTADOR.

        Returns:
            bool: True si se realizó la inserción, False en caso contrario
        """
        if not self.lineas:
            print("El archivo no está cargado o está vacío.")
            return False

        # Buscar la posición del bloque CODIGO_PRESTADOR
        posicion = -1
        for i, linea in enumerate(self.lineas):
            if "<Name>CODIGO_PRESTADOR</Name>" in linea:
                # Buscar el cierre del bloque AdditionalInformation
                for j in range(i, len(self.lineas)):
                    if "</AdditionalInformation>" in self.lineas[j]:
                        posicion = j
                        break
                break

        if posicion == -1:
            print("No se encontró el bloque CODIGO_PRESTADOR.")
            return False

        # Bloques a insertar
        bloques_a_insertar = [
            '                <AdditionalInformation>\n',
            '                  <Name>MODALIDAD_PAGO</Name>\n',
            '                  <Value schemeID="04" schemeName="salud_modalidad_pago.gc">Pago por evento</Value>\n',
            '                </AdditionalInformation>\n',
            '                <AdditionalInformation>\n',
            '                  <Name>COBERTURA_PLAN_BENEFICIOS</Name>\n',
            '                  <Value schemeID="15" schemeName="salud_cobertura.gc">Particular</Value>    \n',
            '                </AdditionalInformation>\n'
        ]

        # Insertar después del cierre del bloque AdditionalInformation
        self.lineas = self.lineas[:posicion + 1] + bloques_a_insertar + self.lineas[posicion + 1:]
        print("Bloques insertados después de CODIGO_PRESTADOR.")
        return True

    def insertar_invoice_period(self, fecha="2025-04-01"):
        """
        Inserta el bloque InvoicePeriod después de la ocurrencia de LineCountNumeric.

        Args:
            fecha (str): Fecha a usar en el bloque InvoicePeriod

        Returns:
            bool: True si se realizó la inserción, False en caso contrario
        """
        if not self.lineas:
            print("El archivo no está cargado o está vacío.")
            return False

        # Buscar la posición de LineCountNumeric
        posicion = -1
        for i, linea in enumerate(self.lineas):
            if "<cbc:LineCountNumeric>1</cbc:LineCountNumeric>" in linea:
                posicion = i
                break

        if posicion == -1:
            print("No se encontró la línea <cbc:LineCountNumeric>1</cbc:LineCountNumeric>.")
            return False

        # Bloque a insertar con la fecha variable
        bloque_a_insertar = [
            '  <cac:InvoicePeriod>\n',
            f'    <cbc:StartDate>{fecha}</cbc:StartDate>\n',
            '    <cbc:StartTime>12:00:00</cbc:StartTime>\n',
            f'    <cbc:EndDate>{fecha}</cbc:EndDate>\n',
            '    <cbc:EndTime>12:00:00</cbc:EndTime>\n',
            '  </cac:InvoicePeriod>\n'
        ]

        # Insertar después de LineCountNumeric
        self.lineas = self.lineas[:posicion + 1] + bloque_a_insertar + self.lineas[posicion + 1:]
        print(f"Bloque InvoicePeriod insertado con fecha {fecha}.")
        return True


# Menú principal para ejecutar las operaciones
def menu_principal():
    print("\n=== EDITOR XML PARA INSERCIONES ESPECÍFICAS ===")
    #ruta_xml = input("Introduce la ruta del archivo XML: ")
    ruta_xml = r"C:\Users\Sergio Silva\Desktop\Invoice-Scripts\Lab\file.xml"


    editor = EditorXML(ruta_xml)
    if not editor.lineas:
        print("No se pudo cargar el archivo. Saliendo.")
        return

    VAR_2_DATE = "2025-04-01"  # Fecha por defecto

    while True:
        print("\n--- MENÚ DE OPERACIONES ---")
        print("1. Insertar bloques después de CODIGO_PRESTADOR")
        print("2. Insertar bloque InvoicePeriod después de LineCountNumeric")
        print("3. Cambiar la fecha para InvoicePeriod (actual:", VAR_2_DATE, ")")
        print("4. Guardar cambios")
        print("5. Guardar como...")
        print("6. Salir")

        opcion = input("\nSelecciona una opción (1-6): ")

        if opcion == "1":
            editor.insertar_despues_codigo_prestador()

        elif opcion == "2":
            editor.insertar_invoice_period(VAR_2_DATE)

        elif opcion == "3":
            nueva_fecha = input("Introduce la nueva fecha (formato YYYY-MM-DD): ")
            if len(nueva_fecha) == 10 and nueva_fecha[4] == '-' and nueva_fecha[7] == '-':
                VAR_2_DATE = nueva_fecha
                print(f"Fecha actualizada a {VAR_2_DATE}")
            else:
                print("Formato de fecha incorrecto. Use YYYY-MM-DD (ej: 2025-04-01)")

        elif opcion == "4":
            editor.guardar_archivo()

        elif opcion == "5":
            ruta_nueva = input("Introduce la ruta para el nuevo archivo: ")
            editor.guardar_archivo(ruta_nueva)

        elif opcion == "6":
            respuesta = input("¿Seguro que deseas salir? Los cambios no guardados se perderán (s/n): ")
            if respuesta.lower() == "s":
                print("¡Hasta luego!")
                break

        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 6.")


# Ejecutar el programa si se llama directamente
if __name__ == "__main__":
    menu_principal()