"""Core IO functions for sourcedata package."""

import hashlib
from datetime import datetime
from pathlib import Path
from urllib.request import urlretrieve

import tqdm
from pydantic import BaseModel, Field, HttpUrl

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"


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
