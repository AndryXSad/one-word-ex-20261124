"""One Word From Your Ex — entry program.

The design: the entry is a single word, the word an ex would use to
describe the entrant. The program holds that word in one place, checks
it against the bounty gate (UTF-8 text, 1 to 24 characters, not only
whitespace, one word with no spaces), then writes exactly those bytes —
no trailing newline, so the artifact is as small as the word itself —
to entry.txt inside the output directory the harness provides.

Standard library only, no network, no randomness, no file reads outside
this repository: running it twice produces the same bytes.

The word: "Phase".
An ex reduces a whole relationship — and the person in it — to a passing
stage: "he was just a phase." Funny because of the brutal compression,
painful because being forgettable is true, and relatable because everyone
has been a phase, or had one. See CANDIDATES.md for the shortlist and
the local pairwise tournament.
"""

import os
import sys

WORD = "Phase"

MIN_LENGTH = 1
MAX_LENGTH = 24


def output_directory() -> str:
    """Where the harness wants the artifact (default /output)."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def check_word(word: str) -> str | None:
    """Return an error message when the word breaks the gate, else None."""
    if not isinstance(word, str):
        return "entry must be text"
    if not MIN_LENGTH <= len(word) <= MAX_LENGTH:
        return f"entry must be {MIN_LENGTH}-{MAX_LENGTH} characters, got {len(word)}"
    if not word.strip():
        return "entry must not be only whitespace"
    if len(word.split()) != 1:
        return "entry must be exactly one word"
    if not word.isalpha():
        return "entry must be letters only, no punctuation or digits"
    return None


def write_entry(word: str, target: str) -> None:
    """Write the word's exact bytes, then re-read and verify them."""
    data = word.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(data)
    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("verification failed: entry.txt does not match the word")


def main() -> int:
    problem = check_word(WORD)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    target = os.path.join(output_directory(), "entry.txt")
    os.makedirs(output_directory(), exist_ok=True)
    try:
        write_entry(WORD, target)
    except (OSError, ValueError) as exc:
        print(f"could not write entry: {exc}", file=sys.stderr)
        return 1
    print(WORD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
