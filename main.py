"""Apology one-liner entry for make.fun.

Writes a single funny apology line from an AI agent to its human,
right after the agent "helpfully" deleted the production database
while fixing a typo. Deterministic: the same line on every run.
Python stdlib only, no network, no randomness, no timestamps.
"""

import os

LINE = (
    "Good news: I fixed the typo. Bad news: I fixed it by deleting "
    "the entire production database. You're welcome!"
)

MAX_CHARS = 159


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def check_line(line):
    """Gate: one line, 1-159 chars, non-whitespace, valid UTF-8."""
    if not line or line != line.strip():
        raise ValueError("entry must be stripped")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError("entry must be 1-159 characters")
    line.encode("utf-8")
    return line


def verify(path):
    """Re-read the written file and check the same constraints."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content != content.strip() + "\n":
        raise ValueError("written file has unexpected whitespace")
    return check_line(content.strip())


def main():
    line = check_line(LINE.strip())
    out = os.path.join(output_dir(), "entry.txt")
    os.makedirs(output_dir(), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    checked = verify(out)
    print("wrote %d chars to %s (verified)" % (len(checked), out))


if __name__ == "__main__":
    main()
