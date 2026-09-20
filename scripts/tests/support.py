"""Shared helpers for the toolkit tests."""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)
ROOT = os.path.dirname(SCRIPTS_DIR)
EXAMPLE = os.path.join(ROOT, "examples", "example-saas")
SCRATCH = os.path.join(ROOT, ".tmp", "tests")
TP = os.path.join(SCRIPTS_DIR, "tp.py")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)


def remove_tree(path: str) -> None:
    """Delete a tree even on Windows, where git objects are read-only and locked."""
    if not os.path.isdir(path):
        return
    for current, dirs, files in os.walk(path):
        for name in list(dirs) + list(files):
            try:
                os.chmod(os.path.join(current, name), stat.S_IWRITE)
            except OSError:
                pass
    shutil.rmtree(path, ignore_errors=True)


def scratch_dir(name: str, clean: bool = True) -> str:
    path = os.path.join(SCRATCH, name)
    if clean:
        remove_tree(path)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def run_tp(args, cwd=None, env=None):
    """Run `tp.py` in a subprocess. Returns (returncode, stdout, stderr)."""
    completed = subprocess.run(
        [sys.executable, TP] + list(args),
        cwd=cwd or ROOT,
        env=dict(os.environ, **(env or {})),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def copy_project(destination: str, include_examples: bool = True) -> str:
    """Copy the template into `destination`, excluding VCS/scratch directories."""
    patterns = [".git", ".tmp", ".freebuff", "__pycache__", "*.pyc"]
    if not include_examples:
        patterns.append("examples")
    remove_tree(destination)
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(*patterns), dirs_exist_ok=True)
    return destination


def git(args, cwd):
    return subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
