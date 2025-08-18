import os
import re
import sys
from pathlib import Path

from .._saves import ABFPlayerSave, ABFWorldSave
from ._door import unlock_door
from ._player import improve_player
from ._world import preprocess_objects, process_sockets, prune_connections, write_attributes


entry, profile, name = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name
player_save_folder = save_folder / "PlayerData"

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)
player_output_folder = output_folder / "PlayerData"
player_output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

save_regex = re.compile(r"Player_([A-Za-z0-9]+)\.sav")
players: list[str] = []
for index, save_file in enumerate(player_save_folder.glob("Player_*.sav")):
    matches = save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid player save file name {save_file.name}")

    save = ABFPlayerSave.from_binary_file(save_file)
    identifier = save.body["SaveIdentifier"]["value"]
    if identifier != matches[1]:
        raise ValueError(f"Player save file {save_file.name} identifier mismatched")

    improve_player(index, save.body["CharacterSaveData"]["value"])
    save.to_binary_file(player_output_folder / save_file.name)

    players.append(identifier)

save_regex = re.compile(r"WorldSave_(\w+)\.sav")
saves: dict[str, ABFWorldSave] = {}
updated_saves: dict[str, None] = {}
for save_file in save_folder.glob("WorldSave_*.sav"):
    matches = save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid save file name {save_file.name}")

    save = ABFWorldSave.from_binary_file(save_file)
    identifier = save.body["SaveIdentifier"]["value"]
    if identifier != matches[1]:
        raise ValueError(f"World save file {save_file.name} identifier mismatched")
    saves[identifier] = save

    if unlock_door(save.body):
        updated_saves[identifier] = None

    preprocess_objects(identifier, save.body)

for identifier, save in saves.items():
    if process_sockets(identifier, save.body):
        updated_saves[identifier] = None

updated_saves.update(prune_connections())

for identifier in updated_saves:
    save = saves[identifier]
    write_attributes(identifier, save.body)
    save.to_binary_file(output_folder / f"WorldSave_{identifier}.sav")
