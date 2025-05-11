import os

from App.ExcelData import ExcelData
from App.JsonData import JsonData
from App.Log import Log
from App.SearchFiles import SearchFiles
import re

from UpdateExcel import procesar_directorios_actualizar_excel as update_excel



class App:
    def __init__(self):
        # RUTAS ARCHIVOS
        self.RUTA_FACTS = r"C:\Users\Sergio Silva\Desktop\Invoice-Scripts\Test Facts"
        self.EJ_RUTA_XML = r"C:\Users\Sergio Silva\Desktop\Invoice-Scripts\Lab\file.xml"
        self.RUTA_EXCEL_PACIENTES = r"C:\Users\Sergio Silva\Desktop\Pacientes atendidos 2 23-25.xlsx"

        #self.lineas = []
        #self._cargar_archivo()
        #self.VAR_2_DATE = self.get_var_2_date()  # Fecha por defecto

        # EXCEL DATA
        print("*** INFO: Cargando Excel... ***")
        self.excel_obj = ExcelData(self.RUTA_EXCEL_PACIENTES)
        self.excel_data = self.excel_obj.getData()
        self.search = SearchFiles()
        print("*** INFO: EXCEL Cargado Correctamente! ***")


    def app_update_excel(self):
        ruta_dir = r"C:\Users\Sergio Silva\Desktop\1-PROC-ABR-4-7\PARA_SUBIR"
        ruta_excel = r"C:\Users\Sergio Silva\Desktop\FACTS-FILES\Lote_02-ABR-4-7.xlsx"
        update_excel(ruta_dir, ruta_excel)


    def search_val_fact(self):
        """
        Busca la ocurrencia de 'ValTolFac' en el XML cargado y extrae la parte entera del valor numérico.

        Returns:
            int: El valor entero asociado a 'ValTolFac', o None si no se encuentra.
        """
        if not self.lineas_xml:
            print("El archivo XML no está cargado.")
            return None

        # Definimos una expresión regular para encontrar 'ValTolFac' seguido de un número
        patron = r"ValTolFac:\s*([0-9]+(?:\.[0-9]+)?)"

        # Recorremos las líneas para encontrar el patrón
        for linea in self.lineas_xml:
            match = re.search(patron, linea)
            if match:
                # Extraemos el valor numérico como una cadena
                valor = match.group(1)
                # Convertimos el valor a entero
                return int(float(valor))  # Lo convertimos primero a float para eliminar posibles decimales

        print("No se encontró 'ValTolFac' en el archivo XML.")
        return None




    def get_var_2_date(self):
        """
        Busca la etiqueta <cbc:IssueDate> en el archivo XML y extrae la fecha.
        Si no encuentra la etiqueta, devuelve una fecha por defecto.

        Returns:
            str: Fecha en formato YYYY-MM-DD
        """
        fecha_default = "2025-04-04"

        if not self.lineas_xml:
            self.log.log_message("El archivo no está cargado o está vacío. Usando fecha por defecto.")
            return fecha_default

        # Buscar la etiqueta IssueDate y extraer la fecha
        for linea in self.lineas_xml:
            if "<cbc:IssueDate>" in linea:
                # Extraer el contenido entre las etiquetas
                inicio = linea.find("<cbc:IssueDate>") + len("<cbc:IssueDate>")
                fin = linea.find("</cbc:IssueDate>")
                if inicio != -1 and fin != -1:
                    fecha = linea[inicio:fin].strip()
                    self.log.log_message(f"Fecha encontrada en el XML: {fecha}")
                    return fecha

        print("No se encontró la etiqueta <cbc:IssueDate> en el XML. Usando fecha por defecto.")
        return fecha_default


    def _cargar_archivo(self, ruta_xml):
        """
        Carga el contenido del archivo XML en memoria como líneas.
        """
        try:
            with open(ruta_xml, 'r', encoding='utf-8') as archivo:
                self.lineas_xml = archivo.readlines()
            self.log.log_message(f"Archivo '{ruta_xml}' cargado correctamente.")
        except FileNotFoundError:
            self.log.log_message(f"Error: El archivo '{ruta_xml}' no existe.")
            self.lineas_xml = []
        except PermissionError:
            self.log.log_message(f"Error: No tienes permisos para leer el archivo '{ruta_xml}'.")
            self.lineas_xml = []
        except Exception as e:
            self.log.log_message(f"Error al cargar el archivo: {e}")
            self.lineas_xml = []

    def rango_xml(self, palabra_1, palabra_2):
        # Buscar rango de lineas por 2 palabras
        flag, pos_ini, pos_fin = False, 0, 0

        for i, linea in enumerate(self.lineas_xml):
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
            #print(f"   ✓ Fecha utilizada: {self.VAR_2_DATE}")
            print(
                f"   ✓ Rango de líneas: {a_op2} - {b_op2}")
        else:
            print("   ✗ No se pudo insertar el bloque")

        # Resumen del guardado
        print("\n3. GUARDADO DEL ARCHIVO:")
        if guardado:
            print(f"   ✓ Archivo guardado correctamente")
            print(f"   ✓ Ruta: {self.EJ_RUTA_XML}")
        else:
            print("   ✗ No se pudo guardar el archivo")

        print("\n" + "=" * 50)



    def run_script_zero(self):
        # Ejecutar Opcion 1
        print("\n=== Ejecutando OP1 XML: Codigo Prestador ===")
        self.bloque_cod_prestador()

        # Ejecutar Opcion 2
        print("\n=== Ejecutando OP2 XML: Fecha del Invoice ===")
        self.invoice_date()

        # Guardar cambios
        print("\n=== Guardando Cambios XML... ===")
        resultado_guardado = self.guardar_archivo()


        # Ejecutar JSON DATA
        print("\n=== Ejecutando OP3 JSON: Datos del Excel al JSON ===")
        #self.json_data()



        # Mostrar resultados y resumen
        self.show_resume(resultado_guardado)




    def bloque_cod_prestador(self):
        """
        Inserta bloques de AdditionalInformation después del bloque CODIGO_PRESTADOR.

        Returns:
            bool: True si se realizó la inserción, False en caso contrario
        """
        if not self.lineas_xml:
            self.log.log_message("El archivo no está cargado o está vacío.")
            return False

        # Buscar la posición del bloque CODIGO_PRESTADOR
        posicion = -1
        for i, linea in enumerate(self.lineas_xml):
            if "<Name>CODIGO_PRESTADOR</Name>" in linea:
                # Buscar el cierre del bloque AdditionalInformation
                for j in range(i, len(self.lineas_xml)):
                    if "</AdditionalInformation>" in self.lineas_xml[j]:
                        posicion = j
                        break
                break

        if posicion == -1:
            self.log.log_message("No se encontró el bloque CODIGO_PRESTADOR.")
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
        self.lineas_xml = self.lineas_xml[:posicion + 1] + bloques_a_insertar + self.lineas_xml[posicion + 1:]
        self.log.log_message("Bloques insertados después de CODIGO_PRESTADOR.")
        return True



    def invoice_date(self):
        """
        Inserta el bloque InvoicePeriod después de la ocurrencia de LineCountNumeric.


        Returns:
            bool: True si se realizó la inserción, False en caso contrario
        """

        fecha = self.get_var_2_date()

        if not self.lineas_xml:
            self.log.log_message("El archivo no está cargado o está vacío.")
            return False

        # Buscar la posición de LineCountNumeric
        posicion = -1
        for i, linea in enumerate(self.lineas_xml):
            if "<cbc:LineCountNumeric>" in linea:
                posicion = i
                break

        if posicion == -1:
            self.log.log_message("No se encontró la línea <cbc:LineCountNumeric>1</cbc:LineCountNumeric>.")
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
        self.lineas_xml = self.lineas_xml[:posicion + 1] + bloque_a_insertar + self.lineas_xml[posicion + 1:]
        self.log.log_message(f"Bloque InvoicePeriod insertado con fecha {fecha}.")
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
        if not self.lineas_xml:
            self.log.log_message("No hay contenido para guardar.")
            return False

        ruta_destino = ruta_salida if ruta_salida else self.rutas['xml']

        try:
            with open(ruta_destino, 'w', encoding='utf-8') as archivo:
                archivo.writelines(self.lineas_xml)
            self.log.log_message(f"Archivo guardado correctamente en '{ruta_destino}'.")
            return True
        except PermissionError:
            self.log.log_message(f"Error: No tienes permisos para escribir en '{ruta_destino}'.")
            return False
        except Exception as e:
            self.log.log_message(f"Error al guardar el archivo: {e}")
            return False


    def process_fact(self, doc):

        try:
            # Ejecutar Opcion 1
            self.log.log_message("\n=== Ejecutando OP1 XML: Codigo Prestador ===")
            self.bloque_cod_prestador()

            # Ejecutar Opcion 2
            self.log.log_message("\n=== Ejecutando OP2 XML: Fecha del Invoice ===")
            self.invoice_date()

            # Guardar cambios
            self.log.log_message("\n=== Guardando Cambios en XML... ===")
            resultado_guardado = self.guardar_archivo()


            # Ejecutar JSON DATA
            self.log.log_message("\n=== Ejecutando OP3 JSON: Datos del Excel al JSON ===")
            self.json_data(doc)


        except Exception as e:
            self.log.log_message(f"*** ERROR *** 'Exception' en funcion 'process_fact(doc)': \n OUT-> {e}")




    def get_cod_proc(self):
        """
        Extrae el ID dentro de las etiquetas StandardItemIdentification de un XML.

        """
        ids_encontrados = []
        contenido_completo = ''.join(self.lineas_xml)  # Unir todas las líneas en una sola cadena

        # Dividir por StandardItemIdentification para encontrar las secciones relevantes
        partes = contenido_completo.split("<cac:StandardItemIdentification>")

        # La primera parte no contiene lo que buscamos, así que empezamos desde la segunda
        for i in range(1, len(partes)):
            # Buscar hasta el cierre de la etiqueta StandardItemIdentification
            seccion = partes[i].split("</cac:StandardItemIdentification>")[0]

            # Extraer el contenido entre <cbc:ID> y </cbc:ID>
            inicio_id = seccion.find("<cbc:ID")
            if inicio_id != -1:
                # Encontrar el inicio del contenido después de >
                inicio_contenido = seccion.find(">", inicio_id) + 1

                # Encontrar el final del contenido antes de </cbc:ID>
                fin_contenido = seccion.find("</cbc:ID>", inicio_contenido)

                # Extraer el ID
                if inicio_contenido < fin_contenido:
                    id_valor = seccion[inicio_contenido:fin_contenido]
                    ids_encontrados.append(id_valor)

        return ids_encontrados[0]


    def get_first_codproc(self, doc):
        registro = self.excel_obj.buscar_paciente_por_cedula(doc)[0]
        return registro['codigo_cups']


    def json_data(self, doc):
        # Obtener Datos Paciente por Documento
        data_doc = self.excel_obj.get_data_by_doc(doc)

        # Agregar valores adicionales a los del excel
        data_doc['numFactura'] = self.rutas['FV_VALUE']
        data_doc['fechaIni'] = f"{self.get_var_2_date()} 00:00"

        # Codigo Servicio
        try:
            codigo = self.get_cod_proc().split('-')[0]
            int(codigo)
            data_doc['codProc'] = str(codigo)

        except ValueError as e:
            self.log.log_error(e)
            data_doc['codProc'] = self.get_first_codproc(doc)


        data_doc['valorServ'] = self.search_val_fact()

        # Modificar JSON
        self.json_obj.modificar_json(data_doc)

        # Guardar JSON
        self.json_obj.guardar_json()



    def verificar_proceso(self):
        dirs = os.listdir(self.RUTA_FACTS)
        a, b = 0, 0
        a_l, b_l = [], []

        for i, directorio in enumerate(dirs):
            rutas = self.search.buscar_por_fv(self.RUTA_FACTS, directorio.split('-')[1])

            # Crear el Log
            log_dir = r'C:\Users\Sergio Silva\Desktop\Invoice-Scripts\LOG-TEST'
            self.log = Log(log_dir, rutas['dir_pac'])
            self.excel_obj.setLog(self.log)

            FV = directorio.split('-')[1]

            self.json_obj = JsonData(rutas['json'], self.excel_obj, self.log)


            if FV == self.json_obj.getNumFac():
                a += 1
                a_l.append(directorio)

            else:
                b += 1
                b_l.append(directorio)

        print("\n======= RESUMEN PROCESO =======")
        print(f" -> # Cantidad de Facturas: {len(dirs)}")
        print(f" -> ✓ Facturas Procesadas: {a}")
        print(f" -> - Facturas Sin Procesar: {b}")

        print(f"\n *** ✓ FACTS PROCESADAS ({a})***")
        for _ in a_l:
            print(f"-> {_}")

        print(f"\n *** - FACTS SIN PROCESAR {b} ***")
        for _ in b_l:
            print(f"-> {_}")


    def script_fvvalue(self):
        fv_value = input("Digite FV VALUE: ")
        self.rutas = self.search.buscar_por_fv(self.RUTA_FACTS, fv_value)


        if self.rutas:
            print("Paciente Encontrado !")
            print(f"Dir: {self.rutas['directorio']}")


            # Crear el Log
            log_dir = r'C:\Users\Sergio Silva\Desktop\Invoice-Scripts\LOG-TEST'
            self.log = Log(log_dir, self.rutas['dir_pac'])
            self.excel_obj.setLog(self.log)

            # Cargar XML
            self.lineas_xml = []
            self._cargar_archivo(self.rutas['xml'])
            if not self.lineas_xml:
                self.log.log_message("No se pudo cargar el archivo XML. Saliendo.")
                return

            # Cargar JSON
            self.json_obj = JsonData(self.rutas['json'], self.excel_obj, self.log)

            # Procesar Factura: XML - JSON - EXCEL
            self.process_fact(self.rutas['doc'])


            # Mostrar INFO Paciente
            self.excel_obj.mostrar_resultados(self.excel_obj.buscar_paciente_por_cedula(fv_value))

        else:
            self.log.log_message(f"ERROR: El Directorio con referencia al DOC: {fv_value} no existe!")



    def script_final(self):
        dirs = os.listdir(self.RUTA_FACTS)
        a, b = 0, 0

        for i, directorio in enumerate(dirs):
            try:
                doc = directorio.split("-")[2]
                fv_value = directorio.split("-")[1]
                self.rutas = self.search.buscar_por_fv(self.RUTA_FACTS, fv_value)

                if self.rutas:

                    # ************ Logica ************

                    # Crear el Log
                    log_dir = r'C:\Users\Sergio Silva\Desktop\Invoice-Scripts\LOG-TEST'
                    self.log = Log(log_dir, self.rutas['dir_pac'])
                    self.excel_obj.setLog(self.log)

                    # Cargar XML
                    self.lineas_xml = []
                    self._cargar_archivo(self.rutas['xml'])
                    if not self.lineas_xml:
                        self.log.log_message("No se pudo cargar el archivo XML. Saliendo.")
                        return

                    # Cargar JSON
                    self.json_obj = JsonData(self.rutas['json'], self.excel_obj, self.log)

                    # Procesar Factura: XML - JSON - EXCEL
                    self.process_fact(doc)

                    # Mostrar INFO Paciente
                    self.excel_obj.mostrar_resultados(self.excel_obj.buscar_paciente_por_cedula(doc))


                    self.log.print_with_log(f" {i}) ✓ Factura '{directorio}' procesada con Exito!")
                    a += 1
                else:
                    self.log.print_with_log("ERROR: no encontro por el doc suministrado (func script_final())")
                    b += 1

            except Exception as e:
                self.log.print_with_log(f" {i}) *ERROR* -> Factura '{directorio}' sin procesar (Revisar el LOG)!\n ERROR {e}")
                b += 1


        # Resumen
        self.verificar_proceso()






