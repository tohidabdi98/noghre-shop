"""yamlmini: the subset parser must be predictable and must fail loudly."""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `support` importable

from support import ROOT  # noqa: E402

from tplib import repoutil, yamlmini


class LoadingTests(unittest.TestCase):
    def test_nested_maps_and_sequences(self):
        text = """
# a comment
schema_version: 1
modules:
  - module_id: AUTH-001
    name: "Authentication"
    status: planned
    depends_on: [USER-001, PROJECT-001]
    history:
      - at: 2026-03-01
        to: ready
"""
        data = yamlmini.loads(text)
        self.assertEqual(data["schema_version"], 1)
        module = data["modules"][0]
        self.assertEqual(module["module_id"], "AUTH-001")
        self.assertEqual(module["name"], "Authentication")
        self.assertEqual(module["depends_on"], ["USER-001", "PROJECT-001"])
        self.assertEqual(module["history"][0]["to"], "ready")
        self.assertEqual(module["history"][0]["at"], "2026-03-01")

    def test_sequence_at_parent_indent(self):
        data = yamlmini.loads("modules:\n- module_id: A-001\n")
        self.assertEqual(data["modules"][0]["module_id"], "A-001")

    def test_trailing_comments_and_hashes_in_strings(self):
        data = yamlmini.loads(
            'name: "A # B"   # trailing comment\nplain: value # another\n'
        )
        self.assertEqual(data["name"], "A # B")
        self.assertEqual(data["plain"], "value")

    def test_scalars(self):
        data = yamlmini.loads(
            "a: true\nb: false\nc: null\nd: ~\ne: 12\nf: 1.5\ng: 'single'\nh:\n"
        )
        self.assertIs(data["a"], True)
        self.assertIs(data["b"], False)
        self.assertIsNone(data["c"])
        self.assertIsNone(data["d"])
        self.assertEqual(data["e"], 12)
        self.assertEqual(data["f"], 1.5)
        self.assertEqual(data["g"], "single")
        self.assertIsNone(data["h"])

    def test_inline_map_and_quoted_colon(self):
        data = yamlmini.loads('edge: {from: A-001, to: B-001}\nurl: "https://example.com/x"\n')
        self.assertEqual(data["edge"], {"from": "A-001", "to": "B-001"})
        self.assertEqual(data["url"], "https://example.com/x")

    def test_block_scalar(self):
        data = yamlmini.loads("notes: |\n  first line\n  second line\nnext: 1\n")
        self.assertIn("first line", data["notes"])
        self.assertIn("second line", data["notes"])
        self.assertEqual(data["next"], 1)

    def test_empty_document(self):
        self.assertEqual(yamlmini.loads(""), {})
        self.assertEqual(yamlmini.loads("# only a comment\n"), {})

    def test_duplicate_key_is_an_error(self):
        with self.assertRaises(yamlmini.YamlError):
            yamlmini.loads("a: 1\na: 2\n")

    def test_tabs_are_an_error(self):
        with self.assertRaises(yamlmini.YamlError):
            yamlmini.loads("a:\n\tb: 1\n")


class RoundTripTests(unittest.TestCase):
    def test_dump_then_load(self):
        payload = {
            "schema_version": 1,
            "modules": [
                {
                    "module_id": "AUTH-001",
                    "status": "in_progress",
                    "depends_on": [],
                    "notes": None,
                    "history": [{"at": "2026-03-01", "to": "ready", "by": "orchestrator"}],
                }
            ],
            "empty_list": [],
            "empty_map": {},
        }
        text = yamlmini.dumps(payload)
        self.assertEqual(yamlmini.loads(text), payload)

    def test_dump_quotes_risky_strings(self):
        text = yamlmini.dumps({"note": "a: b # c", "path": "src/auth/**"})
        data = yamlmini.loads(text)
        self.assertEqual(data["note"], "a: b # c")
        self.assertEqual(data["path"], "src/auth/**")


class RepositoryFilesTests(unittest.TestCase):
    """Every YAML file in the template must parse with the subset parser (no PyYAML needed)."""

    def test_all_yaml_files_parse(self):
        failures = []
        for relative in repoutil.iter_files(ROOT, suffixes=(".yaml", ".yml")):
            path = os.path.join(ROOT, relative)
            try:
                yamlmini.load_file(path)
            except yamlmini.YamlError as exc:
                failures.append("%s: %s" % (relative, exc))
        self.assertEqual(failures, [], "unparseable YAML:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
