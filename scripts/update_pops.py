"""
Modify pops
"""

import re
import sys
import pathlib

# Multiply population size by this number
#  I found that a reduction to 30% makes numbers roughly correspond
#  from the Vic3 1836 start date to the ~1450 EU4 one.
POPULATION_FACTOR = 0.30
# Modify population in some counties that are (almost comically)
#  over or undersized for this time period
STATE_FACTOR_MAP: dict[str, float] = {
    # England - way too large, prob due to Vic3 start effects of early industrialization?
    "STATE_HOME_COUNTIES": 0.4,
    "STATE_WEST_COUNTRY": 0.4,
    "STATE_EAST_ANGLIA": 0.33,
    "STATE_MIDLANDS": 0.33,
    "STATE_LANCASHIRE": 0.33,
    "STATE_YORKSHIRE": 0.33,
    "STATE_WALES": 0.5,
    # France
    "STATE_NORMANDY": 0.4,
    "STATE_ILE_DE_FRANCE": 0.5,
    # Hungary - should be half of what is is (2M)
    "STATE_TRANSDANUBIA": 0.5,
    "STATE_WEST_SLOVAKIA": 0.5,
    "STATE_EAST_SLOVAKIA": 0.5,
    "STATE_CENTRAL_HUNGARY": 0.5,
    "STATE_BEKES": 0.5,
    "STATE_NORTHERN_TRANSYLVANIA": 0.5,
    "STATE_SOUTHERN_TRANSYLVANIA": 0.5,
    "STATE_BANAT": 0.5,
    "STATE_DELVIDEK": 0.5,
    # Egypt - should be more than double what it is (4M)
    "STATE_LOWER_EGYPT": 1.5,
    "STATE_MIDDLE_EGYPT": 3.0,
    "STATE_UPPER_EGYPT": 3.0,
    # China - should be ~80M (now 100M); best to spend some effort here since the lead is already huge
    #  Japan and Korea, while also relatively large, are roughly correct.
    "STATE_BEIJING": 0.8,
    "STATE_SHENGJING": 0.8,
    "STATE_SHANDONG": 0.8,
    "STATE_ZHILI": 0.8,  # Hebei
    "STATE_SHANXI": 0.8,
    "STATE_NINGXIA": 0.8,
    "STATE_GANSU": 0.8,
    "STATE_XIAN": 0.8,
    "STATE_HENAN": 0.8,
    "STATE_NORTHERN_ANHUI": 0.8,
    "STATE_SOUTHERN_ANHUI": 0.8,
    "STATE_JIANGSU": 0.8,
    "STATE_NANJING": 0.8,
    "STATE_SUZHOU": 0.8,
    "STATE_ZHEJIANG": 0.8,
    "STATE_JIANGXI": 0.8,
    "STATE_FUJIAN": 0.8,
    "STATE_SHAOZHOU": 0.8,
    "STATE_GUANGDONG": 0.8,
    "STATE_GUANGXI": 0.8,
    "STATE_YUNNAN": 0.8,
    "STATE_GUIZHOU": 0.8,
    "STATE_HUNAN": 0.8,
    "STATE_EASTERN_HUBEI": 0.8,
    "STATE_WESTERN_HUBEI": 0.8,
    "STATE_CHONGQING": 0.8,
    "STATE_SICHUAN": 0.8,
}


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

RE_STATE = re.compile(r"s:([a-zA-Z0-9_]*?) = \{")
RE_POP_SIZE = re.compile(r"size = ([0-9]+)")

def _replace_line(line: str) -> str:
    if line.lstrip().startswith('s:'):
        _replace_line.last_state = RE_STATE.search(line).group(1)
    if "size =" in line:
        if match := RE_POP_SIZE.search(line):
            new_number = int(
                int(match.group(1))
                * POPULATION_FACTOR
                * STATE_FACTOR_MAP.get(_replace_line.last_state, 1.0)
            )
            return RE_POP_SIZE.sub(f"size = {new_number}", line)
    return line

_replace_line.last_state = None

if __name__ == "__main__":
    main()
