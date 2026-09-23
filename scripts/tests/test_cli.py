"""tp.py end-to-end: validation, board, readiness, context, bootstrap on a fresh copy."""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `support` importable

from support import EXAMPLE, ROOT, SCRATCH, copy_project, remove_tree, run_tp, scratch_dir  # noqa: E402

from tplib import repoutil  # noqa: E402


class ExampleProjectTests(unittest.TestCase):
    def test_validate_strict_passes_on_the_example(self):
        code, out, err = run_tp(["validate", "--strict", "--root", EXAMPLE])
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        self.assertIn("0 error(s)", out)

    def test_status_json_is_parseable(self):
        code, out, _ = run_tp(["status", "--json", "--root", EXAMPLE])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["project"]["id"], "example-saas")
        self.assertEqual(len(payload["modules"]), 5)

    def test_ready_reports_the_next_module(self):
        code, out, _ = run_tp(["ready", "--root", EXAMPLE])
        self.assertEqual(code, 0)
        self.assertIn("NOTIFY-001", out)
        self.assertIn("start with: python scripts/tp.py start --module NOTIFY-001", out)

    def test_context_writes_a_pack_file(self):
        target = os.path.join(ROOT, ".tmp", "tests", "ctx.md")
        code, out, _ = run_tp(
            ["context", "--module", "PROJECT-001", "--agent", "impl-project-001", "--out", target, "--root", EXAMPLE]
        )
        self.assertEqual(code, 0, out)
        self.assertTrue(os.path.isfile(target))
        text = repoutil.read_text(target)
        self.assertIn("Layer 4 — Your module contract", text)
        self.assertIn("PROJECT-001", text)

    def test_validate_reports_the_example_when_asked_from_the_template_root(self):
        # A nested sample must still resolve framework files (registry, scripts) — no link errors.
        code, out, _ = run_tp(["validate", "--root", EXAMPLE])
        self.assertNotIn("link.missing", out)


class TemplateRootTests(unittest.TestCase):
    """Placeholder handling across repo states.

    In a pristine template the tokens are not defects: they collapse into one info notice and
    validation stays green, so a fresh clone does not look broken. Once a project is initialised
    (`initialised: true`), the same tokens become blocking errors — that is what stops a
    placeholder from reaching a real repository. Both behaviours are asserted against a fixture
    (a full copy of this template reset to the pristine state, token injected at test time),
    because a derived project like NoghreShop is already bootstrapped: there, ROOT has no
    placeholders and the pristine expectations would be vacuous or wrong.
    """

    def _pristine_fixture(self) -> str:
        """Full copy of this template, reset to the un-bootstrapped state, token injected."""
        fixture = scratch_dir("pristine-template-fixture")
        copy_project(fixture, include_examples=False)
        state_path = os.path.join(fixture, "state", "project.yaml")
        text = repoutil.read_text(state_path).replace("initialised: true", "initialised: false")
        token = "{" * 2 + "PROJECT_ID" + "}" * 2  # assembled — no literal token may live in this file
        text = text.replace('project_id: "noghre-shop"', 'project_id: "%s"' % token)
        repoutil.write_text(state_path, text)
        return fixture

    def test_unbootstrapped_template_reports_a_single_notice(self):
        code, out, _ = run_tp(["validate", "--root", self._pristine_fixture()])
        self.assertEqual(code, 0, out)
        self.assertIn("template.uninitialised", out)
        self.assertNotIn("placeholder.unreplaced", out)
        self.assertIn("0 error(s)", out)

    def test_initialised_project_treats_placeholders_as_errors(self):
        fixture = self._pristine_fixture()
        state_path = os.path.join(fixture, "state", "project.yaml")
        # a project that has been initialised must not ship a stray token
        text = repoutil.read_text(state_path).replace("initialised: false", "initialised: true")
        repoutil.write_text(state_path, text)
        code, out, _ = run_tp(["validate", "--root", fixture])
        self.assertEqual(code, 1)
        self.assertIn("placeholder.unreplaced", out)
        self.assertIn("state/project.yaml", out)

    def test_validation_works_without_pyyaml(self):
        """The framework claims zero dependencies: mask PyYAML and the built-in parser takes over."""
        mask = os.path.join(SCRATCH, "noyaml")
        if not os.path.isdir(mask):
            os.makedirs(mask)
        repoutil.write_text(
            os.path.join(mask, "yaml.py"),
            'raise ImportError("pyyaml deliberately unavailable")\n',
        )
        code, out, err = run_tp(["validate", "--strict"], env={"PYTHONPATH": mask})
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        self.assertIn("yamlmini", out)
        code, out, _ = run_tp(["validate", "--strict", "--root", EXAMPLE], env={"PYTHONPATH": mask})
        self.assertEqual(code, 0, out)
        self.assertIn("yamlmini", out)

    def test_verify_list_runs_without_a_stack(self):
        # verify.py is exercised directly (it is not a tp.py subcommand)
        import subprocess
        import sys

        completed = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "verify.py"), "--list"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("verify: root=", completed.stdout)

    def test_verify_strict_fails_when_nothing_is_configured(self):
        import subprocess
        import sys

        completed = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "verify.py"), "--strict"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(completed.returncode, 1, completed.stdout)


