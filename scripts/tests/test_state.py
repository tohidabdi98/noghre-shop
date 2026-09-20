"""state: loading, dependency reasoning, readiness and transition legality."""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `support` importable

from support import EXAMPLE, ROOT  # noqa: E402

from tplib import state as state_mod


class ExampleStateTests(unittest.TestCase):
    def setUp(self):
        self.state = state_mod.load_state(EXAMPLE)

    def test_project_identity(self):
        self.assertEqual(self.state["project"]["project_id"], "example-saas")
        self.assertEqual(self.state["project"]["stage"], "implementation")

    def test_five_modules_registered(self):
        self.assertEqual(
            sorted(state_mod.module_ids(self.state)),
            ["AUTH-001", "DASH-001", "NOTIFY-001", "PROJECT-001", "USER-001"],
        )

    def test_upstream_and_downstream_direction(self):
        # NOTIFY-001 depends on PROJECT-001 and USER-001 (to = upstream)
        self.assertEqual(sorted(state_mod.upstream_of(self.state, "NOTIFY-001")), ["PROJECT-001", "USER-001"])
        self.assertIn("DASH-001", state_mod.downstream_of(self.state, "PROJECT-001"))

    def test_only_unblocked_module_is_ready(self):
        board = state_mod.compute_board(EXAMPLE, self.state)
        self.assertEqual(board["ready"], ["NOTIFY-001"])
        self.assertIn("NOTIFY-001", board["waves"].get(3, []))

    def test_ready_warns_about_shared_zone(self):
        board = state_mod.compute_board(EXAMPLE, self.state)
        self.assertTrue(
            any("shared zone" in warning for warning in board["warnings"]),
            "expected a shared-zone advisory for the ready module, got: %s" % board["warnings"],
        )

    def test_terminal_modules_are_reported(self):
        board = state_mod.compute_board(EXAMPLE, self.state)
        self.assertIn("AUTH-001", board["complete"])
        self.assertIn("DASH-001", state_mod.compute_board(EXAMPLE, self.state)["active"])

    def test_dependency_depth(self):
        self.assertEqual(state_mod.dependency_depth(self.state, "AUTH-001"), 0)
        self.assertEqual(state_mod.dependency_depth(self.state, "USER-001"), 1)
        self.assertEqual(state_mod.dependency_depth(self.state, "NOTIFY-001"), 3)

    def test_contract_parses_and_matches_registry(self):
        entry = state_mod.module_by_id(self.state, "AUTH-001")
        contract = state_mod.load_contract(EXAMPLE, entry)
        self.assertTrue(contract["exists"])
        self.assertEqual(contract["data"]["module_id"], "AUTH-001")
        self.assertEqual(contract["data"]["status"], entry["status"])
        self.assertTrue(any("acceptance criteria" == heading.lower() for heading in contract["headings"]))


class TransitionTests(unittest.TestCase):
    def test_legal_flow(self):
        for old, new in (
            ("planned", "ready"),
            ("ready", "assigned"),
            ("assigned", "in_progress"),
            ("in_progress", "awaiting_review"),
            ("awaiting_review", "validated"),
            ("validated", "complete"),
            ("awaiting_review", "changes_requested"),
            ("changes_requested", "in_progress"),
            ("blocked", "ready"),
            ("failed", "assigned"),
        ):
            self.assertTrue(state_mod.can_transition(old, new), "%s -> %s should be legal" % (old, new))

    def test_illegal_flow(self):
        for old, new in (
            ("planned", "complete"),
            ("validated", "in_progress"),
            ("complete", "in_progress"),
            ("cancelled", "ready"),
            ("awaiting_review", "complete"),
        ):
            self.assertFalse(state_mod.can_transition(old, new), "%s -> %s should be illegal" % (old, new))

    def test_apply_transition_records_history(self):
        state = state_mod.load_state(EXAMPLE)
        state_mod.apply_transition(state, "NOTIFY-001", "ready", "orchestrator", "deps satisfied")
        module = state_mod.module_by_id(state, "NOTIFY-001")
        self.assertEqual(module["status"], "ready")
        self.assertEqual(module["history"][-1]["to"], "ready")
        self.assertEqual(module["history"][-1]["by"], "orchestrator")


class OverlapTests(unittest.TestCase):
    def test_overlap_detection(self):
        self.assertTrue(state_mod.overlaps(["src/auth/**"], ["src/auth/session/**"]))
        self.assertTrue(state_mod.overlaps(["src/auth/**"], ["src/auth/**"]))
        self.assertFalse(state_mod.overlaps(["src/auth/**"], ["src/users/**"]))

    def test_cycle_detection(self):
        state = {
            "project": {},
            "modules": [
                {"module_id": "A-001", "status": "ready"},
                {"module_id": "B-001", "status": "ready"},
            ],
            "agents": [],
            "edges": [
                {"from": "A-001", "to": "B-001"},
                {"from": "B-001", "to": "A-001"},
            ],
            "shared_zones": [],
            "docs": {},
        }
        # dependency_depth is where the cycle surfaces
        with self.assertRaises(Exception):
            state_mod.dependency_depth(state, "A-001")
        # and the board must refuse to schedule either module rather than plan on a broken graph
        board = state_mod.compute_board(ROOT, state)
        self.assertEqual(board["ready"], [])

    def test_cycle_is_reported_by_the_integrity_checks(self):
        from tplib import checks

        state = {
            "project": {},
            "modules": [
                {"module_id": "A-001", "status": "ready", "contract": "modules/A-001.md"},
                {"module_id": "B-001", "status": "ready", "contract": "modules/B-001.md"},
            ],
            "agents": [],
            "edges": [
                {"from": "A-001", "to": "B-001", "type": "contract", "status": "frozen"},
                {"from": "B-001", "to": "A-001", "type": "contract", "status": "frozen"},
            ],
            "shared_zones": [],
            "docs": {},
        }
        issues = []
        checks.check_edges(ROOT, state, issues)
        codes = [item["code"] for item in issues]
        self.assertIn("edge.cycle", codes, codes)


if __name__ == "__main__":
    unittest.main()
