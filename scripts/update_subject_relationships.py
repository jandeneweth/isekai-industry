"""
Modify subject relationships
"""

import re
import sys
import pathlib


def main():
    mod_dir = pathlib.Path(sys.argv[1])
    subject_relationships_fp = mod_dir / "common" / "history" / "diplomacy" / "00_subject_relationships.txt"
    print(f"Updating subject relationships at {str(subject_relationships_fp)}")

    with open(subject_relationships_fp, "r", encoding="utf-8") as fh:
        lines = [_replace_line(line) for line in fh]
    full_text = "".join(lines)
    with open(subject_relationships_fp, "w", encoding="utf-8") as fh:
        fh.write(full_text)

RE_COUNTRY_RECOGNITION = re.compile("type = puppet")

def _replace_line(line: str) -> str:
    if "type = puppet" in line:
        return RE_COUNTRY_RECOGNITION.sub("type = vassal", line)
    return line


if __name__ == "__main__":
    main()
