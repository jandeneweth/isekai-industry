"""
Modify country definitions
"""

import re
import sys
import pathlib


def main():
    mod_dir = pathlib.Path(sys.argv[1])
    country_definitions_dir = mod_dir / "common" / "country_definitions"
    print(f"Updating country definitions in {str(country_definitions_dir)}")

    for countryfile in country_definitions_dir.iterdir():
        if str(countryfile).startswith('.'):
            continue
        with open(countryfile, "r", encoding="utf-8") as fh:
            lines = [_replace_line(line) for line in fh]
        full_text = "".join(lines)
        with open(countryfile, "w", encoding="utf-8") as fh:
            fh.write(full_text)

RE_COUNTRY_RECOGNIZED = re.compile("country_type = recognized")

def _replace_line(line: str) -> str:
    if "country_type = recognized" in line:
        return RE_COUNTRY_RECOGNIZED.sub("country_type = unrecognized", line)
    return line


if __name__ == "__main__":
    main()
