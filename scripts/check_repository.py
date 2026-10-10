#!/usr/bin/env python3
"""Run offline repository gates or stage an allowlisted static Pages directory."""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ("index.html", "og-image.png", "BaksoSapi.otf")
DATA_NAME = re.compile(r"(?:[0-9]{4}-[0-9]{2}-[0-9]{2}|latest|index|history)\.json")


def stage_static(destination, source=None):
    """Never copy scripts, Markdown, symlinks, configs, keys or arbitrary files."""
    source = Path(source) if source else ROOT / "status"
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("staging destination must not exist")
    if destination == source.resolve() or source.resolve() in destination.parents:
        raise ValueError("staging destination must be outside status")
    if source.is_symlink() or (source / "data").is_symlink():
        raise ValueError("symlinked status sources are forbidden")
    files = []
    for name in ASSETS:
        path = source / name
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing or symlinked static asset: {name}")
        files.append(path)
    for path in sorted((source / "data").iterdir()):
        if not DATA_NAME.fullmatch(path.name):
            continue
        if path.is_symlink() or not path.is_file():
            raise ValueError("data must be ordinary JSON files")
        json.loads(path.read_text(encoding="utf-8"))
        files.append(path)
    if not all(source / "data" / name in files for name in ["latest.json", "index.json", "history.json"]):
        raise ValueError("missing required static datasets")
    for path in files:
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    print(f"Staged {len(files)} allowlisted static assets/data files")
    return files


def check():
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        [sys.executable, "scripts/test_status_canonical.py"],
        [sys.executable, "scripts/validate_catalog.py"],
        [sys.executable, "-m", "ruff", "check"],
        [shutil.which("zizmor") or str(Path(sys.executable).parent / "zizmor"),
         ".github/workflows", "--offline", "--persona", "pedantic",
         "--format", "plain", "--no-progress"],
    ]
    for command in commands:
        print("+ " + " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage-static", type=Path,
                        help="create a NEW static-only Pages directory instead of running tests")
    args = parser.parse_args(argv)
    try:
        if args.stage_static:
            stage_static(args.stage_static)
        else:
            check()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Repository check failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
