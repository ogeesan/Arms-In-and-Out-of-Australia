from seaborn import xkcd_palette
palette_dict = {'australia': (0.0, 0.0, 0.545)}

class PaletteHandler:
    palette: dict[str, tuple[float, float, float]] = palette_dict
    
    def get_rgb(self, target) -> tuple[float, float, float]:
        return self.palette[target]

palette = PaletteHandler()

def rgb(target: str) -> tuple[float, float, float]:
    return palette.get_rgb(target.lower())

def xkcd(name: str) -> tuple[float, float, float]:
    """Find RGB value for a colour using xkcd.

    Parameters
    ----------
    name : str
        Name of colour.

    Returns
    -------
    tuple[float, float, float]
        The colour in RGB format.
    """
    return xkcd_palette([name])[0]