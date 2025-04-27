# file-automation-scripts

Un conjunto de scripts en Python para automatizar dos flujos de trabajo comunes:

1. **Buscar pacientes en Excel**  
   - Normaliza espacios y mayúsculas en nombres.  
   - Extrae datos fijos (Paciente, Documento, Género, Edad, Fecha de nacimiento) en tabla.  
   - Lista todas las citas asociadas con sus fechas, estados, códigos y servicios.

2. **Procesar archivos `.crdownload`**  
   - Detecta todos los `*.crdownload` de un directorio.  
   - Extrae el ID del nombre de archivo y el valor `ParentDocumentID` (FV…).  
   - Genera, para cada uno, una carpeta `ID-FV_VALUE/` con:
     - `FV_VALUE.xml` (contenido original del `.crdownload`).  
     - `FV_VALUE.json` (plantilla JSON copiada).

---

## 📂 Estructura

```
file-automation-scripts/
├── buscar_paciente.py        # Script de búsqueda y formateo en Excel
├── process_crdownloads.py    # Script de procesamiento de .crdownload
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación de uso
```

---

## ⚙️ Requisitos

- Python 3.7 o superior  
- pandas  
- openpyxl  
- tabulate  

Instálalos con:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuración

Cada script define al inicio unas constantes que debes ajustar:

```python
# buscar_paciente.py
FILENAME  = "data.xlsx"
SHEETNAME = "informe_operacion_1745627271"
```

```python
# process_crdownloads.py
CRDOWNLOAD_DIR    = Path(r"C:\ruta\a\input_cr")
JSON_SOURCE_PATH  = Path(r"C:\ruta\a\template.json")
MASTER_OUTPUT_DIR = Path(r"C:\ruta\a\output_master")
```

---

## 🚀 Uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/file-automation-scripts.git
   cd file-automation-scripts
   ```

2. **Buscar pacientes**:
   ```bash
   python buscar_paciente.py
   # Ingresa el nombre cuando te lo solicite
   ```

3. **Procesar .crdownload**:
   ```bash
   python process_crdownloads.py
   # Procesará todos los .crdownload en CRDOWNLOAD_DIR
   ```

---

## 🤝 Contribuciones

1. Haz un fork 🍴  
2. Crea una rama nueva: `git checkout -b feature/mi-cambio`  
3. Commit de tus cambios: `git commit -m "Agrega nueva funcionalidad"`  
4. Push a tu fork: `git push origin feature/mi-cambio`  
5. Abre un Pull Request 📝  

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.
