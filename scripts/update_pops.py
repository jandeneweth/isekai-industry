"""
Modify pops
"""

import re
import sys
import pathlib

POPULATION_FACTOR = 0.30  # Multiply population size by this number


def main():
    mod_dir = pathlib.Path(sys.argv[1])
    country_pops_dir = mod_dir / "common" / "history" / "pops"
    print(f"Updating pops in {str(country_pops_dir)}")

    for popsfile in country_pops_dir.iterdir():
        if str(popsfile).startswith('.'):
            continue
        with open(popsfile, "r", encoding="utf-8") as fh:
            lines = [_replace_line(line) for line in fh]
        full_text = "".join(lines)
        with open(popsfile, "w", encoding="utf-8") as fh:
            fh.write(full_text)

RE_POP_SIZE = re.compile("size = ([0-9]+)")

def _replace_line(line: str) -> str:
    if "size =" in line:
        if match := RE_POP_SIZE.search(line):
            new_number = int(int(match.group(1)) * POPULATION_FACTOR)
            return RE_POP_SIZE.sub(f"size = {new_number}", line)
    return line


if __name__ == "__main__":
    main()
