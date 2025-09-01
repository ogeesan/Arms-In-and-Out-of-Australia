
palette_dict = {'australia': (0.0, 0.0, 0.545)}

class PaletteHandler:
    palette: dict[str, tuple[float, float, float]] = palette_dict
    
    def get_rgb(self, target) -> tuple[float, float, float]:
        return self.palette[target]

palette = PaletteHandler()

def rgb(target: str) -> tuple[float, float, float]:
    return palette.get_rgb(target.lower())