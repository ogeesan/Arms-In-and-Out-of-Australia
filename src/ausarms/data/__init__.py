from typing import NamedTuple

from .decdata.source import DATA_ROOT as dec_root


class DataPaths(NamedTuple):
    dec = dec_root
