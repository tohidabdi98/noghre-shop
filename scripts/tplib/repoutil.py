"""repoutil — repository helpers shared by the toolkit.

Root discovery, file walking, placeholder detection/replacement, lightweight git wrappers, and the
text-extraction helpers used by the context and validation layers. Standard library only.
"""

from __future__ import annotations

import datetime
import io
import os
import re
import subprocess

try:  # PyYAML is optional: prefer it for reading when available, fall back to yamlmini.
    import yaml as _pyyaml  # type: ignore
except Exception:  # pragma: no cover - exercised on machines without PyYAML
    _pyyaml = None

from . import yamlmini  # noqa: E402  (local package import)

PLACEHOLDERS = (
    "{{PROJECT_ID}}",
    "{{PROJECT_NAME}}",
    "{{PROJECT_DESCRIPTION}}",
    "{{OWNER}}",
    "{{REPO_URL}}",
    "{{DEFAULT_BRANCH}}",
)

TEXT_SUFFIXES = (
    ".md",
    ".markdown",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".txt",
    ".toml",
    ".ini",
    ".cfg",
    ".ipynb",
    ".sh",
)

SKIP_DIR_PARTS = (
    ".git",
    ".freebuff",
    ".tmp",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".cache",
)


# --------------------------------------------------------------------------------------
# Files and text
# --------------------------------------------------------------------------------------
def find_root(start: str = ".") -> str:
    """Walk upwards from `start` until a directory containing state/project.yaml is found."""
    current = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(current, "state", "project.yaml")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise FileNotFoundError(
                "no TemplateProject root found above %s (expected state/project.yaml)" % os.path.abspath(start)
            )
        current = parent


def framework_root(start: str = ".") -> str:
    """Nearest ancestor (including `start`) that contains scripts/tp.py.

    For a derived project this equals the project root. Inside this template it lets nested sample
    projects (examples/…, test fixtures) resolve framework-owned files such as the agent registry.
    """
    current = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(current, "scripts", "tp.py")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return os.path.abspath(start)
        current = parent


def search_roots(root: str):
    """Where to look for framework-owned files: the project root, then the framework root."""
    root = os.path.abspath(root)
    framework = framework_root(root)
    return [root] if framework == root else [root, framework]


def read_text(path: str) -> str:
    with io.open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def write_text(path: str, text: str) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def iter_files(root: str, suffixes=None, skip_hidden=True):
    """Yield repository-relative paths, skipping VCS/scratch/dependency directories."""
    for current, dirs, files in os.walk(root):
        relative_dir = os.path.relpath(current, root)
        if relative_dir == ".":
            relative_dir = ""
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_DIR_PARTS and not (skip_hidden and name.startswith(".") and name not in (".github",))
        ]
        for name in sorted(files):
            if skip_hidden and name.startswith(".") and name not in (
                ".gitignore",
                ".editorconfig",
                ".env.example",
                ".gitmessage",
            ):
                continue
            if suffixes and not name.endswith(tuple(suffixes)):
                continue
            yield os.path.join(relative_dir, name).replace(os.sep, "/")


def markdown_files(root: str):
    return [path for path in iter_files(root, suffixes=(".md", ".markdown"))]


def load_yaml_file(path: str):
    """Read a YAML file, preferring PyYAML when it is installed."""
    text = read_text(path)
    if _pyyaml is not None:
        try:
            return _pyyaml.safe_load(text)
        except Exception as exc:  # pragma: no cover - depends on host
            raise yamlmini.YamlError("%s: %s" % (path, exc))
    return yamlmini.loads(text, path)


def dump_yaml(header: str, data) -> str:
    """Serialise state with a canonical header (keeps generated files readable)."""
    body = yamlmini.dumps(data)
    return (header.rstrip() + "\n\n" + body) if header else body


def yaml_backend() -> str:
    return "pyyaml" if _pyyaml is not None else "yamlmini (built-in subset parser)"


# --------------------------------------------------------------------------------------
# Placeholders
# --------------------------------------------------------------------------------------
def replace_placeholders(root: str, mapping, exclude_paths=(), skip_prefixes=("examples/",)):
    """Replace {{TOKEN}} placeholders across text files. Returns [(path, count)].

    Used by `tp.py bootstrap` so a copied template stops advertising itself as a template.
    """
    changed = []
    excluded = {path.replace("\\", "/") for path in exclude_paths}
    for relative in iter_files(root, suffixes=TEXT_SUFFIXES):
        if relative in excluded or relative.startswith(tuple(skip_prefixes)):
            continue
        path = os.path.join(root, relative)
        try:
            text = read_text(path)
        except OSError:
            continue
        updated = text
        count = 0
        for token, value in mapping.items():
            if token in updated:
                count += updated.count(token)
                updated = updated.replace(token, value)
        if updated != text:
            write_text(path, updated)
            changed.append((relative, count))
    return changed


