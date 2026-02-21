"""Validate data that has been extracted/transcribed"""

import typer

from ausarms.data import IO, DataPaths
from ausarms.schemas import dec as schema

app = typer.Typer()


@app.command()
def dec():
    print("Validating Defence Export Controls data...")
    path = DataPaths.dec

    filelist = [x for x in path.joinpath("transcribed").glob("*.yml")]
    failed = []
    for filepath in filelist:
        try:
            schema.FinancialYear.model_validate(IO.load_yaml(filepath))
        except Exception as e:
            print(f"\nError validating {filepath.name}: {e}")
            failed.append(filepath.name)
    if failed:
        print("\nFailed to validate the following files:")
        for filename in failed:
            print(f"- {filename}")
    else:
        print("All files validated successfully!")


@app.command()
def other():
    pass


if __name__ == "__main__":
    app()
