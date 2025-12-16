# Recuperación de Datos Solar-Climáticos

Este repositorio contiene clases en Python para **recuperar y muestrear variables climáticas desde Google Earth Engine (datasets ERA5)**. La herramienta está diseñada para apoyar flujos de trabajo de **análisis solar-climático**, permitiendo extraer tanto variables directas como derivadas en coordenadas específicas.

---

## ✨ Características
- **Clase Solicitud**  
  - Construye un diccionario de solicitud para una coordenada dada.  
  - Soporta **variables directas** (temperatura, precipitación, radiación solar, presión) y **variables derivadas** (velocidad del viento, dirección del viento, humedad relativa).  
  - Usa datos de **8 días atrás** para asegurar disponibilidad.  

- **Clase DataFetcher**  
  - Ejecuta la solicitud en Google Earth Engine.  
  - Métodos:
    - `fetch()` → obtiene valores de las variables solicitadas.  
    - `get_sample()` → extrae una muestra única de la colección de imágenes.  
    - `get_values()` → calcula valores, incluyendo fórmulas derivadas (ej. velocidad del viento a partir de u/v, humedad relativa a partir de temperatura y punto de rocío, temperatura convertida de Kelvin a Celsius).  
    - `to_dataframe()` → retorna los resultados como un **DataFrame de pandas**.  

---

## 📖 Ejemplo de uso

```python
solicitud_class = Solicitud(coords=[-99.1332, 19.4326])
detalles = solicitud_class.hacer_solicitud(['temperatura','precipitacion','humedad relativa'])

fetcher = DataFetcher(detalles)
valores = fetcher.to_dataframe()

print(valores)
```

**Salida esperada:**
```
   temperatura  precipitacion  humedad relativa
0        25.3           0.002              65.4
```

---

## ⚙️ Configuración rápida

### Requisitos
- Python 3.9+
- [Google Earth Engine Python API](https://developers.google.com/earth-engine/python_install)
- pandas

Instalar dependencias:
```bash
pip install earthengine-api pandas
```

### Autenticación
Antes de ejecutar el demo:
1. Autenticar con Earth Engine:
   ```bash
   earthengine authenticate
   ```
   Sigue el enlace, inicia sesión con tu cuenta de Google y pega el token.
2. Inicializar Earth Engine en tu código:
   ```python
   import ee
   ee.Initialize(project="tu-proyecto-gcp")
   ```

### Ejecutar el demo
Clonar el repositorio:
```bash
git clone https://github.com/anappp15/Solar-Climate-Data-Retrieval.git
cd Solar-Climate-Data-Retrieval
```

Ejecutar el script:
```bash
python demo.py
```

---

## ⚠️ Consideraciones
- El código está diseñado para datasets **diarios** (`ECMWF/ERA5_LAND/DAILY_AGGR`).  
- Usar colecciones horarias o mensuales generará un error.  
- La temperatura se convierte automáticamente de **Kelvin a Celsius**.  
- Variables derivadas se calculan internamente:
  - Velocidad del viento = √(u² + v²)  
  - Dirección del viento = atan2(v, u) en grados  
  - Humedad relativa = aproximación usando punto de rocío y temperatura  
