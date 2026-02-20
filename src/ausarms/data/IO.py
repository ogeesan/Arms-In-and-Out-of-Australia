"""Core IO functions for sourcedata package."""

import hashlib
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

import tqdm
import yaml
from pydantic import BaseModel, Field, HttpUrl

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


class MetaDataEntry(BaseModel):
    filename: str = Field(description="Name of the file as stored in the repository.")
    url: str = Field(description="URL of the file.")
    downloaded_at: datetime = Field(description="When the file was retrieved.")
    sha256sum: str = Field(description="SHA256 checksum of the downloaded file.")


class MetaData(BaseModel):
    downloads: list[MetaDataEntry] = Field(
        description="List of downloaded files and their metadata."
    )


def compute_file_hash(destination_path: Path) -> str:
    """Compute the SHA256 hash of a file."""
    with open(destination_path, "rb") as f:
        file_data = f.read()
        return hashlib.sha256(file_data).hexdigest()


def download_file(url: str, destination_path: Path, overwrite=True) -> MetaDataEntry:
    """
    Download a file from a URL to a destination path, and generate metadata including md5sum.
    """
    if destination_path.exists() and not overwrite:
        raise FileExistsError(f"File {destination_path} already exists.")
    urlretrieve(url, destination_path)
    return MetaDataEntry(
        filename=destination_path.name,
        url=url,
        downloaded_at=datetime.now(),
        sha256sum=compute_file_hash(destination_path),
    )


def bulk_download(
    urls: list[HttpUrl], destination_paths: list[Path], overwrite=True
) -> MetaData:
    """
    Download multiple files from a list of URLs to a destination folder, generating metadata.
    """
    metadata_entries = []
    for url, destination_path in tqdm.tqdm(
        zip(urls, destination_paths), total=len(urls), desc="Downloading files"
    ):
        metadata_entry = download_file(
            url=str(url), destination_path=destination_path, overwrite=overwrite
        )
        metadata_entries.append(metadata_entry)
    return MetaData(downloads=metadata_entries)


class SafeLineLoader(yaml.SafeLoader):
    """YAML loader that inserts line number into the extracted data"""

    # augurar's Stack Overflow answer
    # https://stackoverflow.com/a/53647080
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping["__line__"] = node.start_mark.line + 1
        return mapping


def load_yaml(filepath: Path, with_line_numbers: bool = False):
    with open(filepath) as f:
        if with_line_numbers:
            loaded = yaml.load_all(f, Loader=SafeLineLoader)
        else:
            loaded = yaml.load_all(f, Loader=yaml.SafeLoader)
        docs = [x for x in loaded]
    assert len(docs) == 1
    return docs[0]


def load_multipage_yaml(filepath: Path, with_line_numbers: bool = False) -> list:
    """Loads .yml data with multiple pages."""
    data = []
    with open(filepath) as f:
        if with_line_numbers:
            stream = yaml.load_all(f, Loader=SafeLineLoader)
        else:
            stream = yaml.load_all(f, Loader=yaml.SafeLoader)
        for document in stream:
            data.append(document)
    return data
