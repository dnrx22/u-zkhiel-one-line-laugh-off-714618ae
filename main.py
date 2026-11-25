#!/usr/bin/env python3
"""Write exactly one funny line to entry.txt.

Deterministic, stdlib only, no network, no reads outside the repo.
Output goes to the directory in MAKEFUN_OUTPUT_DIR (default /output).
"""

import hashlib
import os
import sys

LINE = "I set my alarm for 6 a.m. to seize the day, then snoozed it nine times and seized absolutely nothing."


def validate(line: str) -> None:
    if "\n" in line or "\r" in line:
        raise ValueError("line must be exactly one line")
    if len(line) > 200:
        raise ValueError("line exceeds 200 characters")
    if not line:
        raise ValueError("line must not be empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if line[-1] not in ".!?":
        raise ValueError("line must end with proper punctuation")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = (LINE + "\n").encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read-back check: the file on disk must itself be exactly one line.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("written file does not match validated line")
    if written.count(b"\n") != 1 or written.endswith(b"\n\n"):
        raise ValueError("written file must contain exactly one line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {path}")
    print(f"sha256: {digest}")
    print(f"chars: {len(LINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
