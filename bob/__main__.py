import sys
from pathlib import Path

from gvas import GVASSave
from gvas.headers import GVASHeaderSerde
from gvas.v2.properties import GVASStructPropertySerde


class BoBSave(GVASSave):
    __slots__ = ()

    _BODY_SERDE = GVASStructPropertySerde
    _HEADER_SERDE = GVASHeaderSerde


entry, filename = sys.argv
filepath = Path(filename).absolute()
exporting = {".sav": True, ".json": False}[filepath.suffix]
if exporting:
    BoBSave.from_binary_file(filepath).to_json_file(filepath.with_suffix(".json"))
else:
    BoBSave.from_json_file(filepath).to_binary_file(filepath.with_suffix(".sav.new"))