def find_placeholders(root: str, exclude_paths=()):
    """Return [(relative_path, line_number, token)] for every unreplaced placeholder."""
    found = []
    excluded = {path.replace("\\", "/") for path in exclude_paths}
    for relative in iter_files(root, suffixes=TEXT_SUFFIXES):
        if relative in excluded or relative.startswith("examples/"):
            continue
        try:
            text = read_text(os.path.join(root, relative))
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for token in PLACEHOLDERS:
                if token in line:
                    found.append((relative, number, token))
                    break
    return found


# --------------------------------------------------------------------------------------
# Text extraction
# --------------------------------------------------------------------------------------
_FENCE_RE = re.compile(r"^```ya?ml\s*$")


def extract_fenced_yaml(text: str, source: str = "<text>"):
    """Return the first ```yaml fenced block parsed as a mapping (or None if absent)."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if _FENCE_RE.match(line.strip()):
            start = index + 1
            break
    if start is None:
        return None
    block = []
    for line in lines[start:]:
        if line.strip().startswith("```"):
            break
        block.append(line)
    if not block:
        return None
    return yamlmini.loads("\n".join(block), source)


def headings(text: str, level: int = 2):
    """Return the heading texts at the given markdown level."""
    prefix = "#" * level + " "
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix) and not stripped.startswith(prefix + "#"):
            found.append(stripped[len(prefix) :].strip())
    return found


def extract_sections(text: str, tokens, levels=(2, 3)):
    """Return {token: section_text} for headings containing any of `tokens`.

    A section runs from its heading to the next heading of the same or higher level. Used to build
    narrow context packs: a module only receives the requirement/UX sections it cites.
    """
    lines = text.splitlines()
    heading_positions = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        hashes = len(stripped) - len(stripped.lstrip("#"))
        if hashes in levels and stripped[hashes : hashes + 1] == " ":
            heading_positions.append((index, hashes, stripped[hashes:].strip()))
    result = {}
    for token in tokens:
        for position, (index, hashes, title) in enumerate(heading_positions):
            if token in title:
                end = len(lines)
                for next_index, next_hashes, _ in heading_positions[position + 1 :]:
                    if next_hashes <= hashes:
                        end = next_index
                        break
                result[token] = "\n".join(lines[index:end]).strip()
                break
    return result


def relative(root: str, path: str) -> str:
    return os.path.relpath(path, root).replace(os.sep, "/")


def today() -> str:
    return datetime.date.today().isoformat()


def timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


# --------------------------------------------------------------------------------------
# Git
# --------------------------------------------------------------------------------------
def git(args, cwd: str, check: bool = False):
    """Run a git command. Returns (returncode, stdout, stderr) — stdout is NOT stripped.

    Careful: Python's `str.strip()` treats \\x1c–\\x1f as whitespace, so stripping stdout here would
    destroy the field/record separators used by `commits_between`.
    """
    if isinstance(args, str):
        args = args.split()
    try:
        completed = subprocess.run(
            ["git"] + list(args),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return 127, "", "git is not installed"
    if check and completed.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), completed.stderr.strip()))
    return completed.returncode, completed.stdout, completed.stderr.strip()


def git_available(cwd: str) -> bool:
    code, out, _ = git(["rev-parse", "--is-inside-work-tree"], cwd)
    return code == 0 and out.strip() == "true"


def current_branch(cwd: str) -> str:
    code, out, _ = git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    return out.strip() if code == 0 else ""


def commits_between(cwd: str, base: str, head: str = "HEAD"):
    """Return [(sha, subject, body)] for commits in base..head."""
    code, out, err = git(["log", "--format=%H%x1f%s%x1f%b%x1e", "%s..%s" % (base, head)], cwd)
    if code != 0:
        raise RuntimeError("git log failed: %s" % (err or out))
    commits = []
    for chunk in out.split("\x1e"):
        chunk = chunk.strip("\r\n")
        if not chunk.strip():
            continue
        parts = chunk.split("\x1f")
        if len(parts) < 3:
            continue
        commits.append((parts[0].strip(), parts[1].strip(), parts[2]))
    return commits


def changed_paths(cwd: str, base: str, head: str = "HEAD"):
    code, out, err = git(["diff", "--name-only", "%s...%s" % (base, head)], cwd)
    if code != 0:
        raise RuntimeError("git diff failed: %s" % (err or out))
    return [line.strip() for line in out.splitlines() if line.strip()]
