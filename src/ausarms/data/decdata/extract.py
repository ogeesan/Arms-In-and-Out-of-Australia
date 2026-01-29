"""Extraction of data from PDF files"""

from collections import defaultdict
from pathlib import Path
from typing import Any, Protocol

import pandas as pd
import pdfplumber
from pdfplumber.pdf import PDF

import ausarms.data.decdata.source as decsource


# Create a parsing error type
class DECParsingError(Exception):
    """Custom error for parsing Defence Export Controls documents."""

    pass


def find_heading_locations(
    filepath_or_pdf: Path | PDF,
) -> dict[str, list[int]]:
    """
    Find location(s) of tables in the document.
    All tables except "end user destinations - by territory" should only appear once.
    """
    if isinstance(filepath_or_pdf, Path):
        pdf = pdfplumber.open(filepath_or_pdf)
    else:
        assert isinstance(filepath_or_pdf, PDF)
        pdf = filepath_or_pdf

    manifest = decsource.load_manifest()
    heading_check = defaultdict(list)
    for index, page in enumerate(pdf.pages):
        text = page.extract_text_simple()

        if "table of contents" in text.lower():
            continue

        if "key information and caveats" in text.lower():
            continue

        for item in manifest.structure:
            # Handle special cases
            # end user destinations - by territory
            if item.special and "country check" in item.special:
                if "DSGL Part 1" in text:
                    heading_check[item.name].append(index)
                continue

            # All other headings
            if any(
                [
                    possible_name.lower() in text.lower()
                    for possible_name in item.aliases
                ]
            ):
                heading_check[item.name].append(index)
    # convert to regular dict
    heading_check = dict(heading_check)  # type: ignore

    # Validate that non-multipage headings only appear once
    for item in manifest.structure:
        if (
            item.special
            and "optional" in item.special
            and item.name not in heading_check
        ):
            continue

        if (
            not (item.special and "multipage" in item.special)
            and len(heading_check[item.name]) > 1
        ):
            raise DECParsingError(
                f"Multiple occurrences of heading '{item.name}' found in document ({heading_check[item.name]})."
            )

    # use only uniques and sort
    for heading in heading_check:
        heading_check[heading] = list(set(heading_check[heading]))
        heading_check[heading].sort()

    return heading_check


class ExtractorFunction(Protocol):
    def __call__(self, pdf: PDF, page_indices: list[int]) -> list[Any]: ...


def extract_dsgl_territories(pdf: PDF, page_indices: list[int]) -> list[pd.DataFrame]:
    """
    Extract territory/country tables.
    """
    output_tables = []
    for page_index in page_indices:
        page = pdf.pages[page_index]

        # assume it's the same table multiple times on each page
        page_tables = page.find_tables()
        page_table = []
        for t in page_tables:
            table = t.extract()
            if all([cell == "" for cell in table[0]]):
                continue
            assert table[0][0] in ["Country / Territory", "Destination"]
            assert table[0][1] == "DSGL Part 1"
            assert table[0][2] == "DSGL Part 2"
            assert len(table[0]) == 3
            df = pd.DataFrame(table[1:], columns=table[0])
            page_table.append(df)
        output_tables.append(pd.concat(page_table))
    return output_tables


def extract_dsgl_parts_table(
    pdf: PDF, page_indices: list[int]
) -> list[dict[str, int | str]]:
    """
    Extract the DSGL parts table from the given PDF pages.
    """
    tables = []
    for index in page_indices:
        page = pdf.pages[index]
        text = page.extract_text_simple()

        # TODO: find out if I can just do Quarter/FY check across the regions table too
        if "Issued permits – Quarter " in text:
            dsgl_type = "quarter"
        elif "Issued permits – FY" in text:
            dsgl_type = "year"
        else:
            raise DECParsingError("Cannot determine DSGL type on pages.")
        text = text.split("\n")
        data: dict[str, int | str] = {"dsgl_type": dsgl_type}
        for entry_name in [
            "Defence and Strategic Goods List – Part 1 ",
            "Defence and Strategic Goods List – Part 2",
        ]:
            for line in text:
                if entry_name in line:
                    value_str = line.split(entry_name)[-1].strip()
                    value_str = value_str.replace(",", "")
                    data[entry_name] = int(value_str)
                    break
        tables.append(data)
    return tables


heading_function_mapping: dict[str, ExtractorFunction] = {
    "end-user-destinations-territory": extract_dsgl_territories,
    "dsgl-parts": extract_dsgl_parts_table,
}


def get_function(heading: str) -> ExtractorFunction:
    if heading not in heading_function_mapping:
        raise ValueError(f"No extraction function defined for heading '{heading}'")
    return heading_function_mapping[heading]
