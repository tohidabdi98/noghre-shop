"""yamlmini — a small, predictable reader/writer for the YAML subset this template uses.

Why this exists: the framework must work on a fresh machine with **no packages installed**. The
state files are simple YAML (block maps, block sequences, inline lists/maps, quoted and plain
scalars, comments), so a ~300-line subset parser is enough — and it fails loudly instead of
silently mis-parsing.

Supported
    * block mappings                 key: value
    * block sequences                - item        /  - key: value (with aligned continuation keys)
    * nested structures by indentation (2 spaces is the convention; any consistent indent works)
    * inline flow collections        [a, b]        {k: v, k2: v2}
    * quoted scalars                 "..."  '...'   (double quotes support \\n, \\t, \\", \\\\)
    * plain scalars                  int, float, true/false, null/~, strings
    * block scalars                  |  |-  >  >-   (trailing newlines clipped, folded joins with space)
    * comments                       full-line and trailing (`#` outside quotes, preceded by space)
    * document start markers         --- / ...  (ignored)

Not supported (raises a clear error): anchors/aliases (&, *), tags (!), tabs for indentation,
multi-document streams, and YAML 1.1 booleans (`yes`/`no`/`on`/`off` are strings here, deliberately).
"""

from __future__ import annotations

import io
import os
import re

__all__ = ["YamlError", "load", "load_file", "dumps", "dump_file", "loads"]

_BLOCK_INDICATORS = ("|", "|-", "|+", ">", ">-", ">+")
_SEQ_RE = re.compile(r"^([ \t]*)-\s*(.*)$")


class YamlError(ValueError):
    """Raised when the input is outside the supported YAML subset (or malformed)."""


# --------------------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------------------
def loads(text: str, source: str = "<string>"):
    """Parse a YAML subset document. Returns dict/list/scalar (usually dict)."""
    if text is None:
        return None
    tokens, raw_lines = _tokenize(text, source)
    if not tokens:
        return {}
    value, index = _parse_node(tokens, 0, raw_lines, source)
    if index != len(tokens):
        tok = tokens[index]
        raise YamlError(
            "%s: unexpected content at line %d (indent %d): %r"
            % (source, tok["raw"] + 1, tok["indent"], tok["text"])
        )
    return value


def load(stream, source: str = "<stream>"):
    """Parse from a string or a file-like object."""
    if hasattr(stream, "read"):
        text = stream.read()
        return loads(text, getattr(stream, "name", source))
    return loads(stream, source)


def load_file(path: str):
    """Parse a YAML subset file from disk."""
    with io.open(path, "r", encoding="utf-8") as handle:
        return loads(handle.read(), path)


def _tokenize(text: str, source: str):
    raw_lines = text.splitlines()
    tokens = []
    for index, raw in enumerate(raw_lines):
        if "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
            raise YamlError("%s: line %d: tabs are not allowed for indentation" % (source, index + 1))
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        if line.strip() in ("---", "..."):
            continue
        match = _SEQ_RE.match(line)
        if match:
            whitespace, rest = match.group(1), match.group(2)
            tokens.append({"indent": len(whitespace) + 2, "text": rest.strip(), "seq": True, "raw": index})
        else:
            indent = len(line) - len(line.lstrip(" "))
            tokens.append({"indent": indent, "text": line.strip(), "seq": False, "raw": index})
    return tokens, raw_lines


def _strip_comment(line: str) -> str:
    in_single = in_double = False
    for position, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if position == 0 or line[position - 1] in (" ", "\t"):
                return line[:position]
    return line


def _parse_node(tokens, index, raw_lines, source):
    token = tokens[index]
    if token["seq"]:
        return _parse_seq(tokens, index, raw_lines, source)
    return _parse_map(tokens, index, token["indent"], raw_lines, source)


def _parse_seq(tokens, index, raw_lines, source):
    items = []
    indent = tokens[index]["indent"]
    while index < len(tokens) and tokens[index]["indent"] == indent and tokens[index]["seq"]:
        token = tokens[index]
        index += 1
        text = token["text"]
        if text == "":
            if index < len(tokens) and tokens[index]["indent"] > indent:
                value, index = _parse_node(tokens, index, raw_lines, source)
            else:
                value = None
        elif text in _BLOCK_INDICATORS:
            value, index = _parse_block_scalar(text, tokens, index, indent, raw_lines, token["raw"], source)
        elif _split_pair(text) is not None:
            value, index = _parse_map(
                tokens, index, indent, raw_lines, source, first_text=text, first_raw=token["raw"]
            )
        else:
            value = _parse_scalar(text, source)
        items.append(value)
    return items, index


