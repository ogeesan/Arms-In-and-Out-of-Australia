"""Download data script for ausarms-data package."""

from pathlib import Path

import typer
from tqdm import tqdm

from ausarms.data.decdata.source import (
    SOURCE_FOLDER,
    DECManifest,
    find_heading_locations,
    load_manifest,
)
from ausarms.data.source.IO import bulk_download

app = typer.Typer()


@app.command()
def validate_dec_data():
    """
    Validate the downloaded Defence Export Controls data files.
    """
    # TODO: validate other files too?
    filepaths = list(SOURCE_FOLDER.glob("*q*.pdf"))

    def validate_document(filepath: Path):
        heading_locations = find_heading_locations(filepath)
        all_found = all([v for k, v in heading_locations.items() if v is not None])
        if not all_found:
            missing_headings = [k for k, v in heading_locations.items() if v is None]
            raise ValueError(
                f"Document validation failed for {filepath.name}. Missing headings: {missing_headings}"
            )

    failures = []
    for filepath in tqdm(filepaths, desc="Validating DEC data files..."):
        try:
            validate_document(filepath)
        except ValueError as e:
            failures.append(str(e))
    if failures:
        for failure in failures:
            print(failure)
        raise ValueError("Document validation failed for one or more files.")
    print("All Defence Export Controls data files validated successfully.")


@app.command()
def download_dec_data(overwrite: bool = False):
    """Download Defence Export Controls data files."""
    manifest: DECManifest = load_manifest()
    SOURCE_FOLDER.mkdir(parents=True, exist_ok=True)

    # Build the list of urls and filepaths
    download_list = []
    for source_doc in manifest.source_documents:
        if source_doc.url:
            # Single URL for the whole year (older files)
            dest_path = SOURCE_FOLDER.joinpath(f"{source_doc.financial_year}.pdf")
            download_list.append((source_doc.url, dest_path))
        elif source_doc.urls:
            # Quarterly URLs (from FY 2024-2025 onwards)
            for quarter_attr in ["q1", "q2", "q3", "q4"]:
                quarter_url = getattr(source_doc.urls, quarter_attr)
                if quarter_url:
                    dest_path = SOURCE_FOLDER.joinpath(
                        f"{source_doc.financial_year}_{quarter_attr}.pdf"
                    )
                    download_list.append((quarter_url, dest_path))

    metadata = bulk_download(
        urls=[url for url, _ in download_list],
        destination_paths=[path for _, path in download_list],
        overwrite=overwrite,
    )

    # Write metadata to a JSON file
    metadata_path = SOURCE_FOLDER.joinpath("dec-download-metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write(metadata.model_dump_json(indent=2))

    print(f"Downloaded {len(download_list)} files. Metadata saved to {metadata_path}.")


if __name__ == "__main__":
    app()
