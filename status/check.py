#!/usr/bin/env python3
"""Daily portal status checker. Checks from AU and, when enabled, Jakarta.
Writes results to status/data/YYYY-MM-DD.json."""

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

import os

# The Jakarta probe is offline. Keep it opt-in so routine runs do not attempt a
# connection or infer geo-blocking from missing ID observations.
JAKARTA_PROBE_ENABLED = os.environ.get("JAKARTA_PROBE_ENABLED") == "1"
JAKARTA_SSH = "jakarta" if os.environ.get("JAKARTA_SSH_KEY") else "polybot@117.53.46.31"

PORTALS = [
    # (id, name, url, agency, tier)
    ("data-go-id", "Satu Data (SDI)", "https://data.go.id", "Bappenas", 1),
    ("bps", "BPS Statistics", "https://webapi.bps.go.id", "BPS", 1),
    ("bmkg", "BMKG Weather", "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", "BMKG", 1),
    ("idx", "IDX / BEI", "https://idx.co.id", "BEI", 1),
    ("djpb-treasury", "DJPB Treasury", "https://data.treasury.kemenkeu.go.id", "Kemenkeu", 1),
    ("jdih-bpk", "JDIH BPK", "https://jdih.bpk.go.id", "BPK", 1),
    ("putusan-ma", "Putusan MA", "https://putusan3.mahkamahagung.go.id", "MA", 1),
    ("lpse", "LPSE / INAPROC", "https://spse.inaproc.id", "LKPP", 1),
    ("apbn", "Portal APBN", "https://data.anggaran.kemenkeu.go.id", "Kemenkeu", 1),
    ("bi", "Bank Indonesia", "https://www.bi.go.id", "BI", 1),
    # Repointed 2026-10: tanahair.indonesia.go.id timed out; boundaries now served via ArcGIS REST
    ("big", "BIG Geoservices (ArcGIS)", "https://geoservices.big.go.id/rbi/rest/services?f=json", "BIG", 1),
    ("bnpb", "BNPB Disaster", "https://dibi.bnpb.go.id", "BNPB", 1),
    # Tier 2
    ("bpjph-old", "BPJPH Halal (old)", "https://sertifikasi.halal.go.id", "BPJPH", 2),
    ("bpjph-new", "BPJPH Halal (new)", "https://bpjph.halal.go.id", "BPJPH", 2),
    ("bpom", "BPOM Products", "https://cekbpom.pom.go.id", "BPOM", 2),
    ("ahu", "AHU Company Registry", "https://ahu.go.id", "Kemenkumham", 2),
    ("oss", "OSS / NIB", "https://oss.go.id", "BKPM", 2),
    ("ojk-registry", "OJK Registry", "https://sikapiuangmu.ojk.go.id", "OJK", 2),
    ("ojk-api", "OJK API", "https://api.ojk.go.id", "OJK", 2),
    ("lhkpn", "KPK e-LHKPN", "https://elhkpn.kpk.go.id", "KPK", 2),
    # Repointed 2026-10: putusan.mahkamahkonstitusi.go.id is DNS dead; rulings moved to mkri.id
    ("putusan-mk", "Putusan MK", "https://www.mkri.id/perkara/persidangan/putusan", "MK", 2),
    ("ksei", "KSEI Statistics", "https://www.ksei.co.id", "KSEI", 2),
    ("ppid", "e-PPID", "https://ppid.kemenkeu.go.id", "Kemenkeu", 2),
    ("pajak", "Pajak / DJP", "https://ereg.pajak.go.id", "DJP", 2),
    # Tier 3
    # Repointed 2026-10: Open Data portal moved to Satu Data Jakarta (Feb 2023)
    ("jakarta", "Satu Data Jakarta", "https://satudata.jakarta.go.id", "DKI Jakarta", 3),
    ("jabar", "Open Data Jabar", "https://opendata.jabarprov.go.id", "Jawa Barat", 3),
    ("jatim", "Open Data Jatim", "https://data.jatimprov.go.id", "Jawa Timur", 3),
    ("surabaya", "Satu Data Surabaya", "https://data.surabaya.go.id", "Surabaya", 3),
    ("bandung", "Open Data Bandung", "https://data.bandung.go.id", "Bandung", 3),
    ("bali", "Open Data Bali", "https://data.baliprov.go.id", "Bali", 3),
    # Tier 4
    ("kemnaker", "Kemnaker", "https://kemnaker.go.id", "Ketenagakerjaan", 4),
    ("komdigi", "Komdigi", "https://komdigi.go.id", "Komunikasi Digital", 4),
    ("esdm", "ESDM Energy", "https://www.esdm.go.id", "ESDM", 4),
    ("kkp", "KKP Fisheries", "https://kkp.go.id", "KKP", 4),
    ("atr-bpn", "ATR/BPN Land", "https://www.atrbpn.go.id", "ATR/BPN", 4),
    # Repointed 2026-10: dapo.kemdikbud.go.id is DNS dead after the 2024 Kemdikbud split
    ("kemdikbud", "Dapodik Kemendikdasmen", "https://dapo.kemendikdasmen.go.id/pencarian", "Kemendikdasmen", 4),
    ("kemenkes", "Kemenkes Health", "https://sirs.kemkes.go.id", "Kemenkes", 4),
    ("kemenag", "Kemenag", "https://simas.kemenag.go.id", "Kemenag", 4),
    # Tier 5
    ("occrp", "OCCRP Aleph", "https://aleph.occrp.org", "OCCRP", 5),
    ("opencorporates", "OpenCorporates", "https://opencorporates.com", "OpenCorporates", 5),
    ("eiti", "EITI Indonesia", "https://eiti.esdm.go.id", "EITI/ESDM", 5),
    ("ahu-bo", "AHU-BO", "https://ahu.go.id/pencarian/pencarian-bo", "Kemenkumham", 5),
    ("icw", "ICW Corruption Watch", "https://antikorupsi.org", "ICW", 5),
    # Tier 6
    ("ojk-sikepo", "OJK SIKEPO", "https://ojk.go.id", "OJK", 6),
    ("satgas-waspada", "Satgas Waspada", "https://sikapiuangmu.ojk.go.id", "OJK", 6),
    ("ksei-stats", "KSEI Investor Stats", "https://www.ksei.co.id/publications", "KSEI", 6),
    ("djpb-budget", "DJPB Budget", "https://djpb.kemenkeu.go.id", "DJPB", 6),
    # Tier 7
    ("lapor", "LAPOR!", "https://www.lapor.go.id", "KemenPANRB", 7),
    ("indolii", "IndoLII", "https://www.indolii.org", "USAID", 7),
    ("geoportal", "Geoportal One Map", "https://tanahair.indonesia.go.id", "BIG/KLHK", 7),
    ("inarisk", "SIGAP / InaRisk", "https://inarisk.bnpb.go.id", "BNPB", 7),
    ("pasal-id", "pasal.id", "https://pasal.id", "Community", 7),
    # Tier 8: New additions (2026-03-29)
    ("kpu", "KPU Elections", "https://www.kpu.go.id", "KPU", 8),
    ("simbg", "SIMBG Building Permits", "https://simbg.pu.go.id", "Kemen PUPR", 8),
    ("coretax", "CoreTax DJP", "https://coretaxdjp.pajak.go.id", "DJP", 8),
    ("satusehat", "SATUSEHAT", "https://satusehat.kemkes.go.id", "Kemenkes", 8),
    ("cmsbl-halal", "BPJPH Halal API", "https://cmsbl.halal.go.id", "BPJPH", 8),
    # Tier 9: Procurement & program data (2026-10)
    ("inaproc-api", "INAPROC Data API (docs)", "https://data.inaproc.id/docs/dokumentasi/guides/migration-from-isb", "LKPP", 9),
    ("inaproc-satudata", "Satu Data eProc", "https://inaproc.id/satudata", "LKPP", 9),
    ("sirup", "SIRUP / RUP", "https://sirup.inaproc.id", "LKPP", 9),
    ("bgn-sppg", "SPPG Operasional (MBG)", "https://www.bgn.go.id/operasional-sppg", "BGN", 9),
    ("cekbansos", "Cek Bansos", "https://cekbansos.kemensos.go.id/", "Kemensos", 9),
    ("djpk-sikd", "Portal Data SIKD (APBD)", "https://djpk.kemenkeu.go.id/portal/data/apbd", "DJPK Kemenkeu", 9),
    ("pihps", "PIHPS Harga Pangan", "https://www.bi.go.id/hargapangan", "BI", 9),
    ("panelharga", "Panel Harga Pangan", "https://panelharga.badanpangan.go.id/", "Bapanas", 9),
    # Tier 10: Machine-readable APIs & catalogues (2026-10)
    ("sdi-ckan", "Satu Data CKAN API", "https://katalog.data.go.id/api/3/action/package_search?rows=0", "Bappenas", 10),
    ("bmkg-forecast", "BMKG Forecast API", "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.71.03.1001", "BMKG", 10),
    ("bnpb-ckan", "Satu Data Bencana (CKAN)", "https://data.bnpb.go.id/api/3/action/status_show", "BNPB", 10),
    ("referensi-pendidikan", "Data Referensi Pendidikan", "https://referensi.data.kemendikdasmen.go.id/", "Kemendikdasmen", 10),
    # Tier 11: Courts & law (2026-10). SIPP runs one instance per court; sample high-volume ones.
    ("sipp-jakut", "SIPP PN Jakarta Utara", "https://sipp.pn-jakartautara.go.id/", "MA", 11),
    ("sipp-sleman", "SIPP PN Sleman", "https://sipp.pn-sleman.go.id/", "MA", 11),
    ("sipp-medan", "SIPP PN Medan", "https://sipp.pn-medankota.go.id/", "MA", 11),
    ("sipp-palembang", "SIPP PN Palembang", "https://sipp.pn-palembang.go.id/", "MA", 11),
    ("sipp-semarang", "SIPP PN Semarang", "https://sipp.pn-semarangkota.go.id/", "MA", 11),
    ("jdihn", "JDIHN", "https://jdihn.go.id/", "BPHN", 11),
]

