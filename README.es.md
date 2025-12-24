# Recuperación de Datos de Clima Solar

Este repositorio proporciona clases en Python para recuperar variables de radiación y clima utilizando **Google Earth Engine**.  
Las dos clases principales son:  
- **Solicitud** → define la petición (ubicación, variables, fecha).  
- **DataFetcher** → extrae valores de los conjuntos de datos de Earth Engine y los devuelve como diccionarios o DataFrames de Pandas.

---

## 📂 Estructura del Proyecto
- `retrieval_classes.py` → Clases principales (`Solicitud`, `DataFetcher`).  
- `demo.py` → Ejemplo de uso del flujo de recuperación.  
- `requirements.txt` → Dependencias (`earthengine-api`, `pandas`).  

---

## ⚡ Características
- Recupera múltiples variables (radiación solar, temperatura, precipitación, viento, humedad, aerosoles, elevación, etc.).  
- Soporte para conjuntos de datos **diarios**, **por hora** y **estáticos**.  
- Manejo automático de velocidad y dirección del viento, humedad relativa y conversión de temperatura.  
- Exporta resultados a DataFrame de Pandas para análisis.  

---

## 🚀 Instalación
```bash
git clone https://github.com/anappp15/Solar-Climate-Data-Retrieval.git
cd Solar-Climate-Data-Retrieval
pip install -r requirements.txt
```

Asegúrate de tener [Google Earth Engine](https://developers.google.com/earth-engine) inicializado:  
```bash
earthengine authenticate
```

---

## 📖 Uso

### Importar Clases
```python
from retrieval_classes import Solicitud, DataFetcher
```

### Ejemplo de Flujo
```python
# Definir coordenadas (longitud, latitud)
coords = (-82.43, 8.43)  # Ejemplo: David, Chiriquí, Panamá

# Crear una solicitud de radiación solar y temperatura
solicitud = Solicitud(coords).hacer_solicitud(
    variables=['radiacion solar', 'temperatura']
)

# Extraer datos
fetcher = DataFetcher(solicitud)
df = fetcher.to_dataframe()

print(df)
```

---

## 📌 Notas
- La fecha por defecto es **7 días atrás** para asegurar disponibilidad de datos.  
- Las variables deben coincidir con las claves en `Solicitud.registro_variables`.  
- Extiende `Solicitud` para añadir nuevos conjuntos de datos o bandas.  
- `DataFetcher.to_dataframe()` incluye metadatos (latitud, longitud, fecha).  

- Las solicitudes están diseñadas para devolver **datos de un solo día**.  
- Si existen múltiples imágenes para ese día, el código las promediará o manejará la discrepancia de forma controlada.  
- Esto asegura valores diarios consistentes para el análisis.

¿Quieres que te prepare también un **“Futuro Trabajo”** en español para mencionar la posible extensión a **semanal y mensual** de forma natural?
