
class App:
    def __init__(self):
        self.PATH_XML = r"C:\Users\Sergio Silva\Desktop\Invoice-Scripts\Lab\file_2.xml"
        self.lineas = []
        self._cargar_archivo()
        self.VAR_2_DATE = self.get_var_2_date()  # Fecha por defecto




    def get_var_2_date(self):
        """
        Busca la etiqueta <cbc:IssueDate> en el archivo XML y extrae la fecha.
        Si no encuentra la etiqueta, devuelve una fecha por defecto.

        Returns:
            str: Fecha en formato YYYY-MM-DD
        """
        fecha_default = "2025-04-04"

        if not self.lineas:
            print("El archivo no está cargado o está vacío. Usando fecha por defecto.")
            return fecha_default

        # Buscar la etiqueta IssueDate y extraer la fecha
        for linea in self.lineas:
            if "<cbc:IssueDate>" in linea:
                # Extraer el contenido entre las etiquetas
                inicio = linea.find("<cbc:IssueDate>") + len("<cbc:IssueDate>")
                fin = linea.find("</cbc:IssueDate>")
                if inicio != -1 and fin != -1:
                    fecha = linea[inicio:fin].strip()
                    print(f"Fecha encontrada en el XML: {fecha}")
                    return fecha

        print("No se encontró la etiqueta <cbc:IssueDate> en el XML. Usando fecha por defecto.")
        return fecha_default


    def _cargar_archivo(self):
        """
        Carga el contenido del archivo XML en memoria como líneas.
        """
        try:
            with open(self.PATH_XML, 'r', encoding='utf-8') as archivo:
                self.lineas = archivo.readlines()
            print(f"Archivo '{self.PATH_XML}' cargado correctamente.")
        except FileNotFoundError:
            print(f"Error: El archivo '{self.PATH_XML}' no existe.")
            self.lineas = []
        except PermissionError:
            print(f"Error: No tienes permisos para leer el archivo '{self.PATH_XML}'.")
            self.lineas = []
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            self.lineas = []

    def rango_xml(self, palabra_1, palabra_2):
        # Buscar rango de lineas por 2 palabras
        flag, pos_ini, pos_fin = False, 0, 0

        for i, linea in enumerate(self.lineas):
            if palabra_1 in linea:
                pos_ini = i

            elif palabra_2 in linea:
                pos_fin = i + 2
                flag = True
                break

        return flag, pos_ini, pos_fin

    def show_resume(self, guardado):
        # Verificar OP1
        flag_op1, a_op1, b_op1 = self.rango_xml("<Name>MODALIDAD_PAGO</Name>", 'schemeID="15"')

        # Verificar OP2
        flag_op2, a_op2, b_op2 = self.rango_xml("<cac:InvoicePeriod>", "</cac:InvoicePeriod>")
        a_op2 += 1
        b_op2 -= 1

        # Mostrar resumen completo
        print("\n" + "=" * 50)
        print("              RESUMEN DE EJECUCIÓN")
        print("=" * 50)

        # Resumen del bloque CODIGO_PRESTADOR
        print("\n1. BLOQUE CODIGO_PRESTADOR:")
        if flag_op1:
            print(f"   ✓ Insertado correctamente")
            print(
                f"   ✓ Rango de líneas: {a_op1} - {b_op1}")
        else:
            print("   ✗ No se pudo insertar el bloque")

        # Resumen del bloque INVOICE_PERIOD
        print("\n2. BLOQUE INVOICE_PERIOD:")
        if flag_op2:
            print(f"   ✓ Insertado correctamente")
            print(f"   ✓ Fecha utilizada: {self.VAR_2_DATE}")
            print(
                f"   ✓ Rango de líneas: {a_op2} - {b_op2}")
        else:
            print("   ✗ No se pudo insertar el bloque")

        # Resumen del guardado
        print("\n3. GUARDADO DEL ARCHIVO:")
        if guardado:
            print(f"   ✓ Archivo guardado correctamente")
            print(f"   ✓ Ruta: {self.PATH_XML}")
        else:
            print("   ✗ No se pudo guardar el archivo")

        print("\n" + "=" * 50)



    def run_script_zero(self):
        # Ejecutar Opcion 1
        print("\n=== Ejecutando OP1: Codigo Prestador ===")
        self.bloque_cod_prestador()

        # Ejecutar Opcion 2
        print("\n=== Ejecutando OP2: Fecha del Invoice ===")
        self.invoice_date()

        # Guardar cambios
        print("\n=== Guardando Cambios... ===")
        resultado_guardado = self.guardar_archivo()

        # Mostrar resultados y resumen
        self.show_resume(resultado_guardado)



    def bloque_cod_prestador(self):
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



    def invoice_date(self):
        """
        Inserta el bloque InvoicePeriod después de la ocurrencia de LineCountNumeric.


        Returns:
            bool: True si se realizó la inserción, False en caso contrario
        """

        fecha = self.VAR_2_DATE

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

        ruta_destino = ruta_salida if ruta_salida else self.PATH_XML

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




def menu():
    # VARIABLES
    app  = App()


    print("\n=== APLICACION INVOICE v1.0 ===")

    if not app.lineas:
        print("No se pudo cargar el archivo. Saliendo.")
        return

    while True:
        print("\n--- MENÚ DE OPERACIONES ---")
        print("0. SCRIPT ZERO: Ejectutar XML y JSON Scripts!")
        print("1. Insertar BLOQUE -> CODIGO_PRESTADOR")
        print("2. Insertar BLOQUE -> FECHA InvoicePeriod")
        print("3. Cambiar la fecha para InvoicePeriod (actual:", app.PATH_XML, ")")
        print("4. Guardar cambios")
        print("5. Guardar como...")
        print("6. Salir")

        opcion = input("\nSelecciona una opción (1-6): ")

        if opcion == "0":
            app.run_script_zero()

        elif opcion == "1":
            app.bloque_cod_prestador()

        elif opcion == "2":
            app.invoice_date()

        elif opcion == "3":
            nueva_fecha = input("Introduce la nueva fecha (formato YYYY-MM-DD): ")
            if len(nueva_fecha) == 10 and nueva_fecha[4] == '-' and nueva_fecha[7] == '-':
                var_2_date = nueva_fecha
                print(f"Fecha actualizada a {var_2_date}")
            else:
                print("Formato de fecha incorrecto. Use YYYY-MM-DD (ej: 2025-04-01)")

        elif opcion == "4":
            app.guardar_archivo()

        elif opcion == "5":
            ruta_nueva = input("Introduce la ruta para el nuevo archivo: ")
            app.guardar_archivo(ruta_nueva)

        elif opcion == "6":
            respuesta = input("¿Seguro que deseas salir? Los cambios no guardados se perderán (s/n): ")
            if respuesta.lower() == "s":
                print("¡Hasta luego!")
                break

        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 6.")




if __name__ == '__main__':
    menu()

