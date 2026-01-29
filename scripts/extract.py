"""Extract from pdf files"""

import pandas as pd
import typer

from ausarms.data import decdata

app = typer.Typer()


@app.command()
def dec(
    file: str = typer.Argument(..., help="Name of DEC PDF file"),
    heading: str = typer.Argument(..., help="Name of heading to extract"),
    print_terminal: bool = typer.Option(True, help="Print output to terminal"),
):
    pdf = decdata.source.load_file(file)
    heading_locations = decdata.extract.find_heading_locations(pdf)
    extraction_func = decdata.extract.get_function(heading)
    output = extraction_func(pdf, heading_locations[heading])
    if extraction_func == decdata.extract.extract_dsgl_territories:
        df = pd.concat(output)
        if print_terminal:
            for row in df.itertuples(index=False):
                print(f"{row[0]}: [{row[1]}, {row[2]}]")
    else:
        raise NotImplementedError("Output function not supported")


@app.command()
def att():
    raise NotImplementedError("ATT extraction not yet implemented")


def main():
    app()


if __name__ == "__main__":
    main()
