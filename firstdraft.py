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
    def __init__(self, coords):
        self.coords = coords
        self.variables_map =  {
            'temperatura': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'temperature_2m'),
            'precipitacion': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'total_precipitation_sum'),
            'radiacion solar': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'surface_net_solar_radiation'),
            'presion': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'surface_pressure')
        }
        self.variables_derivadas_map = {
            'direccion viento':('ECMWF/ERA5_LAND/DAILY_AGGR', ['u_component_of_wind_10m','v_component_of_wind_10m']),
            'velocidad viento':('ECMWF/ERA5_LAND/DAILY_AGGR', ['u_component_of_wind_10m','v_component_of_wind_10m']),
            'humedad relativa':('ECMWF/ERA5_LAND/DAILY_AGGR', ['temperature_2m','dewpoint_temperature_2m'])
        }

    def hacer_solicitud(self, variables):
        fecha = date.today() - timedelta(days=8)
        # Rebanado de los variables_maps para incluir solo las variables de interes
        selected = {var: self.variables_map[var] for var in variables if var in self.variables_map}
        derived = {var: self.variables_derivadas_map[var] for var in variables if var in self.variables_derivadas_map}
        # Diccionario con la solicitud
        detalles_solicitud = {
            'punto': ee.Geometry.Point(self.coords),
            'fecha_inicio': ee.Date(fecha.isoformat()),
            'fecha_final': ee.Date(fecha.isoformat()).advance(1, 'day'),
            'variables': selected,
            'variables_derivadas': derived
        }
        return detalles_solicitud

# ---------------------------Extracción de Datos-----------------------------
'''
Descripciones varias
Metodo fetch: obtiene los datos de las variables especificadas en la solicitud
    retorna un diccionario con nombre de la variable y los valores muestreados
Metodo get_samples: extrae la colección de imágenes y extrae una y solo una
    muestra
Metodo get_values: genera valores segun la variable a partir de las muestras 
    obtenidas
Metodo to_dataframe: retorna un DataFrame de una fila con los valores de las
    variables de interés
'''
class DataFetcher:
    def __init__(self, solicitud):
        self.solicitud = solicitud

    def fetch(self):
        punto = self.solicitud['punto']
        f1 = self.solicitud['fecha_inicio']
        f2 = self.solicitud['fecha_final']

        results = {}
        # Variables directas
        for var_name, (dataset, band) in self.solicitud['variables'].items():
            results[var_name] = self.get_values(var_name, dataset, [band], f1, f2, punto)
        # Variables derivadas
        for var_name, (dataset, bands) in self.solicitud['variables_derivadas'].items():
            results[var_name] = self.get_values(var_name, dataset, bands, f1, f2, punto)
        return results
    
    def get_sample(self, dataset, bands, f1, f2, punto):
        coll = ee.ImageCollection(dataset).filterDate(f1, f2).select(bands)
        count = coll.size().getInfo()
        if count == 1:
            img = coll.first()
            muestra = img.sample(region=punto, scale=10000).first().toDictionary().getInfo()
            return muestra
        elif count == 0:
            raise ValueError(f"{bands}: No se encontraron imágenes para el periodo de {f1} a {f2}.")
        else:
            raise ValueError(f"{bands}: El programa espera 1 imagen, pero se encontraron {count} entre {f1} y {f2}.")

    def get_values(self, var_name, dataset, bands, f1, f2, punto):
        muestra = self.get_sample(dataset, bands, f1, f2, punto)

        if var_name == 'velocidad viento':
            u, v = muestra[bands[0]], muestra[bands[1]]
            return (u**2 + v**2)**0.5
        elif var_name == 'direccion viento':
            u, v = muestra[bands[0]], muestra[bands[1]]
            return (180 / math.pi) * math.atan2(v, u)
        elif var_name == 'humedad relativa':
            T, Td = muestra[bands[0]], muestra[bands[1]]
            return 100 * (math.exp((17.625*Td)/(243.04+Td)) /
                          math.exp((17.625*T)/(243.04+T)))
        elif var_name == 'temperatura':
            kelvin = muestra.get(bands[0])
            return kelvin - 273.15 if kelvin is not None else None
        else:
            # Para variables directas, bands es una lista de un elemento
            return muestra.get(bands[0])
    
    def to_dataframe(self):
        results = self.fetch()
        df = pd.DataFrame(results, index=[0]) # una fila por solicitud
        return df

    
# DEMO DE FUNCIONAMIENTO
# 1. Hacer la solicitud
solicitud_class = Solicitud(coords=[-99.1332, 19.4326])
detalles = solicitud_class.hacer_solicitud(['temperatura', 'precipitacion', 'humedad relativa'])

# 2. Pasarla al fetcher
fetcher = DataFetcher(detalles)
valores = fetcher.to_dataframe()

print(valores)

'''
Consideraciones adicionales
El código esta diseñado para trabajar con datasets que manejen imagenes diarias,
al usar colecciones de tipo hourly o monthly se le mostrará un error y no podrá
completarse su solicitud.
'''