from . import palette, plot

__all__ = ["palette", "plot"]


def use_project_style() -> None:
    from pathlib import Path
    from matplotlib import rc_file

    filepath = Path(__path__[0]).joinpath("ausarms.mplstyle")
    rc_file(filepath)