# Optional content checks: a 2xx/3xx response only counts as "up" if the body
# contains this text (case-insensitive). Catches error pages, challenge pages and
# empty API responses served with HTTP 200. Misses are reported as "degraded".
EXPECT = {
    "big": '"services"',
    "putusan-mk": "putusan",
    "inaproc-api": "inaproc",
    "inaproc-satudata": "daftar hitam",
    "bgn-sppg": "sppg",
    "cekbansos": "kemensos",
    "djpk-sikd": "sikd",
    "sdi-ckan": '"success": true',
    "bmkg-forecast": '"lokasi"',
    "bnpb-ckan": '"success": true',
    "referensi-pendidikan": "npsn",
    "sipp-jakut": "pembaharuan data",
    "sipp-sleman": "pembaharuan data",
    "sipp-medan": "pembaharuan data",
    "sipp-palembang": "pembaharuan data",
    "sipp-semarang": "pembaharuan data",
}


def classify(code: int) -> str:
    if code == 0:
        return "dns_dead"
    elif 200 <= code < 400:
        return "up"
    elif code == 403:
        return "blocked"
    else:
        return "error"


def check_url_local(url: str, timeout: int = 10, expect: str | None = None) -> dict:
    """Check a URL from the local runner. If `expect` is set, also check the body for it."""
    body_file = tempfile.NamedTemporaryFile(delete=False) if expect else None
    try:
        r = subprocess.run(
            [
                "curl", "-s", "-o", body_file.name if body_file else "/dev/null",
                "-w", "%{http_code}|%{time_total}",
                "-L", "--max-redirs", "3", "--max-time", str(timeout),
                url,
            ],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        parts = r.stdout.strip().split("|")
        code = int(parts[0]) if parts[0].isdigit() else 0
        latency = float(parts[1]) if len(parts) > 1 else 0
    except Exception:
        code, latency = 0, 0

    result = {"http_code": code, "latency_ms": round(latency * 1000), "status": classify(code)}
    if body_file:
        body_file.close()
        body = Path(body_file.name).read_bytes().decode("utf-8", errors="replace")
        os.unlink(body_file.name)
        result["content_ok"] = expect.lower() in body.lower()
    return result


def check_url_jakarta(url: str, timeout: int = 10) -> dict:
    """Check a URL from Jakarta via SSH."""
    cmd = f"curl -s -o /dev/null -w '%{{http_code}}|%{{time_total}}' -L --max-redirs 3 --max-time {timeout} '{url}'"
    try:
        r = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no", JAKARTA_SSH, cmd],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        raw = r.stdout.strip().replace("'", "")
        parts = raw.split("|")
        code = int(parts[0]) if parts[0].isdigit() else 0
        latency = float(parts[1]) if len(parts) > 1 else 0
    except Exception:
        code, latency = 0, 0

    return {"http_code": code, "latency_ms": round(latency * 1000), "status": classify(code)}


def check_jakarta_available() -> bool:
    """Test if Jakarta SSH is reachable."""
    try:
        r = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", JAKARTA_SSH, "echo ok"],
            capture_output=True, text=True, timeout=10,
        )
        return r.stdout.strip() == "ok"
    except Exception:
        return False


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ts = datetime.now(timezone.utc).isoformat()

    jakarta_ok = JAKARTA_PROBE_ENABLED and check_jakarta_available()
    jakarta_state = "✅ available" if jakarta_ok else "⏭️ unavailable (skipped)"
    print(f"Jakarta SSH: {jakarta_state}\n")

    results = {
        "date": today,
        "checked_at": ts,
        "sources": {
            # Key stays "au" for history compatibility; label reflects where the check actually ran.
            "au": ({"location": "GitHub Actions (US)", "type": "datacenter", "provider": "GitHub"}
                   if os.environ.get("GITHUB_ACTIONS") == "true" else
                   {"location": "Sydney, Australia", "type": "datacenter", "provider": "DigitalOcean"}),
            "id": {"location": "Jakarta, Indonesia", "type": "datacenter", "provider": "CloudKilat",
                    "available": jakarta_ok},
        },
        "portals": {},
    }

    for pid, name, url, agency, tier in PORTALS:
        print(f"  {name}...", end=" ", flush=True)

        au = check_url_local(url, expect=EXPECT.get(pid))
        id_result = check_url_jakarta(url) if jakarta_ok else {"http_code": -1, "latency_ms": 0, "status": "skip"}

        # Determine overall status
        au_s = au["status"]
        id_s = id_result["status"]

        if id_s == "skip":
            # Jakarta probe unavailable: report the observable AU status only.
            # Do not infer geo-blocking from a missing comparison point.
            overall = au_s if au_s in {"up", "blocked", "dns_dead"} else "down"
        elif au_s == "up" or id_s == "up":
            if au_s == "up" and id_s == "up":
                overall = "up"
            elif au_s != "up" and id_s == "up":
                overall = "geo_blocked_intl"  # works in ID, blocked outside
            else:
                overall = "geo_blocked_id"  # works outside, blocked in ID (rare)
        elif au_s == "blocked" or id_s == "blocked":
            if id_s == "up":
                overall = "geo_blocked_intl"
            elif au_s == "blocked" and id_s == "blocked":
                overall = "blocked"  # CF challenge everywhere
            else:
                overall = "blocked"
        elif au_s == "dns_dead" and id_s == "dns_dead":
            overall = "dns_dead"
        elif au_s == "dns_dead" and id_s == "skip":
            overall = "dns_dead"
        else:
            overall = "down"

        if overall == "up" and au.get("content_ok") is False:
            overall = "degraded"  # responds, but expected content is missing

        portal = {
            "name": name,
            "url": url,
            "agency": agency,
            "tier": tier,
            "status": overall,
            "au": au,
            "id": id_result,
        }
        results["portals"][pid] = portal

        au_icon = {"up": "✅", "blocked": "⚠️", "dns_dead": "❌", "error": "❌"}.get(au_s, "?")
        id_icon = {"up": "✅", "blocked": "⚠️", "dns_dead": "❌", "error": "❌", "skip": "⏭️"}.get(id_s, "?")
        overall_icon = {
            "up": "✅", "geo_blocked_intl": "🌏", "geo_blocked_id": "🔒",
            "blocked": "⚠️", "dns_dead": "❌", "down": "❌", "degraded": "🟡",
        }.get(overall, "?")
        print(f"AU:{au_icon} ID:{id_icon} → {overall_icon} {overall}")

    # Write files
    out = DATA_DIR / f"{today}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nSaved to {out}")

    latest = DATA_DIR / "latest.json"
    latest.write_text(json.dumps(results, indent=2))

    days = sorted(p.stem for p in DATA_DIR.glob("????-??-??.json"))
    (DATA_DIR / "index.json").write_text(json.dumps(days))

    # Summary
    statuses = [p["status"] for p in results["portals"].values()]
    up = statuses.count("up")
    geo = statuses.count("geo_blocked_intl") + statuses.count("geo_blocked_id")
    blocked = statuses.count("blocked")
    dead = statuses.count("dns_dead")
    down = statuses.count("down")
    degraded = statuses.count("degraded")
    total = len(statuses)
    print(f"\n✅ {up} up | 🌏 {geo} geo-blocked | ⚠️ {blocked} CF challenge | ❌ {dead} DNS dead | ❌ {down} down | 🟡 {degraded} degraded | Total: {total}")


if __name__ == "__main__":
    main()
