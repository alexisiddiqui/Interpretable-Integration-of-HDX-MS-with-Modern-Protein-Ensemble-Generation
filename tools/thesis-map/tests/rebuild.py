#!/usr/bin/env python3
"""Integration check: rebuild all examples and compare deterministic artifacts."""

import argparse
import hashlib
from pathlib import Path
import sys
import tempfile

TOOLS = Path(__file__).resolve().parents[1]
REPO = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
from cli import build, publish, DEFAULT_CACHE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cold-cache", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    with tempfile.TemporaryDirectory(prefix="thesis-map-rebuild-") as scratch:
        scratch = Path(scratch)
        cache = scratch / "cache" if args.cold_cache else DEFAULT_CACHE
        for name in ("crook", "carlos", "vost"):
            document = build(
                name,
                REPO / "examples" / (name + "-thesis.pdf"),
                cache,
                args.jobs,
                lambda message: print(name + ": " + message, flush=True),
            )
            destination = scratch / name
            publish(document, destination)
            for filename in ("thesis.json", "map.html"):
                actual = (destination / filename).read_bytes()
                expected = (REPO / "examples" / (name + "-map") / filename).read_bytes()
                if actual != expected:
                    raise SystemExit(
                        f"{name}/{filename} differs from its rebuild. Refresh the example with cli.py build."
                    )
            print(name + ": both artifacts match their rebuild", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
