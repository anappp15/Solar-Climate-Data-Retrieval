# Solar-Climate Data Retrieval

This repository provides Python classes for **retrieving and sampling climate variables from Google Earth Engine (ERA5 datasets)**. The tool is designed to support **solar-climate analysis workflows**, enabling both direct and derived variable extraction at specific coordinates.

---

## ✨ Features
- **Solicitud class**  
  - Builds a request dictionary for a given coordinate.  
  - Supports both **direct variables** (temperature, precipitation, solar radiation, pressure) and **derived variables** (wind speed, wind direction, relative humidity).  
  - Automatically slices the variable maps to include only those requested.  
  - Uses data from **8 days prior to today** to ensure availability.

- **DataFetcher class**  
  - Executes the request against Google Earth Engine.  
  - Methods:
    - `fetch()` → retrieves values for all requested variables.  
    - `get_sample()` → extracts a single image sample for the specified date and bands.  
    - `get_values()` → computes values, including derived formulas (e.g., wind speed from u/v components, relative humidity from dewpoint and temperature, temperature converted from Kelvin to Celsius).  
    - `to_dataframe()` → returns results as a tidy **pandas DataFrame** (one row per request).

---

## 📖 Example Usage

```python
import ee
import pandas as pd
from datetime import date, timedelta

# Initialize Earth Engine
ee.Initialize(project="place-holder-project")

# 1. Build the request
solicitud_class = Solicitud(coords=[-99.1332, 19.4326])
detalles = solicitud_class.hacer_solicitud(
    ['temperatura', 'precipitacion', 'humedad relativa']
)

# 2. Pass into the fetcher
fetcher = DataFetcher(detalles)
valores = fetcher.to_dataframe()

print(valores)
```

**Output:**
```
   temperatura  precipitacion  humedad relativa
0        25.3           0.002              65.4
```

---

## ⚙️ Quick Setup

### Requirements
- Python 3.9+
- [Google Earth Engine Python API](https://developers.google.com/earth-engine/python_install)
- pandas

Install dependencies:
```bash
pip install earthengine-api pandas
```

### Authentication
Before running the demo:
1. Authenticate with Earth Engine:
   ```bash
   earthengine authenticate
   ```
   Follow the link, sign in with your Google account, and paste the token back.
2. Initialize Earth Engine in your code with your project:
   ```python
   import ee
   ee.Initialize(project="your-gcp-project-id")
   ```

### Running the Demo
Clone the repository:
```bash
git clone https://github.com/anappp15/Solar-Climate-Data-Retrieval.git
cd Solar-Climate-Data-Retrieval
```

Run the demo script:
```bash
python demo.py
```

This will:
- Build a request for selected variables (e.g., temperature, precipitation, relative humidity).
- Fetch values from ERA5 daily aggregates.
- Return results as a tidy pandas DataFrame.

---

## ⚠️ Considerations
- The code is designed for **daily aggregated datasets** (`ECMWF/ERA5_LAND/DAILY_AGGR`).  
- Using hourly or monthly collections will raise an error, since the workflow expects exactly one image per date.  
- Temperature values are automatically converted from **Kelvin to Celsius**.  
- Derived variables are computed internally:
  - Wind speed = √(u² + v²)  
  - Wind direction = atan2(v, u) in degrees  
  - Relative humidity = approximation using dewpoint and temperature  
