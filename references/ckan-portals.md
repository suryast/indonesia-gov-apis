# CKAN Open Data Portals

One pattern works for all Indonesian CKAN portals.

## Portals

| Portal | URL | Scope |
|--------|-----|-------|
| data.go.id | `data.go.id/api/3/action` | National (10K+ datasets) |
| Satu Data Jakarta | `satudata.jakarta.go.id/api/3/action` | DKI Jakarta (best regional) |
| Open Data Jabar | `opendata.jabarprov.go.id/api/3/action` | Jawa Barat |
| Open Data Jatim | `opendata.jatimprov.go.id/api/3/action` | Jawa Timur |
| Satu Data Surabaya | `satudata.surabaya.go.id/api/3/action` | Surabaya |
| Open Data Bandung | `opendata.bandung.go.id/api/3/action` | Bandung |

## Search Datasets

```python
import requests

PORTAL = "data.go.id"  # Swap for any portal above
resp = requests.get(f"https://{PORTAL}/api/3/action/package_search", params={
    "q": "keuangan",     # Search in Indonesian
    "rows": 10,
    "start": 0,
    "sort": "score desc",
}, timeout=30)

for ds in resp.json()["result"]["results"]:
    print(f"{ds['title']} ({ds.get('organization',{}).get('title','N/A')})")
    for r in ds.get("resources", []):
        print(f"  └ {r['format']}: {r['url']}")
```

## Get Dataset by ID

```python
resp = requests.get(f"https://{PORTAL}/api/3/action/package_show", params={
    "id": "dataset-name-or-id",
}, timeout=30)
```

## Datastore Search (Structured Query)

```python
resp = requests.get(f"https://{PORTAL}/api/3/action/datastore_search", params={
    "resource_id": "resource-uuid",
    "q": "keyword",
    "limit": 100,
}, timeout=30)
```

## Common Keywords (Indonesian)

| English | Indonesian |
|---------|-----------|
| Finance | keuangan |
| Health | kesehatan |
| Population | penduduk |
| Education | pendidikan |
| Infrastructure | infrastruktur |
| Agriculture | pertanian |
| Tourism | pariwisata |
| Budget | anggaran |

## Gotchas
- No auth required
- Search queries should be in Indonesian
- ~100 req/min on most portals
- Many datasets are stale (last updated 2020-2022)
- Some resource download URLs are broken
- CSV encoding: mostly UTF-8, some Windows-1252
