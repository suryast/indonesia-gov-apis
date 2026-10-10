#!/usr/bin/env python3
"""Give BPJPH portal guidance; do not mistake halal supervisors for certified products."""
import argparse


def search_halal(query):
    print(f"Manual certification verification required for: {query}")
    print("No public certification-search API is verified by this example.")
    print("Start at the official BPJPH portal: https://bpjph.halal.go.id/")
    print("Follow its current certificate-search guidance, or contact BPJPH if unavailable.")
    print("A penyelia-halal (supervisor) directory is not certification evidence.")
    print("Check the exact product, business and certificate number, scope and current status.")
    print("No match, an unavailable portal, or a supervisor listing proves neither certification "
          "nor its absence. This script makes no network requests.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="product/business name (not sent anywhere by this script)")
    args = parser.parse_args(argv)
    if not args.query.strip():
        parser.error("query must not be empty")
    search_halal(args.query)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
