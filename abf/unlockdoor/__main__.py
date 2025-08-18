import os
import sys
from pathlib import Path

from .._saves import ABFWorldSave


entry, profile, name = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

for save_file in save_folder.glob("WorldSave_*.sav"):
    save = ABFWorldSave.from_binary_file(save_file)
    doormap = save.body.get("SimpleDoorMap")
    if doormap is None:
        continue
    for key, value in doormap["value"]["values"]:
        value["DoorState_16_FC20B6E3483FF18E4FBDF19E39E880E9"]["value"] = "NewEnumerator0"
        value["DoorRotationRootYaw_17_FEB24A4F4081A0EFDC1475AB811846D1"]["value"] = 0.0
        value["OneWayDoor_HasBeenUnlocked_9_128506D0489955F65729EEA611C542AC"]["value"] = True
    save.to_binary_file(output_folder / save_file.name)
