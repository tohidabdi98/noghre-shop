#!/usr/bin/env python3
"""verify.py — run this project's typecheck / lint / format / test pipeline.

The Architecture Agent fills in `scripts/verify.config.yaml` during the architecture phase. Until
then, this script detects the stack and uses sensible defaults, and says clearly what it did and
did not run.

    python scripts/verify.py            # run everything configured
    python scripts/verify.py --list     # show what would run, change nothing
    python scripts/verify.py --strict   # fail when nothing is configured (use in CI once set up)
    python scripts/verify.py --only test

Exit code 0 = every executed command passed. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tplib import repoutil  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    try:  # legacy Windows consoles cannot encode the box characters used in the report
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - non-standard streams
        pass

SECTIONS = ("install", "typecheck", "lint", "format_check", "test", "e2e", "security")

DEFAULTS = {
    "node": {
        "install": ["npm ci"],
        "typecheck": ["npx --no-install tsc --noEmit"],
        "lint": ["npx --no-install eslint ."],
        "format_check": ["npx --no-install prettier --check ."],
        "test": ["npm test --silent"],
    },
    "python": {
        "typecheck": ["python -m mypy ."],
        "lint": ["python -m ruff check ."],
        "format_check": ["python -m ruff format --check ."],
        "test": ["python -m pytest -q"],
    },
    "go": {
        "typecheck": ["go build ./..."],
        "lint": ["go vet ./..."],
        "test": ["go test ./..."],
    },
    "rust": {
        "typecheck": ["cargo check --quiet"],
        "lint": ["cargo clippy --quiet -- -D warnings"],
        "format_check": ["cargo fmt --check"],
        "test": ["cargo test --quiet"],
    },
}


def load_config(root):
    path = os.path.join(root, "scripts", "verify.config.yaml")
    if not os.path.isfile(path):
        return {}
    return repoutil.load_yaml_file(path) or {}


def detect_stack(root):
    if os.path.isfile(os.path.join(root, "go.mod")):
        return "go"
    if os.path.isfile(os.path.join(root, "Cargo.toml")):
        return "rust"
    package_json = os.path.join(root, "package.json")
    if os.path.isfile(package_json):
        return "node"
    if os.path.isfile(os.path.join(root, "pyproject.toml")) or os.path.isfile(os.path.join(root, "setup.py")):
        return "python"
    return None


def node_install_command(root):
    if os.path.isfile(os.path.join(root, "pnpm-lock.yaml")):
        return "pnpm install --frozen-lockfile"
    if os.path.isfile(os.path.join(root, "yarn.lock")):
        return "yarn install --frozen-lockfile"
    if os.path.isfile(os.path.join(root, "bun.lockb")) or os.path.isfile(os.path.join(root, "bun.lock")):
        return "bun install --frozen-lockfile"
    return "npm ci"


def node_scripts(root):
    try:
        with open(os.path.join(root, "package.json"), "r", encoding="utf-8") as handle:
            return (json.load(handle).get("scripts") or {})
    except Exception:
        return {}


def resolve_commands(root, config):
    """Return {section: [commands]} merging explicit config over detected defaults."""
    stack = detect_stack(root)
    commands = {section: [] for section in SECTIONS}
    if stack == "node":
        scripts = node_scripts(root)
        manager = node_install_command(root).split()[0]
        detected = dict(DEFAULTS["node"])
        detected["install"] = [node_install_command(root)]
        for section, script in (("typecheck", "typecheck"), ("lint", "lint"), ("format_check", "format"), ("test", "test"), ("e2e", "e2e")):
            if script in scripts:
                detected[section] = ["%s run %s" % (manager, script)]
            elif section in ("lint", "format_check", "typecheck"):
                detected[section] = []
        detected["test"] = detected["test"] if "test" in scripts else []
    elif stack == "python":
        detected = dict(DEFAULTS["python"])
        if shutil.which("pytest") is None and not _module_available("pytest"):
            detected["test"] = ["python -m unittest discover -q"]
        if shutil.which("ruff") is None and not _module_available("ruff"):
            detected["lint"] = []
            detected["format_check"] = []
        if shutil.which("mypy") is None and not _module_available("mypy"):
            detected["typecheck"] = []
    elif stack in ("go", "rust"):
        detected = dict(DEFAULTS[stack])
    else:
        detected = {}
    for section in SECTIONS:
        explicit = config.get(section) or []
        commands[section] = [str(item) for item in explicit] if explicit else list(detected.get(section) or [])
    return commands, stack


def _module_available(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False


def run(root, command):
    print("-> %s" % command, flush=True)
    completed = subprocess.run(command, cwd=root, shell=True)
    return completed.returncode


def _configure_output():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv=None):
    _configure_output()
    parser = argparse.ArgumentParser(prog="verify.py", description="run the project's checks")
    parser.add_argument("--root", default=None)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--only", action="append", choices=SECTIONS)
    args = parser.parse_args(argv)

    root = repoutil.find_root(args.root or os.getcwd())
    config = load_config(args.root or root)
    commands, stack = resolve_commands(root, config)
    sections = args.only or list(SECTIONS)

    print("verify: root=%s stack=%s yaml=%s" % (root, stack or "not detected", repoutil.yaml_backend()))
    if config.get("notes"):
        print("notes: %s" % str(config["notes"]).strip()[:400])

    planned = [(section, command) for section in sections for command in commands.get(section) or []]
    if args.list or not planned:
        if not planned:
            print(
                "\nNothing is configured to run yet.\n"
                "  · Fill in scripts/verify.config.yaml during the architecture phase "
                "(docs/project/architecture.md §11).\n"
                "  · Sections: %s\n"
                "  · Example:\n"
                "      test:\n"
                "        - \"npm test\"\n"
                "        - \"python scripts/tp.py validate\"\n"
                % ", ".join(SECTIONS)
            )
        else:
            print("\nwould run:")
            for section, command in planned:
                print("  [%s] %s" % (section, command))
        if args.strict and not planned:
            print("\nstrict mode: nothing configured → failure")
            return 1
        return 0

    failures = []
    for section, command in planned:
        code = run(root, command)
        if code != 0:
            failures.append((section, command, code))
            print("x [%s] failed (exit %d): %s" % (section, command, code))

    print("\n%d command(s) run · %d failure(s)" % (len(planned), len(failures)))
    for section, command, code in failures:
        print("  x [%s] %s (exit %d)" % (section, command, code))
    if failures:
        return 1
    print("ok verify passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
