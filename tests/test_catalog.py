#!/usr/bin/env python3
"""Exercise the public catalog commands against the packaged archive."""

import gzip
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "unslopped-ui" / "scripts" / "catalog.py"
DATA = SCRIPT.parents[1] / "data"


def invoke(*arguments, code=0):
    with tempfile.TemporaryDirectory() as directory:
        result = subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=directory,
                                capture_output=True, text=True, check=False)
    if result.returncode != code:
        raise AssertionError(f"{arguments}: exit {result.returncode}, expected {code}: {result.stderr}")
    return json.loads(result.stdout if code == 0 else result.stderr)


class CatalogBehavior(unittest.TestCase):
    def test_exact_title_and_source_filter(self):
        result = invoke("search", "Almanac", "--source", "hallmark", "--kind", "theme")
        self.assertEqual(result["results"][0]["id"], "hallmark-theme-almanac")
        self.assertEqual(result["results"][0]["title"], "Almanac")
        self.assertTrue(all(row["source"] == "hallmark" for row in result["results"]))

    def test_named_brand_is_individually_retrievable(self):
        result = invoke("show", "ux-brand-zara")
        self.assertEqual(result["record"]["title"], "zara")
        self.assertIn("Sources and inherited read coverage:", result["text"])
        self.assertIn("data/brands/zara.json", result["text"])

    def test_table_row_retains_header(self):
        result = invoke("show", "hallmark-theme-newsprint")
        self.assertIn("| Theme | Ground | Ink |", result["record"]["table_header"])
        self.assertIn("| Newsprint | #eeebe3 |", result["text"])

    def test_multiword_search_and_results_pagination(self):
        first = invoke("search", "contrast gradient", "--limit", "2")
        self.assertGreater(first["total_matches"], 2)
        self.assertEqual(len(first["results"]), 2)
        self.assertEqual(first["next_offset"], 2)
        second = invoke("search", "contrast gradient", "--limit", "2", "--offset", "2")
        self.assertFalse({row["id"] for row in first["results"]}
                         & {row["id"] for row in second["results"]})

    def test_character_paging_preserves_full_record(self):
        first = invoke("show", "ux-brand-zara", "--chars", "137")
        self.assertFalse(first["complete"])
        self.assertEqual(len(first["text"]), 137)
        pieces = [first["text"]]
        offset = first["next_offset"]
        while offset is not None:
            page = invoke("show", "ux-brand-zara", "--offset", str(offset), "--chars", "12000")
            pieces.append(page["text"])
            offset = page["next_offset"]
        records = [json.loads(line) for line in gzip.decompress((DATA / "records.jsonl.gz").read_bytes()).decode("utf-8").splitlines()]
        record = next(row for row in records if row["id"] == "ux-brand-zara")
        self.assertEqual("".join(pieces), record["text"])

    def test_unknown_ids_and_bounds_are_json_errors(self):
        self.assertEqual(invoke("show", "not-a-record", code=2)["error"], "unknown record id")
        for arguments in [("list", "--limit", "21"), ("list", "--offset", "-1"),
                          ("show", "ux-001", "--chars", "12001"),
                          ("show", "ux-001", "--offset", "999999"),
                          ("search", "  "), ("list", "--source", "not-a-source")]:
            self.assertIn("error", invoke(*arguments, code=2))

    def test_lossless_archive_and_catalog_counts(self):
        result = invoke("check")
        self.assertTrue(result["ok"])
        self.assertEqual(result["reconstructed_sha256"],
                         "9be913e96876928e9b94b99cdff457152ee3b5b3f334fcb12f5db46785e8882f")
        self.assertEqual(result["reconstructed_bytes"], 2506745)
        info = invoke("info")
        self.assertEqual(info["kinds"]["brand"], 160)
        self.assertEqual(info["kinds"]["style"], 141)
        self.assertEqual(info["kinds"]["theme"], 50)

    def test_package_can_move_without_original_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "relocated-skill"
            (package / "scripts").mkdir(parents=True)
            shutil.copy2(SCRIPT, package / "scripts" / "catalog.py")
            shutil.copytree(DATA, package / "data")
            result = subprocess.run(
                [sys.executable, str(package / "scripts" / "catalog.py"), "show", "ux-001"],
                cwd=directory, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)
            self.assertEqual(output["record"]["id"], "ux-001")
            self.assertEqual(output["record"]["status"], "archived-reference")
            self.assertIn("Complete the brief from the request", output["text"])


if __name__ == "__main__":
    unittest.main()
