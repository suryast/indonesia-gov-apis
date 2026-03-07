# InaRisk — Disaster Risk by Location

## Risk Score by Coordinates

```python
import requests

resp = requests.get("https://inarisk.bnpb.go.id/api/risk/score", params={
    "lat": -6.2088,   # Jakarta
    "lon": 106.8456,
}, timeout=30)
risk = resp.json()
# Returns risk scores per hazard type:
# flood, earthquake, tsunami, volcano, landslide, drought, forest fire
```

## Historical Disaster Events

```python
resp = requests.get("https://data.bnpb.go.id/api/3/action/package_search", params={
    "q": "banjir",  # flood
    "rows": 10,
}, timeout=30)
# CKAN-based portal — same pattern as data.go.id
```

## WMS Layers

InaRisk also serves WMS map layers for visualization:
- Flood risk zones
- Earthquake-prone areas
- Tsunami evacuation routes
- Volcanic hazard zones

## Gotchas
- No auth needed for REST API
- Coordinate-based queries — lat/lon in decimal degrees
- Complements BMKG for real-time vs. historical risk
- data.bnpb.go.id uses CKAN (same API pattern as data.go.id)
