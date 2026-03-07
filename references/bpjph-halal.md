# BPJPH Halal Certification

## Endpoints

| Endpoint | URL | Method | Auth |
|----------|-----|--------|------|
| Penyelia Search | `https://cmsbl.halal.go.id/api/search/data_penyelia` | POST | None |
| General Search | `https://cmsbl.halal.go.id/api/search` | POST | None |
| Certificate List | `https://prod-api-si.halal.go.id/api/v2/dashboard/halal-certificate-list` | GET | None |

## Search

```python
import requests

resp = requests.post("https://cmsbl.halal.go.id/api/search/data_penyelia", json={
    "nama_penyelia": "Ahmad",  # Supervisor name prefix filter
    "start": 0,
    "length": 100,             # Max 100
}, headers={"Content-Type": "application/json"}, timeout=30)

data = resp.json()
# data["recordsTotal"] = total matching
# data["data"] = list of businesses
```

## Response Fields

| Field | Description |
|-------|-------------|
| `nama` | Business name |
| `alamat` | Address |
| `propinsi` | Province |
| `kota_kab` | City/regency |
| `nama_penyelia_halal` | Halal supervisor |
| `nomor_sertifikat` | Certificate number |
| `berlaku_sampai` | Expiry date |

## Bulk Scraping

Use letter prefixes for `nama_penyelia` (A-Z) to partition the dataset. General search degrades at offset >100K.

```python
import string, time
for letter in string.ascii_uppercase:
    offset = 0
    while True:
        resp = requests.post(url, json={"nama_penyelia": letter, "start": offset, "length": 100}, ...)
        records = resp.json().get("data", [])
        if not records: break
        offset += len(records)
        time.sleep(1)
```

Rate: ~116K records/hour. Total dataset: ~1.98M businesses.

## Gotchas
- No auth needed
- Duplicates exist — deduplicate by certificate number
- Some records have encoding issues
- Data can lag behind actual certification status
