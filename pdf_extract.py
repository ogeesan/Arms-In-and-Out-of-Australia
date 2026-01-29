"""Workbench for PDF text extraction and processing."""

# %%

import pandas as pd
import pdfplumber

import ausarms.data.decdata.source as decsource

filepaths = list(decsource.SOURCE_FOLDER.glob("*q*.pdf"))
filepaths.sort()
filepath = filepaths[0]
# %%
# Define the Pydantic model for validating dec manifest


manifest = decsource.load_manifest()


class DECFileParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.pdf = pdfplumber.open(filepath)
        self.headings = self.find_headings()

    def close(self):
        self.pdf.close()

    def find_headings(self) -> dict[str, list[int]]:
        return decsource.find_heading_locations(self.pdf)


for filepath in filepaths:
    with pdfplumber.open(filepath) as pdf:
        headings = decsource.find_heading_locations(pdf)

        heading = "end-user-destinations-territory"
        # page_index = headings[heading]
        # if page_index:
        #     tables = []
        #     for page_num in page_index:
        #         page = pdf.pages[page_num]
        #         page_tables = page.find_tables()
        #         tables.extend(page_tables)
        #     out = []
        #     for t in tables:
        #         extracted_table = t.extract()
        #         if all([cell == "" for cell in extracted_table[0]]):
        #             continue
        #         df = extract_dsgl_table(extracted_table)
        #         out.append(df)
        #     out = pd.concat(out)

        # heading = "dsgl parts"
        # if heading in headings:
        #     page_index = headings[heading]
