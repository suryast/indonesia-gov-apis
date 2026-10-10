#!/usr/bin/env python3
"""Give official manual verification guidance; no public OJK search API is verified."""
import argparse


def check_illegal(query):
    print(f"Manual verification required for: {query}")
    print("Check OJK's official FIND directory: https://find.ojk.go.id/")
    print("Review warnings and announcements through https://www.ojk.go.id/")
    print("No match in an alert list does NOT prove licensed, legal, or safe.")
    print("Match the exact legal name, licence, product/activity and official domain; "
          "an impersonator may copy a licensed firm's name.")
    print("A listing or portal response is not an endorsement. Resolve ambiguity directly with OJK.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="entity's exact legal name (not sent anywhere by this script)")
    args = parser.parse_args(argv)
    if not args.query.strip():
        parser.error("query must not be empty")
    check_illegal(args.query)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
