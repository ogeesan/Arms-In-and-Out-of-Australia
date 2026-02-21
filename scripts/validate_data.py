"""Validate data that has been extracted/transcribed"""

import typer
import yaml

from ausarms.data import IO, DataPaths
from ausarms.schemas import dec as schema

app = typer.Typer()


@app.command()
def dec():
    path = DataPaths.dec

    filelist = [x for x in path.joinpath("transcribed").glob("*.yml")]
    for filepath in filelist:
        try:
            schema.FinancialYear.model_validate(IO.load_yaml(filepath))
        except Exception as e:
            print(f"\nError validating {filepath.name}: {e}")


@app.command()
def other():
    pass


if __name__ == "__main__":
    app()
