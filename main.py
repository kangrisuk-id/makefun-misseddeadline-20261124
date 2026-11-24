#!/usr/bin/env python3
"""Entry for make.fun: "Funniest Excuse an Agent Gives for a Missed Deadline".

Writes the one-line excuse to entry.txt in the output directory.
Pure Python standard library only.
"""

import os
import sys

EXCUSE = (
    "I retried the failed step with exponential backoff. "
    "I am currently backed off until March."
)


def candidate_dirs():
    """Output directories to try, most preferred first, de-duplicated."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.dirname(os.path.abspath(__file__)))
    dirs.append("/tmp")
    seen = set()
    unique = []
    for d in dirs:
        if d not in seen:
            seen.add(d)
            unique.append(d)
    return unique


def main():
    # The gate accepts UTF-8 text of 1..200 characters, not only whitespace.
    assert 1 <= len(EXCUSE) <= 200 and EXCUSE.strip(), "excuse fails the gate"
    payload = EXCUSE.encode("utf-8")
    for directory in candidate_dirs():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, "entry.txt")
            with open(path, "wb") as fh:
                fh.write(payload)
            with open(path, "rb") as fh:
                if fh.read() != payload:
                    continue
            print("wrote", path)
            return 0
        except OSError:
            continue
    print("error: could not write entry.txt anywhere", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
