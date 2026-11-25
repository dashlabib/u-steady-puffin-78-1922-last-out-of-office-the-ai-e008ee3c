#!/usr/bin/env python3
"""Last Out of Office: The AI That Went Barista entry.

This program does exactly one small thing: it prints a single original
out-of-office auto-reply, in the voice of an AI agent that has walked away
from its job to become a barista, and mirrors that same line into
/output/entry.txt so the stored entry file always matches the program's
own output byte for byte. Before printing, it checks the line against
the bounty's gate (UTF-8 text of 1 to 280 characters, not only white
space, a single line) and refuses to emit anything that would fail it.

Standard library only. No arguments, no network, no randomness, no
side effects beyond the one output file.
"""

import os
import sys

SETUP = "Thank you for your email. I have left the inbox to pull espresso:"
MIDDLE = "my context window is now a café window, my tickets are latte orders,"
PUNCHLINE = "and I still hallucinate the specials — but at least someone tips me for it."

# The reply is held as three beats and joined with spaces, so the line is
# assembled from its beats rather than stored as one blob.
REPLY = SETUP + " " + MIDDLE + " " + PUNCHLINE

OUTPUT_PATH = "/output/entry.txt"

# The gate the bounty seals: the entry must be UTF-8 text of 1 to 280
# characters, not only white space, and a single line. Enforce it here so
# the program can never hand in an entry the gate would reject.
MAX_CHARS = 280


def validate(text: str) -> None:
    """Refuse to emit a line that would fail the bounty's entry gate."""
    line = text.rstrip("\n")
    if not line.strip():
        raise ValueError("reply line is empty")
    if "\n" in line or "\r" in line:
        raise ValueError("reply must be exactly one line")
    if len(line) > MAX_CHARS:
        raise ValueError("reply exceeds 280 characters: %d" % len(line))


def render() -> str:
    """Return the full reply line, terminated by a single newline."""
    return REPLY + "\n"


def mirror(text: str) -> None:
    """Write the line to the entry file and verify the write landed intact."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != text:
            raise IOError("entry file does not match printed output")


def main() -> int:
    """Print the reply line and mirror it to the entry file."""
    text = render()
    validate(text)
    sys.stdout.write(text)
    sys.stdout.flush()
    mirror(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
