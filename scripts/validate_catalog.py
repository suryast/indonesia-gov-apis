#!/usr/bin/env python3
"""Validate exact documentation coverage offline, not endpoint availability.

Catalog v1 is deliberately dependency-free. URL checks are syntactic; live
observations belong in dated evidence, never in this deterministic gate.
"""
import argparse
import ast
from collections import Counter
from datetime import date
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit

TIERS = {f"tier{i}" for i in range(1, 9)} | {"other", "reference"}
REVIEW_STATUSES = {"unverified", "primary_documentation_reviewed", "endpoint_observed"}
EVIDENCE_METHODS = {"document_inventory", "primary_documentation", "http_probe", "repository_issue"}

# Pinned literal identities from the 18 additions in upstream commit 0508c7b.
# Do not derive approval from the mutable registry itself.
MONITOR_ONLY_APPROVED = (
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
)


def valid_url(value):
    if not isinstance(value, str) or re.search(r"[\s<>]", value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not parsed.username and not parsed.password and parsed.port != 0
    except ValueError:
        return False


def valid_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except (ValueError, TypeError):
        return False


def relative_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and (root / value).is_file() and (root / value).resolve().is_relative_to(root.resolve())


def compute_totals(sources, supplementary):
    return {"source_documents": len(sources),
            "indonesia_source_documents": sum(s.get("country") == "ID" for s in sources),
            "international_reference_documents": sum(s.get("country") != "ID" for s in sources),
            "supplementary_documents": len(supplementary),
            "by_tier": dict(sorted(Counter(s.get("tier") for s in sources).items()))}


def monitor_tuples(root):
    # Literal AST extraction only: never import or execute the monitor.
    tree = ast.parse((root / "status/check.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PORTALS" for t in node.targets):
            entries = ast.literal_eval(node.value)
            if not isinstance(entries, (list, tuple)) or any(
                not isinstance(e, (list, tuple)) or len(e) != 5
                or any(not isinstance(v, str) for v in e[:4])
                or type(e[4]) is not int for e in entries
            ):
                raise ValueError("PORTALS must contain five-field literal tuples")
            if len({e[0] for e in entries}) != len(entries):
                raise ValueError("duplicate PORTALS id")
            return {e[0]: tuple(e) for e in entries}
    raise ValueError("PORTALS not found")


def monitor_ids(root):
    return set(monitor_tuples(root))


def validate_monitor_inventory(root, linked_monitors, registry=None, portals=None):
    """Check exact union and pinned monitoring-only identities offline."""
    root = Path(root)
    errors = []
    portals = monitor_tuples(root) if portals is None else portals
    path = root / "catalog/monitor-only.json"
    if registry is None:
        if not path.exists():
            return [] if set(linked_monitors) == set(portals) else [
                "monitor id coverage differs from status/check.py PORTALS"]
        try:
            registry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return [f"monitor-only registry cannot be loaded: {exc}"]
    if not isinstance(registry, dict):
        return ["monitor-only registry must be an object"]
    if registry.get("schema_version") != 1 or registry.get("upstream_commit") != "0508c7b" or registry.get("source_document") != "status/2026-10-10-update.md":
        errors.append("monitor-only invalid schema or upstream provenance")
    entries = registry.get("endpoints")
    if not isinstance(entries, list) or any(not isinstance(e, dict) for e in entries):
        return errors + ["monitor-only endpoints must be an array of objects"]
    approved = {e[0]: e for e in MONITOR_ONLY_APPROVED}
    identifiers = [e.get("id") for e in entries]
    if len(entries) != 18 or set(i for i in identifiers if isinstance(i, str)) != set(approved):
        errors.append("monitor-only must contain exactly 18 approved upstream additions (no missing or extras)")
    if len([i for i in identifiers if isinstance(i, str)]) != len(set(i for i in identifiers if isinstance(i, str))):
        errors.append("duplicate monitor-only id")
    for entry in entries:
        identifier = entry.get("id")
        if not isinstance(identifier, str) or identifier not in approved:
            errors.append("unapproved monitor-only id")
            continue
        identity = tuple(entry.get(k) for k in ("id", "name", "url", "agency", "tier"))
        if identity != approved[identifier] or type(entry.get("tier")) is not int:
            errors.append(f"monitor-only tuple mismatch: {identifier}")
        if portals.get(identifier) != approved[identifier]:
            errors.append(f"monitor-only PORTALS tuple missing or mismatch: {identifier}")
        if not valid_url(entry.get("url")):
            errors.append(f"monitor-only invalid URL: {identifier}")
        if entry.get("review") != {"date": "2026-10-10", "status": "unverified"}:
            errors.append(f"monitor-only review must remain unverified: {identifier}")
        access = entry.get("access")
        if not isinstance(access, dict) or access.get("mode") != "public-GET-only" or not isinstance(access.get("notes"), str) or not access["notes"].strip():
            errors.append(f"monitor-only public GET access limits required: {identifier}")
        if entry.get("source_document_status") != "monitoring-only; no canonical source document claimed":
            errors.append(f"monitor-only cannot claim a canonical source document: {identifier}")
    monitor_only_ids = {i for i in identifiers if isinstance(i, str)}
    if set(linked_monitors) & monitor_only_ids:
        errors.append("duplicate monitor id across canonical and monitor-only inventories")
    if set(linked_monitors) | monitor_only_ids != set(portals):
        errors.append("monitor id coverage differs from status/check.py PORTALS (canonical + monitor-only union)")
    return errors


def heading_anchors(text):
    counts, result = Counter(), set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        suffix = f"-{counts[slug]}" if counts[slug] else ""
        counts[slug] += 1
        result.add(slug + suffix)
    result.update(re.findall(r'<(?:a|span)\s+id=[\"\']([^\"\']+)', text))
    return result


def validate_links(root, documents):
    errors = []
    for document in documents:
        text = document.read_text(encoding="utf-8")
        # Examples may contain Markdown-like syntax; code is not navigation.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            parsed = urlsplit(target)
            label = str(document.relative_to(root))
            if parsed.scheme:
                if parsed.scheme not in {"mailto"} and not valid_url(target):
                    errors.append(f"{label}: invalid external link {target}")
                continue
            path = (document.parent / unquote(parsed.path)).resolve() if parsed.path else document.resolve()
            if not path.is_relative_to(root.resolve()):
                errors.append(f"{label}: escaping local link {target}")
            elif not path.exists():
                errors.append(f"{label}: missing local link {target}")
            elif parsed.fragment and path.is_file() and path.suffix == ".md" and unquote(parsed.fragment) not in heading_anchors(path.read_text(encoding="utf-8")):
                errors.append(f"{label}: missing anchor {target}")
    return errors


def validate_catalog(root, catalog=None):
    root = Path(root).resolve()
    errors = []
    if catalog is None:
        try:
            catalog = json.loads((root / "catalog/sources.json").read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return [f"catalog cannot be loaded: {exc}"]
    if not isinstance(catalog, dict):
        return ["catalog must be an object"]
    if catalog.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not valid_date(catalog.get("review_date")):
        errors.append("invalid review_date")
    sources = catalog.get("sources")
    supplementary = catalog.get("supplementary_documents")
    if not isinstance(sources, list) or not sources or any(not isinstance(s, dict) for s in sources):
        return errors + ["sources must be a nonempty array of objects"]
    if not isinstance(supplementary, list) or any(not isinstance(s, dict) for s in supplementary):
        return errors + ["supplementary_documents must be an array of objects"]
    ids, docs, linked_monitors = [], [], []
    for index, source in enumerate(sources):
        tag = f"sources[{index}]"
        for key in ("id", "name", "agency", "tier", "documentation", "portal_url", "kind", "country"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                errors.append(f"{tag}: required string {key}")
        identifier = source.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            errors.append(f"{tag}: invalid id")
        ids.append(identifier)
        docs.append(source.get("documentation"))
        if not isinstance(source.get("tier"), str) or source["tier"] not in TIERS:
            errors.append(f"{tag}: invalid tier")
        if not isinstance(source.get("kind"), str) or source["kind"] not in {"government", "non-government"}:
            errors.append(f"{tag}: invalid kind")
        if not isinstance(source.get("country"), str) or source["country"] not in {"ID", "JP"}:
            errors.append(f"{tag}: invalid country")
        if not relative_file(root, source.get("documentation")):
            errors.append(f"{tag}: invalid documentation path")
        if not valid_url(source.get("portal_url")):
            errors.append(f"{tag}: invalid portal_url")
        access = source.get("access")
        if not isinstance(access, dict) or any(not isinstance(access.get(k), str) or not access[k].strip() for k in ("auth", "notes")):
            errors.append(f"{tag}: access requires auth and notes")
        review = source.get("review")
        if not isinstance(review, dict):
            errors.append(f"{tag}: review must be an object")
            continue
        if not valid_date(review.get("date")) or not valid_date(catalog.get("review_date")) or review["date"] > catalog["review_date"]:
            errors.append(f"{tag}: invalid review date")
        if not isinstance(review.get("status"), str) or review["status"] not in REVIEW_STATUSES:
            errors.append(f"{tag}: invalid review status")
        evidence = review.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{tag}: missing evidence")
        else:
            for entry in evidence:
                if not isinstance(entry, dict) or not valid_url(entry.get("url")) or (not isinstance(entry.get("method"), str) or entry["method"] not in EVIDENCE_METHODS) or not isinstance(entry.get("observation"), str) or not entry["observation"].strip():
                    errors.append(f"{tag}: invalid evidence")
            methods = {e["method"] for e in evidence if isinstance(e, dict) and isinstance(e.get("method"), str)}
            if review.get("status") == "primary_documentation_reviewed" and "primary_documentation" not in methods:
                errors.append(f"{tag}: primary review requires primary evidence")
            if review.get("status") == "endpoint_observed" and "http_probe" not in methods:
                errors.append(f"{tag}: endpoint review requires probe evidence")
        monitors = source.get("monitor_ids")
        if not isinstance(monitors, list) or any(not isinstance(m, str) for m in monitors):
            errors.append(f"{tag}: monitor_ids must be a string array")
        else:
            linked_monitors.extend(monitors)
    valid_ids = {i for i in ids if isinstance(i, str)}
    for field, values in (("id", ids), ("documentation", docs), ("monitor id", linked_monitors)):
        for value, count in Counter(v for v in values if isinstance(v, str)).items():
            if count > 1:
                errors.append(f"duplicate {field}: {value}")
    for source in sources:
        related = source.get("related_sources", [])
        if not isinstance(related, list) or any(not isinstance(r, str) or r not in valid_ids or r == source.get("id") for r in related):
            errors.append("invalid related_sources")
    actual_docs = {str(p.relative_to(root)) for p in (root / "apis").rglob("README.md")}
    if actual_docs != {d for d in docs if isinstance(d, str)}:
        errors.append("source documentation coverage differs from apis/**/README.md")
    references = []
    for entry in supplementary:
        path = entry.get("documentation")
        references.append(path)
        if not relative_file(root, path) or not isinstance(entry.get("source_ids"), list) or not entry["source_ids"] or any(not isinstance(i, str) or i not in valid_ids for i in entry["source_ids"]):
            errors.append("invalid supplementary documentation or source_ids")
    if len(references) != len({r for r in references if isinstance(r, str)}):
        errors.append("duplicate supplementary documentation")
    if {str(p.relative_to(root)) for p in (root / "references").rglob("*.md")} != {r for r in references if isinstance(r, str)}:
        errors.append("reference documentation coverage differs from references/**/*.md")
    if all(isinstance(s.get("tier"), str) for s in sources) and catalog.get("totals") != compute_totals(sources, supplementary):
        errors.append("catalog totals do not match computed totals")
    try:
        errors.extend(validate_monitor_inventory(root, linked_monitors))
    except (OSError, ValueError, SyntaxError, TypeError) as exc:
        errors.append(f"monitor inventory unavailable: {exc}")
    readme = root / "README.md"
    if readme.is_file() and all(isinstance(s.get("tier"), str) for s in sources):
        expected = compute_totals(sources, supplementary)
        for key in ("source_documents", "indonesia_source_documents", "international_reference_documents", "supplementary_documents"):
            if f"<!-- catalog:{key}={expected[key]} -->" not in readme.read_text(encoding="utf-8"):
                errors.append(f"README totals missing or stale: {key}")
        for documentation in actual_docs:
            if f"]({documentation})" not in readme.read_text(encoding="utf-8"):
                errors.append(f"README source index missing: {documentation}")
    owned = [root / name for name in ("README.md", "SKILL.md", "mcp-servers/README.md", "docs/source-review-2026-10-10.md", "docs/monitor-only-endpoints.md")]
    owned += sorted((root / "apis").rglob("*.md")) + sorted((root / "references").rglob("*.md"))
    errors.extend(validate_links(root, [p for p in owned if p.is_file()]))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_catalog(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    data = json.loads((args.root / "catalog/sources.json").read_text(encoding="utf-8"))
    print("Catalog valid (offline): " + json.dumps(data["totals"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
