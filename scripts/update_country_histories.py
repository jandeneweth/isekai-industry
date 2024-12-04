"""
Modify country history
"""

import re
import sys
import pathlib


def main():
    mod_dir = pathlib.Path(sys.argv[1])
    country_history_dir = mod_dir / "common" / "history" / "countries"
    print(f"Updating country histories in {str(country_history_dir)}")

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
    # Production
    "sericulture",
    "enclosure",
    # Military
    "navigation",
    "standing_army",
    # Society
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
    # Power structure
    (re.compile("law_type:law_parliamentary_republic"), "law_type:law_presidential_republic"),
    (re.compile("law_type:law_council_republic"), "law_type:law_presidential_republic"),

    (re.compile("law_type:law_landed_voting"), "law_type:law_oligarchy"),
    (re.compile("law_type:law_wealth_voting"), "law_type:law_oligarchy"),
    (re.compile("law_type:law_census_voting"), "law_type:law_oligarchy"),
    (re.compile("law_type:law_universal_suffrage"), "law_type:law_oligarchy"),
    (re.compile("law_type:law_anarchy"), "law_type:law_oligarchy"),
    (re.compile("law_type:law_single_party_state"), "law_type:law_oligarchy"),

    (re.compile("law_type:law_freedom_of_conscience"), "law_type:law_state_religion"),
    (re.compile("law_type:law_total_separation"), "law_type:law_state_religion"),
    (re.compile("law_type:law_state_atheism"), "law_type:law_state_religion"),

    (re.compile("law_type:law_national_militia"), "law_type:law_peasant_levies"),
    (re.compile("law_type:law_mass_conscription"), "law_type:law_peasant_levies"),
    (re.compile("law_type:law_professional_army"), "law_type:law_peasant_levies"),

    (re.compile("law_type:law_national_guard"), "law_type:law_no_home_affairs"),
    (re.compile("law_type:law_secret_police"), "law_type:law_no_home_affairs"),
    (re.compile("law_type:law_guaranteed_liberties"), "law_type:law_no_home_affairs"),

    # Economy

    (re.compile("law_type:law_interventionism"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_agrarianism"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_industry_banned"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_laissez_faire"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_cooperative_ownership"), "law_type:law_traditionalism"),
    (re.compile("law_type:law_command_economy"), "law_type:law_traditionalism"),

    (re.compile("law_type:law_mercantilism"), "law_type:law_city_tolls"),
    (re.compile("law_type:law_protectionism"), "law_type:law_city_tolls"),
    (re.compile("law_type:law_free_trade"), "law_type:law_city_tolls"),
    (re.compile("law_type:law_isolationism"), "law_type:law_city_tolls"),

    (re.compile("law_type:law_per_capita_based_taxation"), "law_type:law_consumption_based_taxation"),
    (re.compile("law_type:law_proportional_taxation"), "law_type:law_land_based_taxation"),
    (re.compile("law_type:law_graduated_taxation"), "law_type:law_land_based_taxation"),
    
    (re.compile("law_type:law_commercialized_agriculture"), "law_type:law_tenant_farmers"),
    (re.compile("law_type:law_homesteading"), "law_type:law_tenant_farmers"),
    (re.compile("law_type:law_collectivized_agriculture"), "law_type:law_tenant_farmers"),

    (re.compile("law_type:law_local_police"), "law_type:law_no_police"),
    (re.compile("law_type:law_dedicated_police"), "law_type:law_no_police"),
    (re.compile("law_type:law_militarized_police"), "law_type:law_no_police"),

    (re.compile("law_type:law_religious_schools"), "law_type:law_no_schools"),
    (re.compile("law_type:law_private_schools"), "law_type:law_no_schools"),
    (re.compile("law_type:law_public_schools"), "law_type:law_no_schools"),

    # Human Rights

    (re.compile("law_type:law_outlowed_dissent"), "law_type:law_right_of_assembly"),
    (re.compile("law_type:law_censorship"), "law_type:law_right_of_assembly"),
    (re.compile("law_type:law_protected_speech"), "law_type:law_right_of_assembly"),
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
