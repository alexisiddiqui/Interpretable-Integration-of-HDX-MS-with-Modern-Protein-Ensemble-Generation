"""Local, resumable PDF extraction with content-addressed caches."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


class ExtractionError(ValueError):
    pass


def run(command, **kwargs):
    try:
        result = subprocess.run(command, capture_output=True, check=True, **kwargs)
        return result.stdout
    except FileNotFoundError as exc:
        raise ExtractionError(
            f"Missing {command[0]}; install Poppler and, for scanned PDFs, Tesseract."
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = (
            exc.stderr.decode("utf-8", errors="replace")
            if isinstance(exc.stderr, bytes)
            else exc.stderr
        )
        raise ExtractionError(f"{command[0]} failed: {detail.strip()}") from exc


def tool_version(name):
    executable = shutil.which(name)
    if not executable:
        raise ExtractionError(
            f"Missing {name}; install Poppler and, for scanned PDFs, Tesseract."
        )
    flag = "--version" if name == "tesseract" else "-v"
    result = subprocess.run([executable, flag], capture_output=True, text=True)
    return (result.stdout + result.stderr).splitlines()[0]


def atomic_text(destination, text):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination.parent,
        prefix="." + destination.name,
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(text)
    try:
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def extract(pdf, cache, jobs=4, progress=None):
    pdf = Path(pdf).resolve()
    if not pdf.is_file():
        raise ExtractionError(f"PDF not found: {pdf}")
    hasher = hashlib.sha256()
    with pdf.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    digest = hasher.hexdigest()
    versions = {tool: tool_version(tool) for tool in ("pdfinfo", "pdftotext")}
    info = run(["pdfinfo", str(pdf)], text=True)
    found = re.search(r"^Pages:\s+(\d+)", info, re.M)
    if not found:
        raise ExtractionError("pdfinfo did not report a page count.")
    count = int(found.group(1))
    settings = {"pdf_sha256": digest, "versions": versions, "layout": True}
    digital_key = hashlib.sha256(
        json.dumps(settings, sort_keys=True).encode()
    ).hexdigest()
    digital = Path(cache) / digital_key / "text.txt"
    if digital.is_file():
        text = digital.read_text(encoding="utf-8")
    else:
        text = run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"], text=True)
        atomic_text(digital, text)
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    if len(pages) != count:
        raise ExtractionError(
            f"Text extraction returned {len(pages)} pages; PDF contains {count}."
        )
    # Fully scanned PDFs need OCR. Blank versos in digital PDFs stay blank.
    readable = [len(re.findall(r"[A-Za-z]", page)) >= 30 for page in pages]
    scanned = not any(readable)
    missing = (
        list(range(count))
        if scanned
        else [i for i, page in enumerate(pages) if not page.strip()]
    )
    # Blank digital versos should stay blank; fallback is for fully scanned files.
    ocr_indices = missing if scanned else []
    if ocr_indices:
        versions.update(
            {tool: tool_version(tool) for tool in ("pdftoppm", "tesseract")}
        )
        settings.update(versions=versions, dpi=220, language="eng", ocr="tesseract")
        key = hashlib.sha256(json.dumps(settings, sort_keys=True).encode()).hexdigest()
        directory = Path(cache) / key
        directory.mkdir(parents=True, exist_ok=True)
        pending = []
        for i in ocr_indices:
            path = directory / f"p{i + 1:03d}.txt"
            if path.is_file():
                pages[i] = path.read_text(encoding="utf-8")
            else:
                pending.append(i)
        if progress:
            progress(
                f"OCR: {len(pending)} pages to extract ({len(ocr_indices) - len(pending)} cached)."
            )

        def ocr(i):
            with tempfile.TemporaryDirectory(prefix="page-", dir=directory) as scratch:
                prefix = str(Path(scratch) / "page")
                run(
                    [
                        "pdftoppm",
                        "-f",
                        str(i + 1),
                        "-l",
                        str(i + 1),
                        "-singlefile",
                        "-r",
                        "220",
                        "-png",
                        str(pdf),
                        prefix,
                    ]
                )
                env = dict(os.environ, OMP_THREAD_LIMIT="1")
                result = run(
                    ["tesseract", prefix + ".png", "stdout", "-l", "eng"],
                    text=True,
                    env=env,
                )
                atomic_text(directory / f"p{i + 1:03d}.txt", result)
                return i, result

        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(ocr, i) for i in pending]
            for completed, future in enumerate(as_completed(futures), 1):
                i, pages[i] = future.result()
                if progress and (completed % 10 == 0 or completed == len(pending)):
                    progress(f"OCR: {completed}/{len(pending)} pages complete.")
    return pages, {
        "tool": "tesseract" if ocr_indices else "pdftotext -layout",
        "ocr_used": bool(ocr_indices),
        "dpi": 220 if ocr_indices else None,
        "language": "eng" if ocr_indices else None,
        "versions": versions,
        "pdf_sha256": digest,
        "text_layer": "OCR of scanned pages" if ocr_indices else "digital PDF text",
    }
