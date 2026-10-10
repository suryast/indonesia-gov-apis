#!/usr/bin/env python3
"""Bounded, local-only HTTP observations; history.json is the publication unit."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import fcntl
from functools import lru_cache
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

DATA_DIR = Path(__file__).resolve().parent / "data"

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
    ('big', 'BIG Geoservices (ArcGIS)', 'https://geoservices.big.go.id/rbi/rest/services?f=json', 'BIG', 1),
    ("bnpb", "BNPB Disaster", "https://dibi.bnpb.go.id", "BNPB", 1),
    # Tier 2
    ("bpjph-old", "BPJPH Halal (old)", "https://sertifikasi.halal.go.id", "BPJPH", 2),
    ("bpjph-new", "BPJPH Halal (new)", "https://bpjph.halal.go.id", "BPJPH", 2),
    ("bpom", "BPOM Products", "https://cekbpom.pom.go.id", "BPOM", 2),
    ("ahu", "AHU Company Registry", "https://ahu.go.id", "AHU", 2),
    ("oss", "OSS / NIB", "https://oss.go.id", "BKPM", 2),
    ("ojk-registry", "OJK Registry", "https://sikapiuangmu.ojk.go.id", "OJK", 2),
    ("ojk-api", "OJK API", "https://api.ojk.go.id", "OJK", 2),
    ("lhkpn", "KPK e-LHKPN", "https://elhkpn.kpk.go.id", "KPK", 2),
    ('putusan-mk', 'Putusan MK', 'https://www.mkri.id/perkara/persidangan/putusan', 'MK', 2),
    ("ksei", "KSEI Statistics", "https://www.ksei.co.id", "KSEI", 2),
    ("ppid", "e-PPID", "https://ppid.kemenkeu.go.id", "Kemenkeu", 2),
    ("pajak", "Pajak / DJP", "https://ereg.pajak.go.id", "DJP", 2),
    # Tier 3
    ('jakarta', 'Satu Data Jakarta', 'https://satudata.jakarta.go.id', 'DKI Jakarta', 3),
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
    ('kemdikbud', 'Dapodik Kemendikdasmen', 'https://dapo.kemendikdasmen.go.id/pencarian', 'Kemendikdasmen', 4),
    ("kemenkes", "Kemenkes Health", "https://sirs.kemkes.go.id", "Kemenkes", 4),
    ("kemenag", "Kemenag", "https://simas.kemenag.go.id", "Kemenag", 4),
    # Tier 5
    ("occrp", "OCCRP Aleph", "https://aleph.occrp.org", "OCCRP", 5),
    ("opencorporates", "OpenCorporates", "https://opencorporates.com", "OpenCorporates", 5),
    ("eiti", "EITI Indonesia", "https://eiti.esdm.go.id", "EITI/ESDM", 5),
    ("ahu-bo", "AHU-BO", "https://ahu.go.id/pencarian/pencarian-bo", "AHU", 5),
    ("icw", "ICW Corruption Watch", "https://antikorupsi.org", "ICW", 5),
    # Tier 6
    ("ojk-sikepo", "OJK SIKEPO (OJK root-only probe)", "https://ojk.go.id", "OJK", 6),
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
    ("cmsbl-halal", "Legacy cmsbl Halal (unverified web endpoint)", "https://cmsbl.halal.go.id", "BPJPH (legacy attribution)", 8),
    ('inaproc-api', 'INAPROC Data API (docs)', 'https://data.inaproc.id/docs/dokumentasi/guides/migration-from-isb', 'LKPP', 9),
    ('inaproc-satudata', 'Satu Data eProc', 'https://inaproc.id/satudata', 'LKPP', 9),
    ('sirup', 'SIRUP / RUP', 'https://sirup.inaproc.id', 'LKPP', 9),
    ('bgn-sppg', 'SPPG Operasional (MBG)', 'https://www.bgn.go.id/operasional-sppg', 'BGN', 9),
    ('cekbansos', 'Cek Bansos', 'https://cekbansos.kemensos.go.id/', 'Kemensos', 9),
    ('djpk-sikd', 'Portal Data SIKD (APBD)', 'https://djpk.kemenkeu.go.id/portal/data/apbd', 'DJPK Kemenkeu', 9),
    ('pihps', 'PIHPS Harga Pangan', 'https://www.bi.go.id/hargapangan', 'BI', 9),
    ('panelharga', 'Panel Harga Pangan', 'https://panelharga.badanpangan.go.id/', 'Bapanas', 9),
    ('sdi-ckan', 'Satu Data CKAN API', 'https://katalog.data.go.id/api/3/action/package_search?rows=0', 'Bappenas', 10),
    ('bmkg-forecast', 'BMKG Forecast API', 'https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.71.03.1001', 'BMKG', 10),
    ('bnpb-ckan', 'Satu Data Bencana (CKAN)', 'https://data.bnpb.go.id/api/3/action/status_show', 'BNPB', 10),
    ('referensi-pendidikan', 'Data Referensi Pendidikan', 'https://referensi.data.kemendikdasmen.go.id/', 'Kemendikdasmen', 10),
    ('sipp-jakut', 'SIPP PN Jakarta Utara', 'https://sipp.pn-jakartautara.go.id/', 'MA', 11),
    ('sipp-sleman', 'SIPP PN Sleman', 'https://sipp.pn-sleman.go.id/', 'MA', 11),
    ('sipp-medan', 'SIPP PN Medan', 'https://sipp.pn-medankota.go.id/', 'MA', 11),
    ('sipp-palembang', 'SIPP PN Palembang', 'https://sipp.pn-palembang.go.id/', 'MA', 11),
    ('sipp-semarang', 'SIPP PN Semarang', 'https://sipp.pn-semarangkota.go.id/', 'MA', 11),
    ('jdihn', 'JDIHN', 'https://jdihn.go.id/', 'BPHN', 11),
]

EXPECT = {'big': '"services"', 'putusan-mk': 'putusan', 'inaproc-api': 'inaproc', 'inaproc-satudata': 'daftar hitam', 'bgn-sppg': 'sppg', 'cekbansos': 'kemensos', 'djpk-sikd': 'sikd', 'sdi-ckan': '"success": true', 'bmkg-forecast': '"lokasi"', 'bnpb-ckan': '"success": true', 'referensi-pendidikan': 'npsn', 'sipp-jakut': 'pembaharuan data', 'sipp-sleman': 'pembaharuan data', 'sipp-medan': 'pembaharuan data', 'sipp-palembang': 'pembaharuan data', 'sipp-semarang': 'pembaharuan data'}
BODY_BYTE_CAP = 262144

def classify(code: int, exit_code: int = 0) -> str:
    """Transport failures take precedence, even if a redirect returned HTTP."""
    if exit_code:
        if exit_code == 6:
            return "dns_error"
        if exit_code == 5:
            return "proxy_error"
        if exit_code == 28:
            return "timeout"
        if exit_code in {35, 51, 53, 54, 58, 59, 60, 64, 66, 77, 80, 82, 83, 90, 91, 98}:
            return "tls_error"
        if exit_code == 47:
            return "redirect_error"
        if exit_code in {7, 16, 18, 52, 55, 56, 92, 95, 96}:
            return "network_error"
        return "probe_error"
    if 200 <= code < 400:
        return "up"
    if code == 403:
        return "blocked"
    return "http_error" if 100 <= code <= 599 else "probe_error"


@lru_cache(maxsize=1)
def curl_supports_body_cap():
    """curl >=8.4 bounds unknown-size downloads too; older curl skips body checks."""
    try:
        result = subprocess.run(['curl', '--disable', '--version'], stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, text=True, timeout=5, check=True)
        version = re.match(r'curl (\d+)\.(\d+)\.(\d+)', result.stdout)
        return bool(version and tuple(map(int, version.groups())) >= (8, 4, 0))
    except (OSError, subprocess.SubprocessError):
        return False


def check_url_local(url: str, timeout: float = 10, expect: str | None = None) -> dict:
    """Inspect only bounded static public markers; never publish body or raw errors."""
    code, latency, exit_code = 0, 0, None
    content = 'unverified'
    collect = bool(expect) and curl_supports_body_cap()
    # Private temporary directory; every exit, including timeout, removes the body.
    with tempfile.TemporaryDirectory(prefix='status-body-') as temporary:
        body_path = Path(temporary) / 'body'
        args = ['curl', '--disable', '--silent', '--output', str(body_path) if collect else os.devnull,
                '--write-out', '%{http_code}|%{time_total}',
                '--location', '--max-redirs', '3', '--max-time', str(timeout),
                '--connect-timeout', str(timeout), '--proto', '=http,https',
                '--proto-redir', '=https' if url.startswith('https:') else '=http,https']
        if collect:
            args.extend(['--max-filesize', str(BODY_BYTE_CAP)])
        args.extend(['--', url])
        try:
            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                    text=True, timeout=timeout + 2)
            exit_code = result.returncode
            parts = result.stdout.strip().split('|')
            try:
                code, seconds = int(parts[0]), float(parts[1])
                if len(parts) != 2 or not math.isfinite(seconds) or seconds < 0 or not 0 <= code <= 599:
                    raise ValueError('Malformed curl output')
                latency = round(seconds * 1000)
            except (ValueError, IndexError):
                code, latency = 0, 0
            status = classify(code, exit_code)
            if collect and exit_code == 63 and 200 <= code < 400:
                # A capped response proves HTTP reachability, not marker absence.
                status = 'up'
            elif collect and status == 'up':
                with body_path.open('rb') as body:
                    raw = body.read(BODY_BYTE_CAP + 1)
                if len(raw) <= BODY_BYTE_CAP and expect:
                    content = 'matched' if expect.casefold() in raw.decode('utf-8', errors='replace').casefold() else 'missing'
                    if content == 'missing':
                        status = 'degraded'
        except subprocess.TimeoutExpired:
            status = 'timeout'
        except OSError:
            status = 'probe_error'
    observation = {'http_code': code, 'latency_ms': latency, 'status': status, 'curl_exit_code': exit_code}
    if expect:
        observation['content_check'] = content
    return observation


def overall_status(statuses):
    observed = set(statuses) - {"skip"}
    return next(iter(observed)) if len(observed) == 1 else "mixed" if observed else "skip"


def read_history(directory):
    """Validate retained snapshots without normalizing historical evidence."""
    history = {}
    for path in sorted(Path(directory).glob("????-??-??.json")):
        previous = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(previous, dict)
                or not isinstance(previous.get("portals"), dict)
                or not previous["portals"]):
            raise ValueError("Invalid historical snapshot")
        timestamp = previous.get("checked_at")
        if (not isinstance(timestamp, str)
                or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", timestamp)
                or datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date().isoformat() != path.stem):
            raise ValueError("Invalid historical timestamp")
        # Legacy snapshots omit date; checked_at above must still match the filename.
        # An explicit null/wrong date is never treated as a legacy omission.
        if "date" in previous and previous["date"] != path.stem:
            raise ValueError("Invalid historical snapshot date")
        history[path.stem] = previous
    return history


def publish(results, directory):
    """Stage all JSON before replacing files; publish self-contained history last.

    Caller serializes writers with .check.lock. Readers use history.json only.
    Separate compatibility files are atomic individually, not a multi-file transaction.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    day = results["date"]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise ValueError("Invalid snapshot date")
    history = read_history(directory)
    history[day] = results
    history = dict(sorted(history.items()))
    outputs = {f"{day}.json": results, "latest.json": history[max(history)],
               "index.json": list(history), "history.json": history}
    staged = []
    try:
        for name, value in outputs.items():
            # Keep aggregate downloads compact; individual snapshots stay readable.
            indent = None if name in {"history.json", "index.json"} else 2
            payload = json.dumps(value, ensure_ascii=False, allow_nan=False, indent=indent) + "\n"
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory, suffix=".tmp", delete=False) as file:
                staged.append((Path(file.name), directory / name))
                file.write(payload)
                file.flush()
                os.fsync(file.fileno())
        for temporary, target in staged:
            os.replace(temporary, target)
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)