def _parse_map(tokens, index, indent, raw_lines, source, first_text=None, first_raw=None):
    mapping = {}
    if first_text is not None:
        key, value, index = _parse_pair(first_text, tokens, index, indent, raw_lines, first_raw, source)
        _assign(mapping, key, value, source, first_raw)
    while index < len(tokens) and tokens[index]["indent"] == indent and not tokens[index]["seq"]:
        token = tokens[index]
        index += 1
        key, value, index = _parse_pair(token["text"], tokens, index, indent, raw_lines, token["raw"], source)
        _assign(mapping, key, value, source, token["raw"])
    return mapping, index


def _assign(mapping, key, value, source, raw_index):
    if key in mapping:
        raise YamlError("%s: line %d: duplicate key %r" % (source, raw_index + 1, key))
    mapping[key] = value


def _parse_pair(text, tokens, index, indent, raw_lines, raw_index, source):
    pair = _split_pair(text)
    if pair is None:
        raise YamlError("%s: line %d: expected 'key: value', got %r" % (source, raw_index + 1, text))
    key, rest = pair
    rest = rest.strip()
    if rest == "":
        if index < len(tokens) and tokens[index]["indent"] > indent:
            value, index = _parse_node(tokens, index, raw_lines, source)
        elif (
            index < len(tokens)
            and tokens[index]["indent"] == indent
            and tokens[index]["seq"]
        ):
            value, index = _parse_node(tokens, index, raw_lines, source)
        else:
            value = None
    elif rest in _BLOCK_INDICATORS:
        value, index = _parse_block_scalar(rest, tokens, index, indent, raw_lines, raw_index, source)
    else:
        value = _parse_scalar(rest, source)
    return _unquote_key(key), value, index


def _parse_block_scalar(indicator, tokens, index, key_indent, raw_lines, raw_index, source):
    folded = indicator.startswith(">")
    lines = []
    cursor = raw_index + 1
    content_indent = None
    consumed = raw_index
    while cursor < len(raw_lines):
        line = raw_lines[cursor]
        if line.strip() == "":
            lines.append("")
            cursor += 1
            continue
        indentation = len(line) - len(line.lstrip(" "))
        if indentation <= key_indent:
            break
        if content_indent is None:
            content_indent = indentation
        lines.append(line[content_indent:] if len(line) >= content_indent else line.strip())
        consumed = cursor
        cursor += 1
    while lines and lines[-1] == "":
        lines.pop()
    text = " ".join(part for part in lines if part != "") if folded else "\n".join(lines)
    while index < len(tokens) and tokens[index]["raw"] <= consumed:
        index += 1
    return text, index


def _split_pair(text: str):
    """Split 'key: value' at the first top-level colon. Returns (key, rest) or None."""
    in_single = in_double = False
    for position, char in enumerate(text):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == ":" and not in_single and not in_double:
            following = text[position + 1 : position + 2]
            if following in ("", " ", "\t"):
                return text[:position], text[position + 1 :]
    return None


def _unquote_key(key: str) -> str:
    key = key.strip()
    if len(key) >= 2 and key[0] == key[-1] and key[0] in ("'", '"'):
        return _unquote(key)
    return key


def _parse_scalar(text: str, source: str = "<string>"):
    text = text.strip()
    if text == "":
        return None
    if text[0] in "[{":
        return _FlowParser(text, source).parse()
    if text[0] in ("'", '"'):
        return _unquote(text)
    lowered = text.lower()
    if lowered in ("null", "~"):
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    integer = re.match(r"^[+-]?\d+$", text)
    if integer:
        return int(text)
    number = re.match(r"^[+-]?\d+\.\d+([eE][+-]?\d+)?$", text)
    if number:
        return float(text)
    return text


def _unquote(text: str) -> str:
    text = text.strip()
    if len(text) < 2 or text[0] != text[-1] or text[0] not in ("'", '"'):
        raise YamlError("unterminated quoted scalar: %r" % text)
    body = text[1:-1]
    if text[0] == "'":
        return body.replace("''", "'")
    return (
        body.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace('\\"', '"')
        .replace("\\\\", "\\")
    )