def menu():
    # VARIABLES
    app  = App()

    print("\n=== APLICACION INVOICE v1.0 ===")


    while True:
        print("\n=== MENÚ DE OPERACIONES ===")
        print("0) SCRIPT ZERO: Ejectutar XML y JSON Scripts!")
        print("1) *** { SCRIPT FINAL } ***: Procesar Todos Los pacientes")
        print("2) SCRIPT: Procesar por FV-VALUE")
        print("=======================================")
        print(" *** Otras funciones ***")
        print("5. Insertar en XML -> CODIGO_PRESTADOR")
        print("6. Insertar en XML -> FECHA InvoicePeriod")
        print("7. - Verificar Facts Procesadas")
        print("8) *** Actualizar Excel Hash ***")
        print("X) Salir")

        opcion = input("\nSelecciona una opción (1-6): ")

        if opcion == "0":
            app.run_script_zero()

        elif opcion == '1':
            app.script_final()

        elif opcion == "2":
            app.script_fvvalue()

        elif opcion == "5":
            app.bloque_cod_prestador()

        elif opcion == "6":
            app.invoice_date()

        elif opcion == '7':
            app.verificar_proceso()

        elif opcion.lower() == "x":
            respuesta = input("¿Seguro que deseas salir? Los cambios no guardados se perderán (s/n): ")
            if respuesta.lower() == "s":
                print("¡Hasta luego!")
                break

        elif opcion == '8':
            app.app_update_excel()


        else:
            print("Opción no válida. Por favor, selecciona una opción del 1 al 6.")




if __name__ == '__main__':
    menu()



