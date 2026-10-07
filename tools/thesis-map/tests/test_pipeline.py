"""Regression tests for the shared public schema and output contract."""

import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1]
REPO = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
from cli import load_profile, publish, render, build
from extraction import extract, ExtractionError
from validation import validate


def artifact(name):
    root = os.environ.get("THESIS_MAP_EXAMPLES")
    directory = (
        Path(root) / ("thesis-map-" + name + "-check")
        if root
        else REPO / "examples" / (name + "-map")
    )
    return json.loads((directory / "thesis.json").read_text())


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = {name: artifact(name) for name in ("crook", "carlos", "vost")}
        cls.manifest = json.loads((TOOLS / "tests/preservation.json").read_text())

    def test_all_maps_validate_and_have_same_top_level_contract(self):
        expected = {
            "schema_version",
            "meta",
            "pagemap",
            "journey",
            "structure",
            "links",
            "quality",
        }
        for name, document in self.documents.items():
            with self.subTest(name=name):
                self.assertEqual(validate(document)[0], [])
                self.assertEqual(set(document), expected)
                self.assertEqual(document["schema_version"], "2.0.0")

    def test_preservation_of_scientific_content_and_ids(self):
        for name, d in self.documents.items():
            with self.subTest(name=name):
                baseline = self.manifest[name]
                self.assertEqual(
                    set(d["structure"]["nodes"]), set(baseline["node_ids"])
                )
                self.assertEqual(
                    {x["id"]: x["text"] for x in d["links"]["claims"]},
                    baseline["claims"],
                )
                self.assertEqual(
                    {
                        x["id"]: [x["source"], x["target"], x["basis"]]
                        for x in d["links"]["edges"]
                    },
                    baseline["edges"],
                )
                self.assertEqual(
                    {x["id"]: x["name"] for x in d["links"]["entities"]},
                    baseline["entities"],
                )
                self.assertEqual(
                    {x["id"]: x["title"] for x in d["journey"]["stages"]},
                    baseline["stages"],
                )
                self.assertEqual(
                    {x["id"]: x["text"] for x in d["quality"]["observations"]},
                    baseline["observations"],
                )
                self.assertEqual(d["journey"]["arc"], baseline["arc"])
                for i, text in baseline["summaries"].items():
                    self.assertEqual(d["structure"]["nodes"][i]["summary"], text)
                self.assertEqual(
                    sum(
                        n["kind"] == "figure" for n in d["structure"]["nodes"].values()
                    ),
                    baseline["figures"],
                )
                self.assertEqual(
                    sum(n["kind"] == "table" for n in d["structure"]["nodes"].values()),
                    baseline["tables"],
                )

    def test_numbering_and_journal_exceptions(self):
        crook = self.documents["crook"]["pagemap"]["pages"]
        vost = self.documents["vost"]["pagemap"]["pages"]
        carlos = self.documents["carlos"]["pagemap"]["pages"]
        self.assertEqual((crook[0]["label"], crook[30]["label"]), ("i", "1"))
        self.assertEqual(
            [vost[i]["label"] for i in (0, 1, 2, 22)], [None, None, "i", "1"]
        )
        self.assertEqual(carlos[0]["label"], "0")
        self.assertEqual(carlos[0]["status"], "counted")
        self.assertTrue(all(p["status"] == "counted" for p in carlos[187:201]))
        self.assertTrue(any(p["alternate_labels"] for p in carlos[187:201]))

    def test_depth_and_subtree_ranges_are_derived(self):
        for d in self.documents.values():
            nodes = d["structure"]["nodes"]
            for n in nodes.values():
                if n["parent"]:
                    parent = nodes[n["parent"]]
                    self.assertEqual(n["level"], parent["level"] + 1)
                    if n["kind"] not in ("figure", "table"):
                        self.assertGreaterEqual(
                            n["pages"]["pdf_start"], parent["pages"]["pdf_start"]
                        )
                        self.assertLessEqual(
                            n["pages"]["pdf_end"], parent["pages"]["pdf_end"]
                        )
        node = self.documents["vost"]["structure"]["nodes"]["s1.2"]
        self.assertGreater(node["pages"]["pdf_end"], node["own_pages"]["pdf_end"])

    def test_claims_can_reference_origin_and_destination(self):
        d = self.documents["vost"]
        roles = {s["id"]: s["role"] for s in d["journey"]["stages"]}
        self.assertEqual(roles["j0"], "origin")
        self.assertEqual(roles["j13"], "destination")
        self.assertEqual(
            sum(s["role"] == "research" for s in d["journey"]["stages"]), 12
        )
        self.assertEqual(
            sum(c["stage"] in ("j0", "j13") for c in d["links"]["claims"]), 5
        )

    def test_invalid_schema_and_unknown_versions_are_rejected(self):
        d = copy.deepcopy(self.documents["vost"])
        d["schema_version"] = "1.0"
        self.assertIn("Unsupported schema_version", validate(d)[0][0])
        self.assertTrue(validate([])[0])
        d = copy.deepcopy(self.documents["vost"])
        d["notes"] = []
        self.assertTrue(validate(d)[0])
        d = copy.deepcopy(self.documents["vost"])
        next(iter(d["structure"]["nodes"].values()))["source_pages"] = [3]
        self.assertTrue(validate(d)[0])

    def test_missing_references_duplicate_ids_and_cycles_are_rejected(self):
        for action in ("endpoint", "stage", "duplicate", "cycle"):
            with self.subTest(action=action):
                d = copy.deepcopy(self.documents["vost"])
                if action == "endpoint":
                    d["links"]["edges"][0]["target"] = "missing"
                elif action == "stage":
                    d["links"]["claims"][0]["stage"] = "missing"
                elif action == "duplicate":
                    d["links"]["claims"].append(copy.deepcopy(d["links"]["claims"][0]))
                else:
                    d["structure"]["nodes"]["ch1"]["parent"] = "s1.1"
                self.assertTrue(validate(d)[0])

    def test_bad_page_maps_and_reversed_ranges_are_rejected(self):
        d = copy.deepcopy(self.documents["vost"])
        d["pagemap"]["pages"][3]["label"] = "i"
        self.assertTrue(validate(d)[0])
        d = copy.deepcopy(self.documents["vost"])
        d["structure"]["nodes"]["ch1"]["pages"]["pdf_start"] = 176
        self.assertTrue(validate(d)[0])

    def test_quote_and_token_checks_use_extracted_source_text(self):
        d = copy.deepcopy(self.documents["vost"])
        for rec in (
            list(d["structure"]["nodes"].values())
            + d["journey"]["stages"]
            + d["links"]["claims"]
        ):
            rec["quote"] = None
        n = d["structure"]["nodes"]["ch1"]
        n["quote"] = {"text": "A checked quote crosses the page break", "page": "1"}
        pages = [""] * d["meta"]["pdf_pages"]
        pages[22] = "A checked quote crosses"
        pages[23] = "the page break"
        self.assertEqual(validate(d, pages=pages)[0], [])
        pages[23] = "different text"
        self.assertTrue(
            any("quote not found" in x for x in validate(d, pages=pages)[0])
        )
        n["quote"] = None
        check = {"record": "c1", "tokens": [["100", "hundred"]], "source_pages": ["1"]}
        pages[22] = "A hundred training points."
        self.assertEqual(
            validate(d, pages=pages, diagnostics={"source_checks": [check]})[0], []
        )
        pages[22] = "Twenty training points."
        self.assertTrue(
            any(
                "evidence tokens" in x
                for x in validate(
                    d, pages=pages, diagnostics={"source_checks": [check]}
                )[0]
            )
        )

    def test_output_is_offline_and_embeds_the_complete_json_safely(self):
        d = copy.deepcopy(self.documents["vost"])
        d["links"]["claims"][0][
            "text"
        ] = "</script><script>injected()</script>\u2028\u2029"
        html = render(d)
        self.assertNotIn("<script>injected()", html)
        self.assertNotRegex(html, r'<(?:link|script)[^>]+(?:href|src)=["\']https?://')
        embedded = re.search(
            r'<script type="application/json" id="thesis-data">(.*?)</script>',
            html,
            re.S,
        ).group(1)
        self.assertEqual(json.loads(embedded), d)
        self.assertEqual(len(re.findall(r"<script(?:\s|>)", html)), 2)

    def test_failed_preflight_preserves_both_existing_outputs(self):
        d = self.documents["vost"]
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            publish(d, directory)
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            invalid = copy.deepcopy(d)
            invalid["links"]["edges"][0]["target"] = "missing"
            with self.assertRaises(ValueError):
                publish(invalid, directory)
            self.assertEqual(
                before, {p.name: p.read_bytes() for p in directory.iterdir()}
            )
            publish(d, directory)
            self.assertEqual(
                before, {p.name: p.read_bytes() for p in directory.iterdir()}
            )

    def test_render_command_is_independent_of_working_directory(self):
        with tempfile.TemporaryDirectory() as scratch:
            input_path = Path(scratch) / "thesis.json"
            input_path.write_text(json.dumps(self.documents["vost"]))
            output_path = Path(scratch) / "map.html"
            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOLS / "cli.py"),
                    "render",
                    str(input_path),
                    "--out",
                    str(output_path),
                ],
                cwd=scratch,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output_path.read_text(), render(self.documents["vost"]))

    def test_missing_pdf_and_unknown_profiles_fail_cleanly(self):
        with tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / "outputs"
            result = subprocess.run(
                [
                    sys.executable,
                    str(TOOLS / "cli.py"),
                    "build",
                    "--profile",
                    "crook",
                    "--pdf",
                    str(Path(scratch) / "missing.pdf"),
                    "--out",
                    str(output),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("PDF not found", result.stderr)
            self.assertFalse(output.exists())
        with self.assertRaises(ValueError):
            load_profile("../crook")
        with self.assertRaises(ValueError):
            load_profile("unknown")

    def test_format_adapters_have_no_filesystem_or_dynamic_execution_calls(self):
        for source in (TOOLS / "profiles").glob("*.py"):
            tree = ast.parse(source.read_text())
            for n in ast.walk(tree):
                if isinstance(n, ast.Call):
                    name = (
                        n.func.id
                        if isinstance(n.func, ast.Name)
                        else n.func.attr if isinstance(n.func, ast.Attribute) else ""
                    )
                    self.assertNotIn(
                        name,
                        {
                            "open",
                            "exec",
                            "eval",
                            "dump",
                            "write_text",
                            "write_bytes",
                            "unlink",
                        },
                        str(source),
                    )

    def test_extraction_cache_is_content_addressed(self):
        with tempfile.TemporaryDirectory() as scratch:
            pdf = Path(scratch) / "source.pdf"
            pdf.write_bytes(b"PDF test input")
            cache = Path(scratch) / "cache"
            calls = []

            def run(command, **kwargs):
                calls.append(command)
                return (
                    "Pages: 2\n"
                    if command[0] == "pdfinfo"
                    else "First page has enough readable alphabetic text.\fSecond page also has enough alphabetic text.\f"
                )

            with patch("extraction.tool_version", return_value="test version"), patch(
                "extraction.run", side_effect=run
            ):
                first = extract(pdf, cache)
                second = extract(pdf, cache)
                self.assertEqual(first, second)
                self.assertEqual(sum(c[0] == "pdftotext" for c in calls), 1)
                pdf.write_bytes(b"Different PDF input")
                extract(pdf, cache)
                self.assertEqual(sum(c[0] == "pdftotext" for c in calls), 2)


if __name__ == "__main__":
    unittest.main()
