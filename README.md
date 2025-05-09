# 🛠️ File Automation Scripts

Un conjunto de scripts en Python para automatizar flujos de trabajo comunes relacionados con archivos, datos y documentos XML.

## 📚 Scripts Incluidos

### 1. **Generador de Documentos (`gen_docs.py`)**
   - Procesa archivos `.crdownload` con contenido XML.
   - Extrae información clave (ID, FV_VALUE, datos del paciente).
   - Crea estructura de carpetas organizada para cada documento.
   - Genera archivo Excel con resumen de todos los documentos procesados.

### 2. **Procesador de Facturas XML (`app.py`)**
   - Modifica archivos XML de facturas para añadir bloques específicos.
   - Inserta bloques `MODALIDAD_PAGO`, `COBERTURA_PLAN_BENEFICIOS` e `InvoicePeriod`.
   - Incluye interfaz por consola con menú de opciones.
   - Permite modificar la fecha y guardar los cambios.

### 3. **Buscador de Pacientes en Excel**
   - Normaliza espacios y mayúsculas en nombres.
   - Extrae datos fijos (Paciente, Documento, Género, Edad, Fecha de nacimiento) en tabla.
   - Lista todas las citas asociadas con sus fechas, estados, códigos y servicios.

## 📂 Estructura del Proyecto

```
file-automation-scripts/
├── App/
│   └── app.py                # Procesador de facturas XML
├── Scripts/
│   ├── gen_docs.py           # Script de generación de documentos
│   └── Older_Versions/       # Versiones anteriores de los scripts
│       ├── gen_docs_v0.py
│       ├── gen_docs_v1.py
│       └── gen_docs_v2.py
├── buscar_paciente.py        # Script de búsqueda y formateo en Excel
└── README.md                 # Documentación de uso
```

## ⚙️ Requisitos

- Python 3.7 o superior
- pandas
- openpyxl
- tabulate

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## 🚀 Uso de los Scripts

### Generador de Documentos (`gen_docs.py`)

Este script procesa archivos `.crdownload` que contienen documentos XML y genera una estructura organizada:

1. Configura las rutas en las constantes al inicio del script:
   ```python
   CRDOWNLOAD_DIR    = Path(r"C:\ruta\a\tus\archivos\crdownload")
   JSON_SOURCE_PATH  = Path(r"C:\ruta\a\template.json")
   MASTER_OUTPUT_DIR = Path(r"C:\ruta\de\salida")
   EXCEL_OUTPUT_PATH = Path(r"C:\ruta\al\excel\resultado.xlsx")
   ```

2. Ejecuta el script:
   ```bash
   python Scripts/gen_docs.py
   ```

3. El script realizará las siguientes acciones:
   - Procesa cada archivo `.crdownload` encontrado
   - Extrae ID, valor FV, nombre y documento del paciente
   - Crea una carpeta con formato `ID-FV-DOCUMENTO-NOMBRE`
   - Genera un archivo XML y copia la plantilla JSON
   - Guarda un Excel con toda la información extraída

### Procesador de Facturas XML (`app.py`)

Este script modifica archivos XML de facturas para añadir información específica:

1. Configura la ruta al archivo XML en la clase `App`:
   ```python
   self.PATH_XML = r"C:\ruta\a\tu\archivo.xml"
   ```

2. Ejecuta el script:
   ```bash
   python App/app.py
   ```

3. Utiliza el menú interactivo para:
   - Insertar bloques específicos (CODIGO_PRESTADOR, InvoicePeriod)
   - Cambiar la fecha del documento
   - Guardar los cambios en el archivo original o en una nueva ubicación
   - Ver un resumen de las operaciones realizadas

### Buscador de Pacientes en Excel

1. Configura las constantes al inicio del script:
   ```python
   FILENAME  = "data.xlsx"
   SHEETNAME = "informe_operacion"
   ```

2. Ejecuta el script:
   ```bash
   python buscar_paciente.py
   ```

3. Ingresa el nombre del paciente cuando te lo solicite.

## 🔍 Detalles Técnicos

### Procesamiento de Documentos XML

El generador de documentos utiliza expresiones regulares para extraer información clave de los archivos XML:

```python
def extract_fv_value(text: str) -> str:
    """Extrae el valor FV dentro de <cbc:ParentDocumentID>...</cbc:ParentDocumentID>."""
    m = re.search(r'<cbc:ParentDocumentID>\s*([^<]+)\s*</cbc:ParentDocumentID>', text)
    return m.group(1) if m else None
```

### Modificación de Facturas XML

El procesador de facturas inserta bloques XML como:

```xml
<AdditionalInformation>
  <Name>MODALIDAD_PAGO</Name>
  <Value schemeID="04" schemeName="salud_modalidad_pago.gc">Pago por evento</Value>
</AdditionalInformation>
```

Y bloques de fecha:

```xml
<cac:InvoicePeriod>
  <cbc:StartDate>2025-04-04</cbc:StartDate>
  <cbc:StartTime>12:00:00</cbc:StartTime>
  <cbc:EndDate>2025-04-04</cbc:EndDate>
  <cbc:EndTime>12:00:00</cbc:EndTime>
</cac:InvoicePeriod>
```

## 🤝 Contribuciones

1. Haz un fork 🍴
2. Crea una rama nueva: `git checkout -b feature/mi-cambio`
3. Commit de tus cambios: `git commit -m "Agrega nueva funcionalidad"`
4. Push a tu fork: `git push origin feature/mi-cambio`
5. Abre un Pull Request 📝

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.
Consulta el archivo [LICENSE](LICENSE) para más detalles.