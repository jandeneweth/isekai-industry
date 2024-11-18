"""
Modify building histories
"""

import re
import sys
import pathlib


def main():
    mod_dir = pathlib.Path(sys.argv[1])
    building_histories_dir = mod_dir / "common" / "history" / "buildings"
    print(f"Updating building histories in {str(building_histories_dir)}")

    for buildingsfile in building_histories_dir.iterdir():
        if str(buildingsfile).startswith('.'):
            continue
        with open(buildingsfile, "r", encoding="utf-8") as fh:
            lines = [_replace_line(line) for line in fh]
        full_text = "".join(lines)
        full_text = _replace_full_text(full_text)
        with open(buildingsfile, "w", encoding="utf-8") as fh:
            fh.write(full_text)

RE_PRODUCTION_METHOD_PORT = re.compile(r'activate_production_methods = \{ "(pm_basic_port)" \}')

def _replace_line(line: str) -> str:
    if "activate_production_methods = " in line:
        return RE_PRODUCTION_METHOD_PORT.sub('activate_production_methods = { "pm_anchorage" }', line)
    return line

RE_GOVERNMENT_ADMINISTRATION = re.compile(
    (
        r'create_building = \{\s*?building = "building_government_administration"'
        r'.*?activate_production_methods = \{ "[a-zA-Z_]*?" \}\s*?\}'
    ), 
    flags=re.DOTALL
)

def _replace_full_text(text: str) -> str:
    text = RE_GOVERNMENT_ADMINISTRATION.sub("", text)
    return text

if __name__ == "__main__":
    main()
