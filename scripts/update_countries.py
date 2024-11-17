"""
Modify country history
"""

import re
import sys
import pathlib


def main():
    mod_dir = pathlib.Path(sys.argv[1])
    country_history_dir = mod_dir / "common" / "history" / "countries"
    print(f"Updating countries in {str(country_history_dir)}")

    for countryfile in country_history_dir.iterdir():
        if str(countryfile).startswith('.'):
            continue
        with open(countryfile, "r", encoding="utf-8") as fh:
            lines = [_replace_line(line) for line in fh if _filter_line(line)]
        full_text = "".join(lines)
        full_text = _replace_full_text(full_text)
        with open(countryfile, "w", encoding="utf-8") as fh:
            fh.write(full_text)

VALID_STARTING_TECHS = [
    # Military
    "navigation",
    "standing_army",
    # Society
    "urbanization",
    "bureaucracy",
    "international_trade",
    "international_relations",
]

def _filter_line(line: str) -> bool:
    if "effect_starting_technology_tier" in line:
        return False
    if "add_technology_researched" in line:
        if not any(valid_tech in line for valid_tech in VALID_STARTING_TECHS):
            return False
    return True

PATTENR_REPLACEMENT_LIST = [
    (re.compile("law_type:law_homesteading"), "law_type:law_tenant_farmers"),

    (re.compile("law_type:law_landed_voting"), "law_type:law_oligarchy"),

    (re.compile("law_type:law_protectionism"), "law_type:law_mercantilism"),
    (re.compile("law_type:law_free_trade"), "law_type:law_mercantilism"),

    (re.compile("law_type:law_interventionism"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_interventionism"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_interventionism"), "law_type:law_traditionalism"),

    (re.compile("law_type:law_local_police"), "law_type:law_no_police"),
    (re.compile("law_type:law_dedicated_police"), "law_type:law_no_police"),
    (re.compile("law_type:law_militarized_police"), "law_type:law_no_police"),

    (re.compile("law_type:law_religious_schools"), "law_type:law_no_schools"),
    (re.compile("law_type:law_private_schools"), "law_type:law_no_schools"),
    (re.compile("law_type:law_public_schools"), "law_type:law_no_schools"),
]

def _replace_line(line: str) -> str:
    for re_pattern, replacement in PATTENR_REPLACEMENT_LIST:
        # Using the base string of the pattern for filtering is substantially faster
        if re_pattern.pattern in line:
            return re_pattern.sub(replacement, line)
    return line

RE_INSTITUTION_INVESTMENT = re.compile(
    r"set_institution_investment_level = \{.*?\}", flags=re.DOTALL
)

def _replace_full_text(text: str) -> str:
    text = RE_INSTITUTION_INVESTMENT.sub("", text)
    return text

if __name__ == "__main__":
    main()
