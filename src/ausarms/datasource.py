"""Prepare data obtained from SIPRI and ASPI for SQL database insertion."""

from pathlib import Path

import pandas as pd

rawdatafolder = Path("data/raw")


def load_sipri_traderegister(io: str) -> pd.DataFrame:
    """Load SIPRI trade register data for Australia, either incoming or outgoing."""
    if io not in ["incoming", "outgoing"]:
        raise ValueError("Invalid IO type. Must be 'incoming' or 'outgoing'.")
    filename = f"SIPRI-trade-register-AUS-{io}.csv"
    data = pd.read_csv(rawdatafolder.joinpath(filename), skiprows=11, encoding="latin")
    # fix "iinfantry fighting vehicle turrent" typo in description
    data['Weapon description'] = data['Weapon description'].str.replace("iinfantry fighting vehicle turret", "infantry fighting vehicle turret")
    return data

def load_aspi_cod_table() -> pd.DataFrame:
    """Load ASPI's Cost of Defence - Defence Exports table."""
    filename = "ASPI CoD - Defence Exports - Dec2022.xlsx - Sheet1.csv"
    data = pd.read_csv(rawdatafolder.joinpath(filename))

    # Convert value column into numbers
    value_column = "Value (AUDm)"
    tf = data[value_column].isin(["-", "Tied into the Protector-class contract"])
    data.loc[tf, value_column] = None
    data[value_column] = data[value_column].str.replace(",", "").astype(float)
    
    data['Current or prior ADF-use'] = data['Current or prior ADF-use'] == 'Y'
    data['Donation'] = data['Donation'] == 'Y'
    return data


MILEX_FILENAME = "SIPRI-Milex-data-1949-2024.xlsx"
measures_and_sheets = {
    "current_usd": "Current US$",
    "share_of_gov_spending": "Share of Govt. spending",
    "share_of_gdp": "Share of GDP",
    "per_capita": "Per capita",
}
measure_types = list(measures_and_sheets.keys())


def load_military_expenditure_data(measure_type: str) -> pd.DataFrame:
    """Load SIPRI's military expenditure data"""
    sheet_name = measures_and_sheets[measure_type]
    df = load_milex_sheet(sheet_name)
    df = remove_preheader_rows(df, "Country")

    # exclude all rows that have empty values for 2000 (are sub-headers)
    df = df[df[2000].notna()]
    df.drop(columns=["Notes"], inplace=True)
    if "Reporting Year" in df.columns:
        df.drop(columns=["Reporting Year"], inplace=True)

    df.reset_index(drop=True, inplace=True)
    # TODO: some sheets have 0.0 values even though other sheets show there is no data for that early (e.g. Australia 1949)
    return df


def load_milex_sheet(sheet_name: str) -> pd.DataFrame:
    """Load raw sheet from SIPRI's military expenditure data"""
    return pd.read_excel(rawdatafolder / MILEX_FILENAME, sheet_name=sheet_name)


def remove_preheader_rows(df: pd.DataFrame, header_str: str) -> pd.DataFrame:
    """Remove rows before the real header row in SIPRI military expenditure data."""
    n_skip = df.index[df.iloc[:, 0] == header_str][0]
    column_names = df.iloc[
        n_skip
    ].to_list()  # list here to prevent setting index with Series name
    df.columns = column_names
    return df.iloc[n_skip + 1 :]


# Countries missing from SIPRI's global milex dataset
missing_countries = [
    {"Country": "Solomon Islands", "Continent": "Asia & Oceania", "Region": "Oceania"},
    {"Country": "Tonga", "Continent": "Asia & Oceania", "Region": "Oceania"},
    {"Country": "Vanuatu", "Continent": "Asia & Oceania", "Region": "Oceania"},
]


def build_country_table() -> pd.DataFrame:
    """Build a table of countries with continent and region information using SIPRI military expenditure data."""
    continents = set(["Africa", "Americas", "Asia & Oceania", "Europe", "Middle East"])
    measure_tables = {}
    for measure in measure_types:
        df = load_milex_sheet(measures_and_sheets[measure])
        df = remove_preheader_rows(df, "Country")

        region_values = set(df.loc[df[2000].isna(), "Country"])
        subregions = region_values.difference(continents)
        measure_tables[measure] = _build_country_identities(df, continents, subregions)

    # Verify all of the measure_tables have the same data
    merged_table = pd.concat(measure_tables.values(), keys=measure_tables.keys())
    n_countries = merged_table["Country"].nunique()
    merged_table.drop_duplicates(inplace=True)
    if merged_table["Country"].nunique() != n_countries:
        raise ValueError("Inconsistent country data found")

    merged_table = pd.concat(
        [merged_table, pd.DataFrame(missing_countries)], ignore_index=True
    )

    merged_table.sort_values(["Continent", "Region", "Country"], inplace=True)

    return merged_table.reset_index(drop=True)


def _build_country_identities(
    data: pd.DataFrame, continents: set, subregions: set
) -> pd.DataFrame:
    """Build a table of countries with continent and region information."""
    current_continent = None
    current_region = None
    country_data = []
    for row in data["Country"]:
        if row in continents:
            current_continent = row
            continue
        if row in subregions:
            current_region = row
            continue
        country_data.append(
            {"Country": row, "Continent": current_continent, "Region": current_region}
        )
    return pd.DataFrame(country_data)


def normalise_country_name(original: str) -> str:
    """Convert SIPRI names to standardised names."""
    if original == "Korea, North":
        return "North Korea"
    if original == "Korea, South":
        return "South Korea"
    if original == "United States":
        return "United States of America"
    if original == "UAE":
        return "United Arab Emirates"
    if original == "Timor Leste":
        return "Timor-Leste"
    return original
