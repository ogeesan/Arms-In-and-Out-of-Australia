"""Retrieve Defence Export Controls data from the Australian Government"""

from typing import List, Optional

import pdfplumber
import yaml
from pdfplumber.pdf import PDF
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from ausarms.data.source import IO

DATA_ROOT = IO.DATA_DIR.joinpath("defence-export-controls")
MANIFEST_PATH = DATA_ROOT.joinpath("dec-manifest.yml")
SOURCE_FOLDER = DATA_ROOT.joinpath("source")


class QuarterlyUrls(BaseModel):
    q1: Optional[HttpUrl] = Field(None)
    q2: Optional[HttpUrl] = Field(None)
    q3: Optional[HttpUrl] = Field(None)
    q4: Optional[HttpUrl] = Field(None)


class SourceDocument(BaseModel):
    financial_year: str = Field(..., alias="financial year")
    # url could be direct url for a whole year or urls for each quarter
    url: Optional[HttpUrl] = Field(None)
    urls: Optional[QuarterlyUrls] = Field(None)


class StructureItem(BaseModel):
    name: str
    aliases: List[str]
    special: Optional[list[str]] = None


class DECManifest(BaseModel):
    source_documents: List[SourceDocument] = Field(..., alias="source-documents")
    structure: List[StructureItem]

    model_config = ConfigDict(
        populate_by_name=True,
    )


def load_manifest() -> DECManifest:
    """Load the manifest file for Defence Export Controls data source."""
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return DECManifest.model_validate(yaml.safe_load(f))


def load_file(filename: str) -> PDF:
    """Load a DEC PDF file from the source folder."""
    filepath = SOURCE_FOLDER.joinpath(filename)
    return pdfplumber.open(filepath)
