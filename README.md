# Solar Climate Data Retrieval

This repository provides Python classes for retrieving some radiation and climate variables using **Google Earth Engine**.
The said two main classes are:  
- **Solicitud** → defines the request (location, variables, date).  
- **DataFetcher** → extracts values from Earth Engine datasets and returns them as dictionaries or Pandas DataFrames.

---

## 📂 Project Structure
- `retrieval_classes.py` → Core classes (`Solicitud`, `DataFetcher`).
- `demo.py` → Example usage of the retrieval workflow.
- `requirements.txt` → Dependencies (`earthengine-api`, `pandas`).

---

## ⚡ Features
- Retrieve multiple variables (solar radiation, temperature, precipitation, wind, humidity, aerosols, elevation, etc.).
- Support for **daily**, **hourly**, and **static** datasets.
- Automatic handling of wind speed, wind direction, relative humidity, and temperature conversions.
- Export results to Pandas DataFrame for analysis.

---

## 🚀 Installation
```bash
git clone https://github.com/anappp15/Solar-Climate-Data-Retrieval.git
cd Solar-Climate-Data-Retrieval
pip install -r requirements.txt
```

Make sure you have [Google Earth Engine](https://developers.google.com/earth-engine) initialized:
```bash
earthengine authenticate
```

---

## 📖 Usage

For a complete example, check out the [demo.py](demo.py) file in this repository.

Run it with:
```bash
python demo.py
```
---

## 📌 Notes
- Default date is **7 days ago** to ensure data availability.
- Variables must match keys in `Solicitud.registro_variables`.
- Extend `Solicitud` to add new datasets or bands.
- `DataFetcher.to_dataframe()` includes metadata (lat, lon, date).

- Requests are designed to return **one day of data**.  
- If multiple images exist for that day, the code will either average them or handle the mismatch gracefully.  
- This ensures consistent daily values for analysis.
