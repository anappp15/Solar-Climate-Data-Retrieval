import ee
import pandas as pd
from datetime import date, timedelta

# ---Inicializamos la sesión de Earth Engine con el proyecto especificado---
ee.Initialize(project="place-holder-project")

# -------------------------Detalles de Solicitud-----------------------------
'''
Observación: se hace la solicitud de la data de hace 8 días para
asegurar la existencia de información a partir de la cual predecir
'''

class Solicitud:
    def __init__(self, coords, variables_map=None):
        self.coords = coords
        self.variables_map = variables_map or {
            'temperatura': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'temperature_2m'),
            'precipitacion': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'total_precipitation_sum'),
            'radiacion solar': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'surface_net_solar_radiation'),
            'presion': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'surface_pressure')
        }

    def hacer_solicitud(self, variables):
        fecha = date.today() - timedelta(days=8)
        # Rebanado de variable_maps para incluir solo las variables de interes
        selected = {var: self.variables_map[var] for var in variables if var in self.variables_map}
        # Diccionario con la solicitud
        detalles_solicitud = {
            'punto': ee.Geometry.Point(self.coords),
            'fecha_inicio': ee.Date(fecha.isoformat()),
            'fecha_final': ee.Date(fecha.isoformat()).advance(1, 'day'),
            'variables': selected
        }
        return detalles_solicitud

# ---------------------------Extracción de Datos-----------------------------
'''
Descripciones varias
Metodo fetch: obtiene los datos de las variables especificadas en la solicitud
    retorna un diccionario con nombre de la variable y los valores muestreados
'''
class ERA5Fetcher:
    def __init__(self, solicitud):
        self.solicitud = solicitud

    def fetch(self):
        punto = self.solicitud['punto']
        f1 = self.solicitud['fecha_inicio']
        f2 = self.solicitud['fecha_final']
        variables = self.solicitud['variables']
        # Iteración para llenar el diccionario de valores
        results = {}
        for var_name, (dataset, band) in variables.items():
            coll = ee.ImageCollection(dataset) \
                        .filterDate(f1, f2) \
                        .select([band])
            # Sección de manejo de precauciones de solicitud
            count = coll.size().getInfo()
            if count == 1:
                img = coll.first()
                muestra = img.sample(region=punto, scale=10000).first()
                valores = muestra.toDictionary().getInfo()
                results[var_name] = valores.get(band)
            elif count == 0:
                results[var_name] = None
                raise ValueError(f"{var_name}: No se encontraron imágenes para el periodo de {f1} a {f2}.")
            else:
                raise ValueError(f"{var_name}: El programa espera 1 imagen, pero se encontraron {count} entre {f1} y {f2}.")
        return results
    
# DEMO DE FUNCIONAMIENTO
# 1. Hacer la solicitud
solicitud_class = Solicitud(coords=[-99.1332, 19.4326])
detalles = solicitud_class.hacer_solicitud(['temperatura', 'precipitacion'])

# 2. Pasarla al fetcher
fetcher = ERA5Fetcher(detalles)
valores = fetcher.fetch()

print(valores)