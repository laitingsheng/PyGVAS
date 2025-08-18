import sys
from pathlib import Path

from ._saves import ABFCommonSave, ABFPlayerSave, ABFWorldSave


entry, filename = sys.argv
filepath = Path(filename).absolute()
filename = filepath.name
if filename.startswith("Player_"):
    save_class = ABFPlayerSave
elif filename.startswith("WorldSave_"):
    save_class = ABFWorldSave
else:
    save_class = ABFCommonSave
exporting = {".sav": True, ".json": False}[filepath.suffix]
if exporting:
    save_class.from_binary_file(filepath).to_json_file(filepath.with_suffix(".json"))
else:
    save_class.from_json_file(filepath).to_binary_file(filepath.with_suffix(".sav.new"))
