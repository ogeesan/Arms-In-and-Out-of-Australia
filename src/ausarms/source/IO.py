"""Core IO functions for sourcedata package."""

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "source"

# TODO: checksums for downloaded data
# TODO: access date for downloaded data

def generate_metadata():
    pass
