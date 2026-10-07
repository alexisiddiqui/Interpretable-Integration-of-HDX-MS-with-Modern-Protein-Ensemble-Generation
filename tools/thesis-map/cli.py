#!/usr/bin/env python3
"""Build, validate and render versioned thesis maps. See README.md for dependencies."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from extraction import extract, atomic_text, ExtractionError
from normalize import normalize
from validation import validate, coverage

ROOT = Path(__file__).resolve().parent
DEFAULT_CACHE = ROOT / ".cache"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_profile(name):
    # Named profiles are discovered without editing a registry or executing curation.
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise ValueError("Profile must be a lowercase name, e.g. crook.")
    source = ROOT / "profiles" / (name + ".py")
    data = source.with_suffix(".json")
    if not source.is_file() or not data.is_file():
        raise ValueError(
            f"Unknown profile {name!r}; expected {source.name} and {data.name} under profiles/."
        )
    spec = importlib.util.spec_from_file_location("thesis_map_profile_" + name, source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = read_json(data)
    if config.get("profile_version") != 1 or config.get("name") != name:
        raise ValueError("Unsupported profile version or mismatched profile name.")
    return module, config


def build(profile, pdf, cache=DEFAULT_CACHE, jobs=4, progress=None):
    adapter, config = load_profile(profile)
    pages, extraction = extract(pdf, cache, jobs=jobs, progress=progress)
    expected = config["pdf_pages"]
    if len(pages) != expected:
        raise ValueError(
            f"Profile {profile} expects {expected} PDF pages, got {len(pages)}."
        )
    config["source_pdf"] = Path(pdf).name
    config["profile_sha256"] = hashlib.sha256(
        (ROOT / "profiles" / (profile + ".json")).read_bytes()
        + (ROOT / "profiles" / (profile + ".py")).read_bytes()
    ).hexdigest()
    native, diagnostics = adapter.parse(pages, config)
    diagnostics["pages"] = pages
    diagnostics["source_checks"] = config.get("source_checks", [])
    document = normalize(native, config, extraction, diagnostics)
    failures, warnings = validate(document, pages=pages, diagnostics=diagnostics)
    if failures:
        raise ValueError("Validation failed:\n" + "\n".join("  " + x for x in failures))
    document["quality"]["coverage"] = coverage(document)
    document["quality"]["coverage"]["source_token_checks"] = len(
        config.get("source_checks", [])
    )
    document["quality"]["coverage"]["verified_quotes"] = sum(
        bool(n.get("quote"))
        for n in list(document["structure"]["nodes"].values())
        + document["journey"]["stages"]
        + document["links"]["claims"]
    )
    document["quality"]["validation"] = dict(failures=[], warnings=warnings)
    return document


def render(document):
    failures, _ = validate(document)
    if failures:
        raise ValueError("Cannot render invalid thesis map:\n" + "\n".join(failures))
    template = (ROOT / "map_template.html").read_text(encoding="utf-8")
    placeholder = "/*__DATA__*/"
    if template.count(placeholder) != 1:
        raise ValueError("Shared template must contain exactly one data placeholder.")
    data = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    data = (
        data.replace("<", "\\u003c")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
    return template.replace(placeholder, data)


def publish(document, directory):
    # Both complete artifacts exist in memory before either destination is touched.
    serialized = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    html = render(document)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".thesis-map-", dir=directory) as scratch:
        scratch = Path(scratch)
        (scratch / "thesis.json").write_text(serialized, encoding="utf-8")
        (scratch / "map.html").write_text(html, encoding="utf-8")
        os.replace(scratch / "thesis.json", directory / "thesis.json")
        os.replace(scratch / "map.html", directory / "map.html")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    builder = commands.add_parser(
        "build", help="Rebuild both artifacts from a PDF and curated profile."
    )
    builder.add_argument("--profile", required=True)
    builder.add_argument("--pdf", type=Path, required=True)
    builder.add_argument("--out", type=Path, required=True)
    builder.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    builder.add_argument("--jobs", type=int, default=4)
    validator = commands.add_parser(
        "validate",
        help="Check schema and references; optionally verify against the source PDF.",
    )
    validator.add_argument("json", type=Path)
    validator.add_argument("--pdf", type=Path)
    validator.add_argument("--profile")
    validator.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    validator.add_argument("--jobs", type=int, default=4)
    renderer = commands.add_parser(
        "render", help="Render validated v2 JSON without a PDF or OCR dependency."
    )
    renderer.add_argument("json", type=Path)
    renderer.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        progress = lambda message: print(message, file=sys.stderr, flush=True)
        if getattr(args, "jobs", 1) < 1:
            raise ValueError("--jobs must be a positive integer.")
        if args.command == "build":
            document = build(args.profile, args.pdf, args.cache, args.jobs, progress)
            publish(document, args.out)
            print(json.dumps(document["quality"]["coverage"], sort_keys=True))
        elif args.command == "render":
            atomic_text(args.out, render(read_json(args.json)))
            print(f"Wrote {args.out}")
        else:
            document = read_json(args.json)
            failures, warnings = validate(document)
            if args.pdf and not args.profile:
                raise ValueError("--pdf requires --profile for source validation.")
            if args.profile and not args.pdf:
                raise ValueError("--profile requires --pdf for source validation.")
            if args.pdf and not failures:
                rebuilt = build(args.profile, args.pdf, args.cache, args.jobs, progress)
                if document != rebuilt:
                    failures.append(
                        "Map differs from the validated rebuild of its PDF/profile; run build to refresh it."
                    )
                else:
                    warnings = []
            for message in warnings:
                print("Warning: " + message, file=sys.stderr)
            if failures:
                raise ValueError("\n".join(failures))
            print("Valid thesis map " + document["schema_version"])
        return 0
    except (
        ValueError,
        OSError,
        AssertionError,
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
