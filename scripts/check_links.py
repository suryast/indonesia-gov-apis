#!/usr/bin/env python3
"""Allowlisted Markdown link audit; bounded, credential-free GET observations only.

Uses curl with normal certificate verification, no user curl configuration, no
cookie/auth headers and no automatic redirects. Bodies go directly to /dev/null;
--max-filesize bounds transfers even without Content-Length (curl >= 8.4).
This is reachability evidence, NOT authenticated/API/POST functionality proof.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import ipaddress
import json
import re
import subprocess
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

ROOT_FILES = ("README.md", "SKILL.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md")
ROOT_DIRS = ("docs", "apis", "references", "mcp-servers", "status", "examples")
EXCLUDED = {
    ".git",
    ".cache",
    "__pycache__",
    "node_modules",
    "vendor",
    "deps",
    "private",
    "scratch",
    ".scratch",
    ".venv",
    ".ruff_cache",
    ".pytest_cache",
}
SECRET_KEYS = re.compile(
    r"(?i)(api[-_]?key|access[-_]?key|token|secret|password|passwd|"
    r"authorization|signature|credential|client[-_]?secret|session|auth|^key$)"
)
TEMPLATE = re.compile(
    r"[{}<>]|\$[A-Za-z_{]|\[\w+\]|(?i:YOUR[_-]|REPLACE[_-]|INSERT[_-]|"
    r"API_KEY|ACCESS_TOKEN|TOKEN_HERE|XXXXX|\.\.\.)"
)
HTTP_URL = re.compile(r'https?://[^\s`"\'\\]+', re.I)


def markdown_files(root: Path) -> list[Path]:
    files = [root / name for name in ROOT_FILES if (root / name).is_file()]
    for dirname in ROOT_DIRS:
        directory = root / dirname
        if not directory.is_dir() or directory.is_symlink():
            continue
        for path in directory.rglob("*"):
            rel = path.relative_to(root)
            if any(
                part in EXCLUDED or part.startswith((".venv", ".cache"))
                for part in rel.parts
            ):
                continue
            if path.is_symlink() or not path.is_file() or path.suffix.lower() != ".md":
                continue
            if path.name.startswith("link-audit-"):
                continue
            if not path.resolve().is_relative_to(root.resolve()):
                continue
            files.append(path)
    return sorted(set(files), key=lambda p: p.relative_to(root).as_posix())


def trim_url(target: str) -> str:
    target = html.unescape(target).rstrip(".,;:!?")
    while target.endswith(")") and target.count(")") > target.count("("):
        target = target[:-1]
    # A Markdown autolink's closing > is not a template's closing >.
    if target.endswith(">") and "<" not in target:
        target = target[:-1]
    return target


def destination_offset(text: str, start: int) -> int:
    while start < len(text) and text[start].isspace():
        start += 1
    return start + 1 if text[start : start + 1] == "<" else start


def destination(text: str, start: int) -> tuple[str, int]:
    """Parse an inline/ref destination, preserving balanced URL parentheses."""
    while start < len(text) and text[start].isspace():
        start += 1
    if start < len(text) and text[start] == "<":
        end = text.find(">", start + 1)
        if end >= 0:
            return text[start + 1 : end], end + 1
    end, depth = start, 0
    while end < len(text):
        char = text[end]
        if char == "\\" and end + 1 < len(text):
            end += 2
            continue
        if char.isspace() and depth == 0:
            break
        if char == "(":
            depth += 1
        if char == ")":
            if depth == 0:
                break
            depth -= 1
        end += 1
    return re.sub(r"\\([() ])", r"\1", text[start:end]), end


def extract(text: str, file: str) -> list[dict]:
    """Extract inline links/images, references/autolinks and literals in code/prose.

    Occurrences are deduplicated by exact target + source position (not line),
    so the HTTP literal inside a Markdown target is not counted twice. Reference
    usages and their definitions are both retained at their actual locations.
    """
    refs = {}
    occurrences = {}
    occupied = []

    def add(target: str, offset: int, kind: str):
        if not target:
            return
        occurrences[(target, offset)] = {
            "target": target,
            "file": file,
            "line": text.count("\n", 0, offset) + 1,
            "column": offset - text.rfind("\n", 0, offset),
            "kind": kind,
        }

    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*", text, re.M):
        target, end = destination(text, match.end())
        refs[" ".join(match[1].split()).casefold()] = target
        add(target, destination_offset(text, match.end()), "reference_definition")
        occupied.append((match.start(), end))

    # Labels can contain escaped brackets and simple nested brackets (images).
    pattern = r"!?\[((?:\\.|\[[^\]\n]*\]|[^\]\\\n])*)\]"
    for match in re.finditer(pattern, text):
        if any(a <= match.start() < b for a, b in occupied):
            continue
        end = match.end()
        if end < len(text) and text[end] == "(":
            target, target_end = destination(text, end + 1)
            add(
                target,
                destination_offset(text, end + 1),
                "image" if match[0].startswith("!") else "link",
            )
            occupied.append((end + 1, target_end))
            continue
        ref_match = re.match(r"\[([^\]\n]*)\]", text[end:])
        key = ref_match[1] if ref_match and ref_match[1] else match[1]
        target = refs.get(" ".join(key.split()).casefold())
        if target:
            add(target, match.start(), "reference_usage")
            if ref_match:
                occupied.append((end, end + len(ref_match[0])))
    for match in HTTP_URL.finditer(text):
        if any(a <= match.start() < b for a, b in occupied):
            continue
        add(trim_url(match[0]), match.start(), "literal_url")
    return sorted(
        occurrences.values(), key=lambda x: (x["line"], x["column"], x["target"])
    )


def skip_reason(target: str) -> str | None:
    if TEMPLATE.search(unquote(target)):
        return "templated_or_placeholder_url"
    try:
        parts = urlsplit(target)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            return "unsupported_or_invalid_url"
        if parts.username is not None or parts.password is not None:
            return "credential_bearing_url"
        if any(
            SECRET_KEYS.search(unquote(pair.split("=", 1)[0]))
            for pair in (parts.query + "&" + parts.fragment).split("&")
            if "=" in pair
        ):
            return "credential_bearing_query"
        if re.search(r"(?i)/(?:key|token|secret|password|apikey)/[^/]+", parts.path):
            return "credential_bearing_path"
        host = parts.hostname.lower().rstrip(".")
        if host in {
            "example.com",
            "example.org",
            "example.net",
            "localhost",
        } or host.endswith(
            (
                ".example.com",
                ".example.org",
                ".example.net",
                ".example",
                ".invalid",
                ".test",
                ".localhost",
                ".local",
            )
        ):
            return "dummy_or_local_hostname"
        try:
            if not ipaddress.ip_address(host).is_global:
                return "non_public_address"
        except ValueError:
            pass
        if re.search(r"/(?:12345|1234567890)(?:/|$)", parts.path):
            return "dummy_example_identifier"
        # Invalid ports must be rejected before curl rather than leaking diagnostics.
        parts.port
    except ValueError:
        return "unsupported_or_invalid_url"
    return None


def public_target(target: str) -> str:
    """Do not persist userinfo or plausible credentials, even in skipped links."""
    try:
        parts = urlsplit(target)
        netloc = parts.netloc.rsplit("@", 1)[-1]
        query = "&".join(
            pair.split("=", 1)[0] + "=[REDACTED]"
            if SECRET_KEYS.search(unquote(pair.split("=", 1)[0]))
            else pair
            for pair in parts.query.split("&")
        )
        path = re.sub(
            r"(?i)(/(?:key|token|secret|password|apikey)/)[^/]+",
            r"\1[REDACTED]",
            parts.path,
        )
        fragment = "&".join(
            pair.split("=", 1)[0] + "=[REDACTED]"
            if "=" in pair and SECRET_KEYS.search(unquote(pair.split("=", 1)[0]))
            else pair
            for pair in parts.fragment.split("&")
        )
        return urlunsplit((parts.scheme, netloc, path, query, fragment))
    except ValueError:
        return "[invalid URL; see identity hash and source location]"


def anchors(text: str) -> set[str]:
    result, counts, fence = set(), Counter(), None
    previous = ""
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = (marker[1][0], len(marker[1]))
            elif marker[1][0] == fence[0] and len(marker[1]) >= fence[1]:
                fence = None
            previous = ""
            continue
        if fence:
            continue
        result.update(
            html.unescape(x)
            for x in re.findall(r'\b(?:id|name)\s*=\s*["\']([^"\']+)["\']', line, re.I)
        )
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$", line)
        heading = match[1] if match else None
        if re.match(r"^ {0,3}(?:=+|-+)\s*$", line) and previous.strip():
            heading = previous.strip()
        if heading:
            heading = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", heading)
            heading = html.unescape(re.sub(r"<[^>]*>", "", heading)).lower()
            slug = "".join(c for c in heading if c.isalnum() or c in "_- ")
            slug = slug.replace(" ", "-")
            suffix = counts[slug]
            counts[slug] += 1
            result.add(slug if not suffix else f"{slug}-{suffix}")
        previous = line
    return result


def check_local(root: Path, source: str, target: str) -> dict:
    try:
        parts = urlsplit(target)
    except ValueError:
        return {"classification": "invalid_local_target"}
    if parts.scheme or target.startswith("//"):
        return {"classification": "not_requested", "reason": "non_http_scheme"}
    if TEMPLATE.search(target):
        return {"classification": "not_requested", "reason": "templated_local_target"}
    path_string = unquote(parts.path)
    if path_string.startswith("/"):
        path = root / path_string.lstrip("/")
    elif path_string:
        path = root / Path(source).parent / path_string
    else:
        path = root / source
    path = path.resolve()
    if not path.is_relative_to(root.resolve()):
        return {"classification": "outside_repository"}
    if path.is_dir():
        readme = next(
            (
                path / name
                for name in ("README.md", "readme.md")
                if (path / name).is_file()
            ),
            None,
        )
        if readme:
            path = readme
    if not path.exists():
        return {"classification": "missing_path"}
    if parts.fragment:
        if not path.is_file() or path.suffix.lower() not in (
            ".md",
            ".html",
            ".htm",
            ".svg",
        ):
            return {
                "classification": "local_anchor_unverified",
                "reason": "unsupported_target_fragment",
            }
        target_text = path.read_text(encoding="utf-8")
        ids = (
            anchors(target_text)
            if path.suffix.lower() == ".md"
            else {
                html.unescape(x)
                for x in re.findall(
                    r'\b(?:id|name)\s*=\s*["\']([^"\']+)["\']', target_text, re.I
                )
            }
        )
        if unquote(parts.fragment) not in ids:
            return {"classification": "missing_anchor"}
    return {"classification": "local_ok"}


def classify_curl(code: int) -> str:
    if code in (5, 6):
        return "dns_error"
    if code == 28:
        return "timeout"
    if code in (35, 51, 53, 54, 58, 59, 60, 64, 66, 77, 80, 82, 83, 90, 91):
        return "tls_error"
    if code == 47:
        return "redirect_limit"
    if code == 63:
        return "response_limit"
    if code in (1, 2, 3, 4):
        return "tool_or_url_error"
    return "network_error"


def classify_http(status: int, api: bool) -> str:
    if 200 <= status < 300:
        return "reachable"
    if status == 401:
        return "auth_required"
    if status == 403:
        return "blocked"
    if status == 429:
        return "rate_limited"
    if api and status in (400, 404, 405, 406, 415, 422):
        return "api_request_required"
    if status in (404, 410):
        return "broken_http"
    if 500 <= status:
        return "server_error"
    if 300 <= status < 400:
        return "redirect_without_location"
    return "http_error"


_HOST_LOCK = threading.Lock()
_HOSTS: dict[str, threading.Semaphore] = {}


def host_lock(url: str) -> threading.Semaphore:
    host = urlsplit(url).hostname or ""
    with _HOST_LOCK:
        return _HOSTS.setdefault(host, threading.Semaphore(1))


@contextmanager
def request_slot(url: str, remaining: float | None):
    lock = host_lock(url)
    acquired = (
        lock.acquire() if remaining is None else lock.acquire(timeout=max(0, remaining))
    )
    try:
        yield acquired
    finally:
        if acquired:
            lock.release()


def probe(
    url: str,
    timeout: float = 12,
    byte_cap: int = 65536,
    redirect_cap: int = 5,
    api: bool = False,
) -> dict:
    reason = skip_reason(url)
    if reason:
        return {
            "classification": "not_requested",
            "reason": reason,
            "status": None,
            "final_url": public_target(url),
        }
    current = urlunsplit(urlsplit(url)._replace(fragment=""))
    queued_at = time.monotonic()
    started = None
    queue_seconds = 0.0
    result = {
        "request_url": public_target(current),
        "final_url": public_target(current),
        "status": None,
        "redirects": [],
        "method": "GET",
        "body_limit_reached": False,
    }
    for hop in range(redirect_cap + 1):
        reason = skip_reason(current)
        if reason:
            result.update(
                classification="not_requested"
                if hop == 0
                else "redirect_not_requested",
                reason=reason,
            )
            break
        budget = None if started is None else timeout - (time.monotonic() - started)
        with request_slot(current, budget) as acquired:
            if not acquired:
                result["classification"] = "timeout"
                break
            if started is None:
                started = time.monotonic()
                queue_seconds = started - queued_at
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0:
                result["classification"] = "timeout"
                break
            command = [
                "curl",
                "-q",
                "--silent",
                "--proto",
                "=http,https",
                "--connect-timeout",
                str(min(5, remaining)),
                "--max-time",
                str(remaining),
                "--max-filesize",
                str(byte_cap),
                "--output",
                "/dev/null",
                "--user-agent",
                "RepositoryMarkdownLinkAudit/1.0",
                "--write-out",
                "%{http_code}\n%{redirect_url}\n",
                "--",
                current,
            ]
            try:
                completed = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=remaining + 1,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                result["classification"] = "timeout"
                break
            except OSError:
                result.update(
                    classification="tool_or_url_error", reason="curl_execution_failed"
                )
                break
        fields = completed.stdout.splitlines()
        status = int(fields[0]) if fields and re.fullmatch(r"\d{3}", fields[0]) else 0
        result["status"] = status or None
        result["final_url"] = public_target(current)
        if completed.returncode == 63 and status:
            result["body_limit_reached"] = True
        elif completed.returncode:
            result["classification"] = classify_curl(completed.returncode)
            result["curl_exit_code"] = completed.returncode
            break
        if 300 <= status < 400 and len(fields) > 1 and fields[1]:
            following = urljoin(current, fields[1])
            result["redirects"].append(
                {
                    "status": status,
                    "from": public_target(current),
                    "to": public_target(following),
                }
            )
            if skip_reason(following):
                result.update(
                    classification="redirect_not_requested",
                    reason=skip_reason(following),
                )
                break
            if hop == redirect_cap:
                result["classification"] = "redirect_limit"
                break
            current = urlunsplit(urlsplit(following)._replace(fragment=""))
            continue
        result["classification"] = (
            classify_http(status, api) if status else "network_error"
        )
        break
    result["elapsed_seconds"] = round(time.monotonic() - (started or queued_at), 3)
    result["initial_queue_seconds"] = round(queue_seconds, 3)
    return result


def audit(
    root: Path,
    workers: int = 8,
    timeout: float = 12,
    byte_cap: int = 65536,
    redirect_cap: int = 5,
) -> dict:
    sources, local, external_map = [], [], {}
    for path in markdown_files(root):
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        name = path.relative_to(root).as_posix()
        sources.append(
            {"file": name, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        )
        lines = text.splitlines()
        for occurrence in extract(text, name):
            target = occurrence.pop("target")
            occurrence["target"] = public_target(target)
            if re.match(r"^https?://", target, re.I):
                entry = external_map.setdefault(
                    target,
                    {
                        "url": public_target(target),
                        "identity_sha256": hashlib.sha256(target.encode()).hexdigest(),
                        "locations": [],
                        "api_context": False,
                    },
                )
                entry["locations"].append(occurrence)
                # Only a contextual clue, not a claim that an API actually works.
                context = lines[max(0, occurrence["line"] - 3) : occurrence["line"] + 1]
                entry["api_context"] |= bool(
                    re.search(
                        r"(?i)(/api(?:/|\?|$)|webapi|/rest/|/v[1-9]/|/resource/|/action/)",
                        target,
                    )
                    or re.search(
                        r"(?i)^https?://(?:[^/]*[.-])?(?:api|web-api|dataapi)[.-]",
                        target,
                    )
                    or re.search(r"(?i)\bPOST\b|--data|-X\s*POST", "\n".join(context))
                )
            else:
                local.append({**occurrence, **check_local(root, name, target)})

    def task(pair):
        url, entry = pair
        reason = skip_reason(url)
        if reason:
            return {
                **entry,
                "classification": "not_requested",
                "reason": reason,
                "status": None,
            }
        return {
            **entry,
            **probe(url, timeout, byte_cap, redirect_cap, entry["api_context"]),
        }

    with ThreadPoolExecutor(max_workers=workers) as executor:
        external = list(executor.map(task, sorted(external_map.items())))
    counts = {
        "markdown_files": len(sources),
        "unique_external_urls": len(external),
        "external_occurrences": sum(len(x["locations"]) for x in external),
        "local_occurrences": len(local),
        "external_classifications": dict(
            sorted(Counter(x["classification"] for x in external).items())
        ),
        "local_classifications": dict(
            sorted(Counter(x["classification"] for x in local).items())
        ),
    }
    # Detect concurrent document writes during a first-pass shared-worktree audit.
    changed = [
        x["file"]
        for x in sources
        if not (root / x["file"]).exists()
        or hashlib.sha256((root / x["file"]).read_bytes()).hexdigest() != x["sha256"]
    ]
    source_names = {x["file"] for x in sources}
    added = sorted(
        p.relative_to(root).as_posix()
        for p in markdown_files(root)
        if p.relative_to(root).as_posix() not in source_names
    )
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "root_files": list(ROOT_FILES),
            "directories": list(ROOT_DIRS),
            "excluded_components": sorted(EXCLUDED),
            "excluded_reports": "link-audit-*",
            "symlinks": "not enumerated; no resolved source outside repository",
        },
        "policy": {
            "method": "GET only",
            "verified_tls": True,
            "workers": workers,
            "per_host_concurrency": 1,
            "timeout_seconds": timeout,
            "response_byte_cap": byte_cap,
            "redirect_cap": redirect_cap,
            "response_bodies_stored": False,
            "credential_values_stored": False,
            "http_fragments_verified": False,
            "initial_host_queue_excluded_from_request_timeout": True,
            "limitations": "Fragments retain exact identity but are stripped for HTTP. "
            "HTTP success is not API functionality. API 400/404/405/422 requires review, "
            "not a confirmed broken prose link. No POST, auth, cookies or CAPTCHA bypass.",
        },
        "counts": counts,
        "sources_changed_during_audit": changed,
        "sources_added_during_audit": added,
        "sources": sources,
        "external": external,
        "local": local,
    }


def render_markdown(report: dict) -> str:
    counts = report["counts"]
    lines = [
        "# Repository Markdown link audit",
        "",
        f"Generated: `{report['generated_at']}`. Bounded reachability observations; "
        "compare the source hashes with final documentation before publishing.",
        "",
        f"- Markdown sources: **{counts['markdown_files']}**",
        f"- Exact external URL identities: **{counts['unique_external_urls']}** "
        f"({counts['external_occurrences']} occurrences)",
        f"- Local link occurrences: **{counts['local_occurrences']}**",
        "",
        "## Computed classifications",
        "",
        "| Kind | Classification | Count |",
        "| --- | --- | ---: |",
    ]
    for kind in ("external", "local"):
        for category, count in counts[f"{kind}_classifications"].items():
            lines.append(f"| {kind} | {category} | {count} |")
    lines += ["", "## Broken prose links and local failures", ""]
    failures = [
        (x, x["locations"])
        for x in report["external"]
        if x["classification"] == "broken_http"
    ]
    failures += [
        (x, [x])
        for x in report["local"]
        if x["classification"]
        in ("missing_path", "missing_anchor", "outside_repository")
    ]
    for entry, locations in failures:
        where = ", ".join(f"{x['file']}:{x['line']}:{x['column']}" for x in locations)
        target = entry.get("url", entry.get("target", "")).replace("`", "\\`")
        lines.append(f"- **{entry['classification']}** `{target}` — {where}")
    if not failures:
        lines.append("None observed.")
    lines += ["", "## Other external observations requiring review", ""]
    for entry in report["external"]:
        if entry["classification"] in ("reachable", "broken_http", "not_requested"):
            continue
        where = ", ".join(f"{x['file']}:{x['line']}" for x in entry["locations"])
        lines.append(
            f"- **{entry['classification']}** (HTTP {entry.get('status') or 'none'}) "
            f"`{entry['url']}` — {where}"
        )
    lines += [
        "",
        "## Safety and freshness",
        "",
        "Allowlisted root Markdown and docs/apis/references/mcp-servers/status/examples only. "
        "Caches, dependencies, private scratch, symlinks and audit reports are excluded. "
        "Credential-bearing, templated, dummy and non-public literal-address targets are "
        "not requested. Redirect targets receive the same screening. No response body or "
        "raw error text is retained. Verified-TLS GETs have explicit total per-URL timeout, "
        "byte and redirect caps, with one in-flight request per host.",
        "",
        "403 means observed blocked; 401 authentication required; 429 rate limited. "
        "Transport errors are not HTTP outages. Parameterized/API/POST examples are "
        "distinguished from confirmed broken prose links. External fragment validity, "
        "authentication, POST functionality and CAPTCHA behavior are not tested.",
        "",
        "Complete occurrences, skipped reasons, redirect observations and exact SHA-256 "
        "source snapshots are in the sibling JSON report. Compare hashes to current files "
        "before treating this report as fresh.",
        "",
    ]
    if report["sources_changed_during_audit"]:
        lines.append(
            "**Stale during execution:** "
            + ", ".join(report["sources_changed_during_audit"])
        )
        lines.append("")
    if report.get("sources_added_during_audit"):
        lines += [
            "**New sources during execution (not audited):** "
            + ", ".join(report["sources_added_during_audit"]),
            "",
        ]
    lines += [
        "## Source SHA-256 snapshots",
        "",
        "| Source | SHA-256 |",
        "| --- | --- |",
    ]
    lines += [f"| {x['file']} | `{x['sha256']}` |" for x in report["sources"]]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--json", type=Path, default=Path("docs/link-audit-2026-10-10.json")
    )
    parser.add_argument(
        "--markdown", type=Path, default=Path("docs/link-audit-2026-10-10.md")
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=12)
    parser.add_argument("--byte-cap", type=int, default=65536)
    parser.add_argument("--redirect-cap", type=int, default=5)
    args = parser.parse_args()
    if not (
        1 <= args.workers <= 16
        and 0 < args.timeout <= 60
        and 1 <= args.byte_cap <= 1048576
        and 0 <= args.redirect_cap <= 10
    ):
        parser.error(
            "bounds: workers 1..16; timeout >0..60; byte cap 1..1048576; redirects 0..10"
        )
    version = subprocess.run(
        ["curl", "-q", "--version"], capture_output=True, text=True, check=True
    )
    match = re.search(r"curl (\d+)\.(\d+)\.(\d+)", version.stdout)
    if not match or tuple(map(int, match.groups())) < (8, 4, 0):
        parser.error("curl >= 8.4 required for a streaming response byte cap")
    report = audit(
        args.root.resolve(),
        args.workers,
        args.timeout,
        args.byte_cap,
        args.redirect_cap,
    )
    for path, content in (
        (args.json, json.dumps(report, indent=2, ensure_ascii=False) + "\n"),
        (args.markdown, render_markdown(report)),
    ):
        if not path.is_absolute():
            path = args.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(json.dumps(report["counts"], indent=2))
    print(
        "Sources changed during audit:",
        ", ".join(report["sources_changed_during_audit"]) or "none",
    )
    # Reports are useful even when links fail; callers decide whether publication is safe.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
