#!/usr/bin/env python3
"""Read BI's public transaction-rate HTML, not JISDOR or an authless BI API."""
import argparse
import json
import math
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx"


def positive_timeout(value):
    value = float(value)
    if not math.isfinite(value) or not 0 < value <= 120:
        raise argparse.ArgumentTypeError("timeout must be finite and between 0 and 120 seconds")
    return value


def parse_exchange_rates(html):
    """Preserve BI's units and locale formatting; reject an unknown page layout."""
    soup = BeautifulSoup(html, "html.parser")
    expected = ["mata uang", "nilai", "kurs jual", "kurs beli"]
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        header_index = next((i for i, row in enumerate(rows) if [
            cell.get_text(" ", strip=True).casefold()
            for cell in row.find_all(["th", "td"])
        ] == expected), None)
        if header_index is None:
            continue
        rates = []
        for row in rows[header_index + 1:]:
            cols = [td.get_text(" ", strip=True) for td in row.find_all("td")]
            if not cols:
                continue
            if len(cols) != 4 or not all(cols):
                raise ValueError("BI rate row has an unexpected layout")
            rates.append(dict(zip(["currency", "units", "sell", "buy"], cols)))
        if rates:
            return rates
        raise ValueError("BI table contains no rates")
    raise ValueError("BI rate table not found; use the official portal manually")


def get_exchange_rates(timeout=30):
    resp = requests.get(URL, headers={"User-Agent": "indonesia-gov-apis-example/0.1"},
                        timeout=timeout)
    resp.raise_for_status()
    return parse_exchange_rates(resp.text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=positive_timeout, default=30)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(get_exchange_rates(args.timeout), ensure_ascii=False, indent=2))
    except (requests.RequestException, ValueError):
        print("BI request or HTML validation failed. Consult the official rate page.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
