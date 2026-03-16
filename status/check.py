#!/usr/bin/env python3
"""Daily portal status checker. Checks from AU (local) and ID (Jakarta SSH).
Writes results to status/data/YYYY-MM-DD.json."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

import os

# Jakarta proxy box for in-country checks
# In GH Actions: uses SSH config alias "jakarta" (key from secret)
# Locally: direct SSH to polybot@117.53.46.31
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
    ("big", "BIG Geospatial", "https://tanahair.indonesia.go.id", "BIG", 1),
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
    ("putusan-mk", "Putusan MK", "https://putusan.mahkamahkonstitusi.go.id", "MK", 2),
    ("ksei", "KSEI Statistics", "https://www.ksei.co.id", "KSEI", 2),
    ("ppid", "e-PPID", "https://ppid.kemenkeu.go.id", "Kemenkeu", 2),
    ("pajak", "Pajak / DJP", "https://ereg.pajak.go.id", "DJP", 2),
    # Tier 3
    ("jakarta", "Satu Data Jakarta", "https://data.jakarta.go.id", "DKI Jakarta", 3),
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
    ("kemdikbud", "Kemendikdasmen", "https://dapo.kemdikbud.go.id", "Pendidikan", 4),
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
]


def classify(code: int) -> str:
    if code == 0:
        return "dns_dead"
    elif 200 <= code < 400:
        return "up"
    elif code == 403:
        return "blocked"
    else:
        return "error"


def check_url_local(url: str, timeout: int = 10) -> dict:
    """Check a URL from local machine (Sydney AU)."""
    try:
        r = subprocess.run(
            [
                "curl", "-s", "-o", "/dev/null",
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

    return {"http_code": code, "latency_ms": round(latency * 1000), "status": classify(code)}


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

    jakarta_ok = check_jakarta_available()
    print(f"Jakarta SSH: {'✅ available' if jakarta_ok else '❌ unreachable'}\n")

    results = {
        "date": today,
        "checked_at": ts,
        "sources": {
            "au": {"location": "Sydney, Australia", "type": "datacenter", "provider": "DigitalOcean"},
            "id": {"location": "Jakarta, Indonesia", "type": "datacenter", "provider": "CloudKilat",
                    "available": jakarta_ok},
        },
        "portals": {},
    }

    for pid, name, url, agency, tier in PORTALS:
        print(f"  {name}...", end=" ", flush=True)

        au = check_url_local(url)
        id_result = check_url_jakarta(url) if jakarta_ok else {"http_code": -1, "latency_ms": 0, "status": "skip"}

        # Determine overall status
        au_s = au["status"]
        id_s = id_result["status"]

        if au_s == "up" or id_s == "up":
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
            "blocked": "⚠️", "dns_dead": "❌", "down": "❌",
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
    total = len(statuses)
    print(f"\n✅ {up} up | 🌏 {geo} geo-blocked | ⚠️ {blocked} CF challenge | ❌ {dead} DNS dead | ❌ {down} down | Total: {total}")


if __name__ == "__main__":
    main()