def positive_timeout(value):
    number = float(value)
    if not math.isfinite(number) or not 0 < number <= 120:
        raise argparse.ArgumentTypeError("timeout must be greater than 0 and at most 120 seconds")
    return number


def workers_count(value):
    number = int(value)
    if not 1 <= number <= 32:
        raise argparse.ArgumentTypeError("workers must be between 1 and 32")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--timeout", type=positive_timeout, default=10)
    parser.add_argument("--workers", type=workers_count, default=4)
    parser.add_argument("--source-location", default=os.environ.get("STATUS_SOURCE_LOCATION", "Not configured"))
    parser.add_argument("--source-provider", default=os.environ.get("STATUS_SOURCE_PROVIDER", "Not configured"))
    parser.add_argument("--source-type", default=os.environ.get("STATUS_SOURCE_TYPE", "Not configured"))
    args = parser.parse_args(argv)
    try:
        # curl absence is an infrastructure failure, not an outage of every portal.
        subprocess.run(["curl", "--disable", "--version"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with (args.output_dir / ".check.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Fail before any endpoint requests; publish revalidates before writing.
            read_history(args.output_dir)
            now = datetime.now(timezone.utc)
            results = {"schema_version": 2, "date": now.strftime("%Y-%m-%d"),
                       "checked_at": now.isoformat(),
                       "sources": {"local": {"location": args.source_location, "provider": args.source_provider,
                                             "type": args.source_type, "available": True}}, "portals": {}}
            def observe(portal):
                pid, name, url, agency, tier = portal
                observation = check_url_local(url, args.timeout, expect=EXPECT.get(pid))
                return pid, {"name": name, "url": url, "agency": agency, "tier": tier,
                             "status": observation["status"], "observations": {"local": observation}}
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                for pid, portal in pool.map(observe, PORTALS):
                    results["portals"][pid] = portal
                    print(f"{pid}: {portal['status']}")
            if any(p["status"] == "probe_error" for p in results["portals"].values()):
                raise ValueError("Local probe failed; snapshot not published")
            publish(results, args.output_dir)
        print(f"Published {len(results['portals'])} observations and history")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError):
        # No raw exception content: paths, stderr or credential details may be sensitive.
        print("Status check failed: probe, lock, or output validation/publication error; no deployment should follow.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
