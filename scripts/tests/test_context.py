"""context: packs must be layered, narrow, and must cite only the module's own scope."""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `support` importable

from support import EXAMPLE  # noqa: E402

from tplib import context as context_mod
from tplib import state as state_mod


class ContextPackTests(unittest.TestCase):
    def setUp(self):
        self.state = state_mod.load_state(EXAMPLE)
        self.pack = context_mod.build_pack(EXAMPLE, self.state, "AUTH-001", "impl-auth-001")
        self.markdown = self.pack["markdown"]

    def test_layers_present_in_order(self):
        for title in (
            "Layer 1 — Project identity",
            "Layer 2 — Relevant requirements",
            "Layer 3 — Relevant architecture",
            "Layer 4 — Your module contract",
            "Layer 5 — Neighbour interfaces",
            "Layer 6 — Conventions",
            "Layer 7 — Current task and state",
            "Layer 8 — Validation requirements",
        ):
            self.assertIn(title, self.markdown, "missing %s" % title)
        self.assertLess(self.markdown.index("Layer 1"), self.markdown.index("Layer 8"))

    def test_module_contract_is_included_whole(self):
        self.assertIn("# AUTH-001 — Authentication", self.markdown)
        self.assertIn("## Acceptance criteria", self.markdown)

    def test_only_cited_requirements_are_included(self):
        self.assertIn("FR-AUTH-1", self.markdown)
        self.assertIn("NFR-SEC-1", self.markdown)
        # a requirement this module does not cite must not leak into the pack
        self.assertNotIn("FR-DASH-1", self.markdown)
        self.assertNotIn("UX-005", self.markdown)

    def test_ux_slice_only_when_cited(self):
        self.assertIn("UX-001", self.markdown)
        dash_pack = context_mod.build_pack(EXAMPLE, self.state, "DASH-001", "impl-dashboard-003")["markdown"]
        self.assertIn("UX-005", dash_pack)
        self.assertNotIn("FR-AUTH-1", dash_pack)

    def test_neighbour_interfaces_are_summarised_not_dumped(self):
        # USER-001 is a neighbour: its interface digest appears, its prose must not be dumped.
        self.assertIn("IF-USER-PORT", self.markdown)
        self.assertNotIn("Own the person behind a session", self.markdown)
        self.assertNotIn("tests/users/user-port.contract.test.ts::role_changes_are_visible", self.markdown)

    def test_validation_layer_has_commands(self):
        self.assertIn("python scripts/verify.py", self.markdown)
        self.assertIn("python scripts/tp.py validate", self.markdown)
        self.assertIn("python scripts/verify.py", self.pack["layers"]["8_validation"])

    def test_discovery_index_present(self):
        self.assertIn("Discovery index", self.markdown)

    def test_pack_is_bounded(self):
        # A pack that is larger than a few thousand lines means the module is too big.
        self.assertLess(len(self.markdown.splitlines()), 3000)

    def test_unknown_module_raises(self):
        with self.assertRaises(KeyError):
            context_mod.build_pack(EXAMPLE, self.state, "NOPE-999")


if __name__ == "__main__":
    unittest.main()
