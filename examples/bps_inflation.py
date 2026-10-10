#!/usr/bin/env python3
"""Fetch a user-verified BPS indicator; variable IDs are not assumed to mean inflation."""
import argparse
import json
import os
import re
import sys
from urllib.parse import quote

import requests

BASE = "https://webapi.bps.go.id/v1/api"


def positive_timeout(value):
    value = int(value)
    if not 0 < value <= 120:
        raise argparse.ArgumentTypeError("timeout must be between 1 and 120 seconds")
    return value


def get_inflation(api_key, variable, domain="0000", timeout=30):
    """Return BPS JSON unchanged, including datacontent and dimension metadata.

    Select and verify an inflation/CPI variable in the official developer portal first.
    The historical filename does not make an arbitrary variable an inflation series.
    """
    if not re.fullmatch(r"[0-9]+", variable) or not re.fullmatch(r"[0-9]{4}", domain):
        raise ValueError("variable must be numeric and domain must contain four digits")
    if not api_key or not api_key.strip():
        raise ValueError("BPS_API_KEY is required")
    resp = requests.get(
        f"{BASE}/list/model/data/domain/{domain}/var/{variable}/key/{quote(api_key, safe='')}",
        timeout=timeout,
    )
    resp.raise_for_status()
    if "application/json" not in resp.headers.get("Content-Type", "").lower():
        raise ValueError("BPS did not return JSON")
    payload = resp.json()
    if not isinstance(payload, dict) or payload.get("status") != "OK":
        raise ValueError("BPS returned an error or an unknown response shape")
    if not isinstance(payload.get("datacontent"), dict):
        raise ValueError("BPS response has no datacontent mapping")
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variable", required=True,
                        help="BPS variable ID confirmed in the developer portal (no assumed default)")
    parser.add_argument("--domain", default="0000", help="four-digit BPS domain")
    parser.add_argument("--timeout", type=positive_timeout, default=30)
    args = parser.parse_args(argv)
    key = os.environ.get("BPS_API_KEY")
    if not key:
        parser.error("set BPS_API_KEY in your environment; register at https://webapi.bps.go.id/developer/")
    try:
        payload = get_inflation(key, args.variable, args.domain, args.timeout)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except (requests.RequestException, ValueError):
        # BPS embeds the key in the URL. Never print exception/request URLs or raw errors.
        print("BPS request or response validation failed; check your key and selected indicator.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
