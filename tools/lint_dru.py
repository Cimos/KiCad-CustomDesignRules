#!/usr/bin/env python3
"""Lint KiCad custom design rule (.kicad_dru) files.

Catches the classes of mistakes that have actually slipped into this repo
before there was any automated check:

  * unbalanced parentheses / malformed s-expressions
  * a missing or wrong `(version 1)` header
  * a `(rule ...)` with no name or no `(constraint ...)`
  * duplicate rule names
  * rule names not prefixed with the fab name (e.g. "JLCPCB: ")
  * lowercase item-type literals in conditions (`'track'`, `'via'`, `'pad'`,
    `'text'`, `'graphic'`) — KiCad expects PascalCase (`'Track'`, `'Via'`,
    `'Pad'`, ...); the lowercase form parses fine but silently never matches.

No third-party dependencies; runs on any Python 3.8+.

Usage:
    python3 tools/lint_dru.py FILE [FILE ...]
    python3 tools/lint_dru.py            # lint every *.kicad_dru in the repo

Exit code is non-zero if any error is found.
"""

from __future__ import annotations

import glob
import os
import re
import sys

# Item-type literals that must be PascalCase in KiCad expressions. Maps the
# wrong (lowercase) spelling to the correct one for the error message.
BAD_TYPE_LITERALS = {
    "track": "Track",
    "via": "Via",
    "pad": "Pad",
    "text": "Text",
    "graphic": "Graphic",
    "zone": "Zone",
}

# Matches e.g.  A.Type == 'track'   or   B.Type=='via'
TYPE_LITERAL_RE = re.compile(r"\.Type\s*[=!]=\s*'([^']*)'")


class LintError(Exception):
    pass


def strip_comments(text: str) -> str:
    """Blank out `#` comments and the inside of "strings" so paren counting
    and structural checks aren't confused by them. Preserves newlines and
    overall length so line numbers stay accurate."""
    out = []
    in_string = False
    in_comment = False
    for ch in text:
        if ch == "\n":
            in_comment = False
            out.append(ch)
            continue
        if in_comment:
            out.append(" ")
            continue
        if in_string:
            out.append(ch)
            if ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            out.append(ch)
        elif ch == "#":
            in_comment = True
            out.append(" ")
        else:
            out.append(ch)
    return "".join(out)


def check_paren_balance(code: str, errors: list) -> bool:
    depth = 0
    line = 1
    for ch in code:
        if ch == "\n":
            line += 1
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                errors.append((line, "unbalanced ')' (closes with no matching '(')"))
                return False
    if depth != 0:
        errors.append((line, f"unbalanced parentheses ({depth} '(' left unclosed)"))
        return False
    return True


def iter_top_level_forms(code: str):
    """Yield (start_line, text) for each top-level parenthesised form."""
    depth = 0
    line = 1
    start_line = None
    buf = []
    for ch in code:
        if depth > 0:
            buf.append(ch)
        if ch == "(":
            if depth == 0:
                start_line = line
                buf = ["("]
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                yield start_line, "".join(buf)
        if ch == "\n":
            line += 1


def lint_file(path: str) -> list:
    """Return a list of (line, message) errors for one file."""
    errors: list = []
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()

    code = strip_comments(raw)

    if not check_paren_balance(code, errors):
        # Structure is broken; further checks would be noise.
        return errors

    forms = list(iter_top_level_forms(code))

    # 1. version header
    if not forms or not re.match(r"\(\s*version\s+1\s*\)", forms[0][1]):
        errors.append((1, "file must start with a `(version 1)` header"))

    # 2. fab prefix from filename, e.g. JLCPCB.kicad_dru -> "JLCPCB: "
    fab = os.path.basename(path).split(".")[0]

    seen_names: dict = {}
    for start_line, form in forms:
        if not re.match(r"\(\s*rule\b", form):
            continue

        name_match = re.match(r'\(\s*rule\s+"([^"]*)"', form)
        if not name_match:
            errors.append((start_line, "rule is missing a quoted name"))
            continue
        name = name_match.group(1)

        if not re.search(r"\(\s*constraint\b", form):
            errors.append((start_line, f'rule "{name}" has no (constraint ...)'))

        if name in seen_names:
            errors.append(
                (start_line, f'duplicate rule name "{name}" (first defined at line {seen_names[name]})')
            )
        else:
            seen_names[name] = start_line

        if not name.startswith(f"{fab}: "):
            errors.append(
                (start_line, f'rule "{name}" should be prefixed with "{fab}: "')
            )

    # 3. lowercase type literals (scanned on the raw text so line numbers and
    #    the surrounding condition are reported as the author wrote them).
    for i, raw_line in enumerate(raw.splitlines(), start=1):
        line_code = strip_comments(raw_line)
        for m in TYPE_LITERAL_RE.finditer(line_code):
            literal = m.group(1)
            if literal in BAD_TYPE_LITERALS:
                errors.append(
                    (
                        i,
                        f"lowercase type literal '{literal}' — KiCad expects "
                        f"'{BAD_TYPE_LITERALS[literal]}' (the lowercase form never matches)",
                    )
                )

    return errors


def main(argv: list) -> int:
    paths = argv[1:]
    if not paths:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        paths = sorted(glob.glob(os.path.join(root, "**", "*.kicad_dru"), recursive=True))

    if not paths:
        print("no .kicad_dru files found", file=sys.stderr)
        return 1

    total = 0
    for path in paths:
        errors = lint_file(path)
        if errors:
            total += len(errors)
            for line, msg in sorted(errors):
                print(f"{path}:{line}: {msg}")
        else:
            print(f"{path}: OK")

    if total:
        print(f"\n{total} problem(s) found", file=sys.stderr)
        return 1
    print("\nAll design rule files pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
