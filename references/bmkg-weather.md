# BMKG Weather & Earthquake Data

## Earthquake — Latest

```python
import requests

resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", timeout=30)
q = resp.json()["Infogempa"]["gempa"]
print(f"M{q['Magnitude']} | {q['Wilayah']} | {q['Tanggal']} {q['Jam']} | Depth: {q['Kedalaman']}")
```

## Earthquake — Recent 15

```python
resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json", timeout=30)
for q in resp.json()["Infogempa"]["gempa"]:
    print(f"M{q['Magnitude']} | {q['Wilayah']} | {q['Tanggal']} {q['Jam']}")
```

## Earthquake — M5.0+ (Felt)

```python
resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.json", timeout=30)
```

## Weather Forecast

XML format, 3-day forecast at kelurahan/desa level:

```python
resp = requests.get("https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-DKIJakarta.xml", timeout=30)
# Parse XML — contains humidity, temperature, wind, weather code per area
```

### Province Codes

| Code | Province |
|------|----------|
| `DKIJakarta` | DKI Jakarta |
| `JawaBarat` | Jawa Barat |
| `JawaTengah` | Jawa Tengah |
| `JawaTimur` | Jawa Timur |
| `Bali` | Bali |
| `SulawesiSelatan` | Sulawesi Selatan |
| `KalimantanTimur` | Kalimantan Timur |
| `SumateraUtara` | Sumatera Utara |

## Endpoints Summary

| Endpoint | Data | Format |
|----------|------|--------|
| `/DataMKG/TEWS/autogempa.json` | Latest earthquake | JSON |
| `/DataMKG/TEWS/gempaterkini.json` | Recent 15 earthquakes | JSON |
| `/DataMKG/TEWS/gempadirasakan.json` | Felt earthquakes | JSON |
| `/DataMKG/MEWS/DigitalForecast/DigitalForecast-{Province}.xml` | Weather forecast | XML |

## Gotchas
- No auth, no rate limit stated
- Real-time data — earthquakes appear within minutes
- Weather XML is verbose — use `xml.etree.ElementTree` to parse
- Province codes are CamelCase, no spaces
