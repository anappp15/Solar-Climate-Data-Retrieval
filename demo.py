import ee
import pandas as pd
import math
from datetime import date, timedelta

# Inicializamos Earth Engine (requiere autenticación previa)
ee.Initialize(project="place-holder-project")

# -------------------------Clase Solicitud-----------------------------
class Solicitud:
    def __init__(self, coords):
        self.coords = coords
        self.variables_map = {
            'temperatura': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'temperature_2m'),
            'precipitacion': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'total_precipitation_sum'),
            'radiacion solar': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'surface_net_solar_radiation'),
            'presion': ('ECMWF/ERA5_LAND/DAILY_AGGR', 'surface_pressure')
        }
        self.variables_derivadas_map = {
            'direccion viento': ('ECMWF/ERA5_LAND/DAILY_AGGR',
                                 ['u_component_of_wind_10m','v_component_of_wind_10m']),
            'velocidad viento': ('ECMWF/ERA5_LAND/DAILY_AGGR',
                                 ['u_component_of_wind_10m','v_component_of_wind_10m']),
            'humedad relativa': ('ECMWF/ERA5_LAND/DAILY_AGGR',
                                 ['temperature_2m','dewpoint_temperature_2m'])
        }

    def hacer_solicitud(self, variables):
        fecha = date.today() - timedelta(days=8)
        selected = {var: self.variables_map[var] for var in variables if var in self.variables_map}
        derived = {var: self.variables_derivadas_map[var] for var in variables if var in self.variables_derivadas_map}
        return {
            'punto': ee.Geometry.Point(self.coords),
            'fecha_inicio': ee.Date(fecha.isoformat()),
            'fecha_final': ee.Date(fecha.isoformat()).advance(1, 'day'),
            'variables': selected,
            'variables_derivadas': derived
        }

# -------------------------Clase DataFetcher-----------------------------
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
            raise ValueError(f"{bands}: Se esperaban 1 imagen, pero se encontraron {count} entre {f1} y {f2}.")

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
            return muestra.get(bands[0])

    def to_dataframe(self):
        results = self.fetch()
        return pd.DataFrame(results, index=[0])

# -------------------------Demo opcional-----------------------------
if __name__ == "__main__":
    solicitud_class = Solicitud(coords=[-99.1332, 19.4326])
    detalles = solicitud_class.hacer_solicitud(['temperatura', 'precipitacion', 'humedad relativa'])
    fetcher = DataFetcher(detalles)
    valores = fetcher.to_dataframe()
    print(valores)