class _FlowParser:
    """Recursive-descent parser for inline lists/maps (the `[a, b]` / `{k: v}` style)."""

    def __init__(self, text: str, source: str = "<string>"):
        self.text = text
        self.position = 0
        self.source = source

    def parse(self):
        value = self._value()
        self._skip_space()
        if self.position != len(self.text):
            raise YamlError("%s: trailing characters in flow value: %r" % (self.source, self.text))
        return value

    def _peek(self):
        return self.text[self.position] if self.position < len(self.text) else ""

    def _skip_space(self):
        while self.position < len(self.text) and self.text[self.position] in " \t":
            self.position += 1

    def _value(self):
        self._skip_space()
        char = self._peek()
        if char == "[":
            return self._list()
        if char == "{":
            return self._map()
        if char in ('"', "'"):
            return self._quoted()
        return _parse_scalar(self._raw_until(",]}\n"), self.source)

    def _quoted(self):
        quote = self._peek()
        start = self.position
        self.position += 1
        while self.position < len(self.text):
            char = self.text[self.position]
            if char == "\\" and quote == '"':
                self.position += 2
                continue
            if char == quote:
                self.position += 1
                return _unquote(self.text[start : self.position])
            self.position += 1
        raise YamlError("%s: unterminated quoted string in flow value" % self.source)

    def _raw_until(self, stop_chars):
        start = self.position
        while self.position < len(self.text) and self.text[self.position] not in stop_chars:
            self.position += 1
        return self.text[start : self.position].strip()

    def _list(self):
        self.position += 1  # '['
        items = []
        while True:
            self._skip_space()
            if self._peek() == "]":
                self.position += 1
                return items
            if self._peek() == "":
                raise YamlError("%s: unterminated inline list" % self.source)
            items.append(self._value())
            self._skip_space()
            if self._peek() == ",":
                self.position += 1
                continue
            if self._peek() == "]":
                self.position += 1
                return items
            raise YamlError("%s: expected ',' or ']' in inline list" % self.source)

    def _map(self):
        self.position += 1  # '{'
        mapping = {}
        while True:
            self._skip_space()
            if self._peek() == "}":
                self.position += 1
                return mapping
            if self._peek() == "":
                raise YamlError("%s: unterminated inline map" % self.source)
            key = self._raw_until(":,")
            self._skip_space()
            if self._peek() != ":":
                raise YamlError("%s: expected ':' in inline map" % self.source)
            self.position += 1
            mapping[_unquote_key(key)] = self._value()
            self._skip_space()
            if self._peek() == ",":
                self.position += 1
                continue
            if self._peek() == "}":
                self.position += 1
                return mapping
            raise YamlError("%s: expected ',' or '}' in inline map" % self.source)


# --------------------------------------------------------------------------------------
# Dumping (emits the same subset; strings are always double-quoted for safety)
# --------------------------------------------------------------------------------------
def dumps(data, indent: int = 0) -> str:
    """Serialise to YAML within the supported subset."""
    lines = []
    _dump_node(data, indent, lines)
    return "\n".join(lines) + "\n"


def dump_file(path: str, data) -> None:
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(dumps(data))


def _dump_node(node, indent: int, lines):
    pad = " " * indent
    if isinstance(node, dict):
        if not node:
            lines.append(pad + "{}")
            return
        for key, value in node.items():
            _dump_pair(str(key), value, indent, lines)
    elif isinstance(node, (list, tuple)):
        if not node:
            lines.append(pad + "[]")
            return
        for item in node:
            _dump_item(item, indent, lines)
    else:
        lines.append(pad + _format_scalar(node))


def _dump_pair(key: str, value, indent: int, lines):
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            lines.append("%s%s: {}" % (pad, key))
        else:
            lines.append("%s%s:" % (pad, key))
            _dump_node(value, indent + 2, lines)
    elif isinstance(value, (list, tuple)):
        if not value:
            lines.append("%s%s: []" % (pad, key))
        else:
            lines.append("%s%s:" % (pad, key))
            _dump_node(value, indent + 2, lines)
    else:
        lines.append("%s%s: %s" % (pad, key, _format_scalar(value)))


def _dump_item(item, indent: int, lines):
    pad = " " * indent
    if isinstance(item, dict):
        if not item:
            lines.append(pad + "- {}")
            return
        keys = list(item.keys())
        first = keys[0]
        head, rest = item[first], {key: item[key] for key in keys[1:]}
        if isinstance(head, (dict, list, tuple)) and head:
            lines.append("%s- %s:" % (pad, first))
            _dump_node(head, indent + 4, lines)
        elif isinstance(head, (dict, list, tuple)):
            lines.append("%s- %s: %s" % (pad, first, "{}" if isinstance(head, dict) else "[]"))
        else:
            lines.append("%s- %s: %s" % (pad, first, _format_scalar(head)))
        if rest:
            _dump_node(rest, indent + 2, lines)
    elif isinstance(item, (list, tuple)):
        lines.append(pad + "-")
        _dump_node(item, indent + 2, lines)
    else:
        lines.append("%s- %s" % (pad, _format_scalar(item)))


def _format_scalar(value) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return repr(value)
    text = str(value)
    if "\n" in text:
        body = "\n".join("  " + line if line else "" for line in text.split("\n"))
        return "|-\n" + body
    escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
    return '"%s"' % escaped