class FreshCopyTests(unittest.TestCase):
    """The documented copy → bootstrap flow must work on a clean copy of the template."""

    def test_bootstrap_can_create_the_project_directory_itself(self):
        # outside the template on purpose: copying a project into itself is refused
        with tempfile.TemporaryDirectory() as parent:
            self._create_project(os.path.join(parent, "my-project"))

    def _create_project(self, destination):
        code, out, err = run_tp(
            [
                "bootstrap",
                destination,
                "--name",
                "Created In Place",
                "--id",
                "created-in-place",
                "--profile",
                "backend",
                "--adopt-env",
            ]
        )
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        self.assertIn("copied the template", out)
        self.assertIn("adopt-env", out)

        project = repoutil.load_yaml_file(os.path.join(destination, "state", "project.yaml"))
        self.assertEqual(project["project_id"], "created-in-place")
        self.assertTrue(project["initialised"])
        self.assertTrue(os.path.isfile(os.path.join(destination, ".env")))
        self.assertFalse(os.path.exists(os.path.join(destination, ".git")))

        code, out, _ = run_tp(["validate", "--strict", "--root", destination])
        self.assertEqual(code, 0, out)

    def test_bootstrap_refuses_a_destination_inside_the_template(self):
        inside = os.path.join(ROOT, ".tmp", "tests", "inside-the-template")
        code, _, err = run_tp(["bootstrap", inside, "--name", "Nope"], cwd=ROOT)
        self.assertEqual(code, 1)
        self.assertIn("outside the template", err)

    def test_bootstrap_then_validate(self):
        destination = scratch_dir("fresh-project")
        copy_project(destination)

        code, out, err = run_tp(
            [
                "bootstrap",
                "--name",
                "Fresh Project",
                "--id",
                "fresh-project",
                "--owner",
                "tester",
                "--profile",
                "backend",
                "--root",
                destination,
            ]
        )
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        self.assertIn("bootstrap:", out)

        project = repoutil.load_yaml_file(os.path.join(destination, "state", "project.yaml"))
        self.assertEqual(project["project_id"], "fresh-project")
        self.assertEqual(project["name"], "Fresh Project")
        self.assertEqual(project["profile"], "backend")

        from tplib import checks

        config = checks.load_config(destination)
        remaining = repoutil.find_placeholders(
            destination, exclude_paths=config.get("placeholder_check_exclude") or ()
        )
        self.assertEqual(remaining, [], "placeholders left behind: %s" % remaining)

        code, out, err = run_tp(["validate", "--strict", "--root", destination])
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))

        code, out, _ = run_tp(["status", "--root", destination])
        self.assertEqual(code, 0)
        self.assertIn("no modules registered yet", out)

        remove_tree(destination)

    def test_new_module_scaffold_then_start(self):
        destination = scratch_dir("module-project")
        copy_project(destination)
        run_tp(["bootstrap", "--name", "Module Project", "--id", "module-project", "--root", destination])

        code, out, err = run_tp(
            ["new-module", "--id", "AUTH-001", "--name", "Authentication", "--root", destination]
        )
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        self.assertTrue(os.path.isfile(os.path.join(destination, "modules", "AUTH-001.md")))

        # a fresh scaffold is intentionally incomplete: criteria and validation are empty
        code, out, _ = run_tp(["validate", "--root", destination])
        self.assertEqual(code, 1)
        self.assertIn("contract.no_criteria", out)

        # fill the contract the way the decomposition agent would
        contract_path = os.path.join(destination, "modules", "AUTH-001.md")
        text = repoutil.read_text(contract_path)
        text = text.replace(
            "acceptance_criteria: []",
            'acceptance_criteria:\n  - id: AC-1\n    criterion: "sign in works"\n    evidence: "tests/auth/signin.test.ts"',
        ).replace(
            "validation: []               # commands that must pass",
            'validation:\n  - command: python scripts/verify.py\n    expects: exit 0',
        )
        text = text.replace("requirement_refs: []", 'requirement_refs: ["FR-AUTH-1"]')
        repoutil.write_text(contract_path, text)

        # add the requirement it cites so traceability passes
        requirements = os.path.join(destination, "docs", "project", "requirements.md")
        repoutil.write_text(
            requirements,
            repoutil.read_text(requirements)
            + "\n\n### FR-AUTH-1 — Sign in\n\n- **Acceptance criteria:**\n  - [ ] AC-1 — works\n",
        )

        code, out, _ = run_tp(["validate", "--root", destination])
        self.assertEqual(code, 0, out)

        code, out, err = run_tp(
            ["start", "--module", "AUTH-001", "--agent", "impl-auth-001", "--root", destination]
        )
        self.assertEqual(code, 0, "stdout=%s\nstderr=%s" % (out, err))
        modules = repoutil.load_yaml_file(os.path.join(destination, "state", "modules.yaml"))
        self.assertEqual(modules["modules"][0]["status"], "in_progress")
        contract = repoutil.read_text(contract_path)
        self.assertIn("status: in_progress", contract)
        agents = repoutil.load_yaml_file(os.path.join(destination, "state", "agents.yaml"))
        self.assertEqual(agents["agents"][0]["agent_id"], "impl-auth-001")

        code, out, _ = run_tp(["validate", "--strict", "--root", destination])
        self.assertEqual(code, 0, out)

        remove_tree(destination)


if __name__ == "__main__":
    unittest.main()
