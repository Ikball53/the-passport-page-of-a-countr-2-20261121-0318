#!/usr/bin/env python3
"""Entry point for the invented passport spread competition.

Country: Republic of Thalvarra (capital Port Senn), holder Mira Solenne.

The rendered spread is bundled as entry.png alongside this file.
Running the script copies it to /output/entry.png, creating the
output directory when it does not exist yet.
"""
from pathlib import Path
import shutil
import sys


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"missing bundled image: {source}", file=sys.stderr)
        return 1
    dest_dir = Path("/output")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(source, dest)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
