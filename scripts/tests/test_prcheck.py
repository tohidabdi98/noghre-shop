"""pr-check: the CI gate for branch naming, commit trailers, ownership and PR completeness."""

from __future__ import annotations

import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `support` importable

from support import EXAMPLE, ROOT, git, remove_tree, run_tp, scratch_dir  # noqa: E402

from tplib import repoutil  # noqa: E402

BODY_OK = """## Module
AUTH-001 — contract modules/AUTH-001.md
## Agent
impl-auth-001 (implementation)
## Summary
Adds the reset-token expiry guard.
## Acceptance criteria
- AC-2 — single use and 30 minute expiry: met
## Tests executed
python scripts/verify.py -> exit 0 (41 tests)
## Validation results
python scripts/tp.py validate -> exit 0
## Known limitations
none
"""


class PullRequestCheckTests(unittest.TestCase):
    """A scratch repository built from the example project, with a real branch and commits."""

    def setUp(self):
        self.repo = scratch_dir("prcheck-repo")
        remove_tree(self.repo)
        os.makedirs(self.repo)
        shutil.copytree(
            EXAMPLE,
            self.repo,
            ignore=shutil.ignore_patterns("__pycache__"),
            dirs_exist_ok=True,
        )
        # the example references the framework's scripts; give the scratch repo its own copy
        os.makedirs(os.path.join(self.repo, "scripts"), exist_ok=True)
        for name in ("tp.py", "verify.py"):
            shutil.copy(os.path.join(ROOT, "scripts", name), os.path.join(self.repo, "scripts", name))
        shutil.copytree(os.path.join(ROOT, "scripts", "tplib"), os.path.join(self.repo, "scripts", "tplib"))
        shutil.copy(
            os.path.join(ROOT, "scripts", "validate.config.yaml"),
            os.path.join(self.repo, "scripts", "validate.config.yaml"),
        )
        git(["init", "-b", "main"], self.repo)
        git(["config", "user.email", "test@example.invalid"], self.repo)
        git(["config", "user.name", "test"], self.repo)
        git(["add", "."], self.repo)
        git(["commit", "-m", "chore(repo): example baseline"], self.repo)

    def tearDown(self):
        remove_tree(self.repo)

    def _commit(self, path, content, message, trailers=True):
        full = os.path.join(self.repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        repoutil.write_text(full, content)
        git(["add", path], self.repo)
        body = message
        if trailers:
            body += (
                "\n\nAgent: impl-auth-001\nAgent-Role: implementation\n"
                "Module: AUTH-001\nValidated-With: python scripts/verify.py (exit 0)"
            )
        git(["commit", "-m", body], self.repo)

    def test_clean_branch_passes(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/auth/token-guard.ts", "export const guard = true;\n", "feat(AUTH-001): add reset token expiry guard")
        body_file = os.path.join(self.repo, "pr-body.md")
        repoutil.write_text(body_file, BODY_OK)
        code, out, err = run_tp(["pr-check", "--base", "main", "--body-file", body_file, "--root", self.repo])
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        self.assertIn("pr-check passed", out)

    def test_forbidden_path_is_rejected(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/billing/invoice.ts", "export const x = 1;\n", "feat(AUTH-001): touch billing")
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", BODY_OK, "--root", self.repo])
        self.assertEqual(code, 1)
        self.assertIn("forbidden_to_modify", out)

    def test_path_outside_allowed_is_rejected(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/reports/monthly.ts", "export const y = 1;\n", "feat(AUTH-001): add report code")
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", BODY_OK, "--root", self.repo])
        self.assertEqual(code, 1)
        self.assertIn("outside allowed_to_modify", out)

    def test_missing_trailers_are_rejected(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/auth/x.ts", "export const z = 1;\n", "feat(AUTH-001): no trailers here", trailers=False)
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", BODY_OK, "--root", self.repo])
        self.assertEqual(code, 1)
        self.assertIn("missing `Agent:` trailer", out)

    def test_unconventional_commit_subject_is_rejected(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/auth/y.ts", "export const w = 1;\n", "fixed stuff")
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", BODY_OK, "--root", self.repo])
        self.assertEqual(code, 1)
        self.assertIn("conventional type", out)

    def test_bad_branch_name_is_rejected(self):
        git(["checkout", "-b", "feature/auth"], self.repo)
        self._commit("src/auth/z.ts", "export const v = 1;\n", "feat(AUTH-001): something")
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", BODY_OK, "--root", self.repo])
        self.assertEqual(code, 1)
        self.assertIn("does not match agent/<agent-id>/<MODULE-ID>", out)

    def test_framework_managed_paths_are_allowed(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/auth/x.ts", "export const t = 1;\n", "feat(AUTH-001): add auth guard")
        repoutil.write_text(
            os.path.join(self.repo, "reports", "validation-AUTH-001.md"),
            "# Validation — AUTH-001\n\npython scripts/verify.py -> exit 0\n",
        )
        git(["add", "reports/validation-AUTH-001.md"], self.repo)
        git(["commit", "-m", "docs(AUTH-001): validation report\n\nAgent: impl-auth-001\nModule: AUTH-001\nValidated-With: python scripts/verify.py"], self.repo)
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", BODY_OK, "--root", self.repo])
        self.assertEqual(code, 0, out)
        self.assertIn("framework-managed paths", out)

    def test_incomplete_pr_body_is_rejected(self):
        git(["checkout", "-b", "agent/impl-auth-001/AUTH-001"], self.repo)
        self._commit("src/auth/q.ts", "export const u = 1;\n", "feat(AUTH-001): add something")
        code, out, _ = run_tp(["pr-check", "--base", "main", "--body", "## Module\nAUTH-001\n", "--root", self.repo])
        self.assertEqual(code, 1)
        self.assertIn("missing the `Validation results` section", out)


class BranchNameTests(unittest.TestCase):
    """CI hands pr-check a remote-tracking ref; the naming rules must ignore the prefix."""

    def _load_cli(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("tp_cli", os.path.join(ROOT, "scripts", "tp.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_ref_prefixes_are_stripped(self):
        branch_name = self._load_cli()._branch_name
        cases = {
            "agent/impl-auth-001/AUTH-001": "agent/impl-auth-001/AUTH-001",
            "refs/heads/agent/impl-auth-001/AUTH-001": "agent/impl-auth-001/AUTH-001",
            "origin/agent/impl-auth-001/AUTH-001": "agent/impl-auth-001/AUTH-001",
            "refs/remotes/origin/human/t/anav": "human/t/anav",
            "main": "main",
        }
        for given, expected in cases.items():
            self.assertEqual(branch_name(given), expected, given)


if __name__ == "__main__":
    unittest.main()
