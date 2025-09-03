import itertools
import os
import re
import sys
from pathlib import Path

from .._saves import ABFPlayerSave, ABFWorldSave
from ._door import unlock_door
from ._player import improve_player
from ._world import (
    deploy_beds,
    deploy_farms,
    deploy_liquid_containers,
    preprocess_objects,
    process_sockets,
    prune_connections,
    write_attributes,
)


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

    if preprocess_objects(
        identifier,
        save.body,
        {
            "deployed_furniture_craftedbed_c",
            "deployed_furniture_craftedbed_t2_c",
            "deployed_furniture_craftedbed_t3_c",
            "deployed_liquidcontainer_barrel_c",
            "deployed_liquidcontainer_barrel_wood_c",
            "deployed_liquidcontainer_cauldron_tech_c",
            "deployed_watercooler_c",
            "deployed_waterfilter_c",
            "deployed_watertank_c",
            "gardenplot_large_c",
            "gardenplot_medium_c",
            "gardenplot_small_c",
            "gardenplot_smallround_c",
        },
    ):
        updated_saves[identifier] = None

for identifier, save in saves.items():
    if process_sockets(identifier, save.body):
        updated_saves[identifier] = None

identifier = "Facility"
deploy_beds(
    identifier,
    13,
    players,
    (
        (
            (-17545.0, 11110.0, 1571.0),
            (0.0, 140.0),
            "PZ0",
            {
                0: (0, 0),
                1: (0, 1),
            },
        ),
    ),
)
deploy_farms(
    identifier,
    13,
    (
        (
            (-16528.0, 11539.0, 1571.0),
            (-330.0, 0.0),
            "PZ270",
            {
                (0, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_Corn",
                                "Plant_Egg",
                                "Plant_Greyeb",
                                "Plant_Potato",
                            ),
                            2,
                        ),
                    ),
                ),
                (1, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_Pumpkin",
                                "Plant_Rice",
                                "Plant_SpaceLettuce",
                                "Plant_Super_Tomato",
                            ),
                            2,
                        ),
                    ),
                ),
                (2, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_Tomato",
                                "Plant_Wheat",
                                "Plant_GlowTulip",
                                "Plant_Nyxshade",
                            ),
                            2,
                        ),
                    ),
                ),
                (3, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_RopePlant",
                                "Plant_VinePlant",
                            ),
                            4,
                        ),
                    ),
                ),
            },
        ),
    ),
)
deploy_liquid_containers(
    identifier,
    13,
    (
        (
            (-15472.0, 9989.0, 1211.0),
            (-96.0, 78.0),
            "PZ180",
            (2, 5),
            tuple(
                itertools.chain(
                    itertools.repeat(11, 4),
                    itertools.repeat(16, 1),
                    itertools.repeat(1, 5),
                ),
            ),
        ),
        (
            (-18690.0, 10264.0, 1016.0),
            (0.0, 78.0),
            "PZ0",
            (1, 4),
            tuple(itertools.repeat(1, 4)),
        ),
        (
            (-18246.0, 9988.0, 1016.0),
            (-78.0, 0.0),
            "PZ90",
            (5, 1),
            tuple(itertools.chain(range(2, 5), itertools.repeat(1, 2))),
        ),
        (
            (-18246.0, 10186.0, 1016.0),
            (-78.0, 0.0),
            "PZ270",
            (3, 1),
            tuple(range(2, 5)),
        ),
    ),
)
updated_saves[identifier] = None

updated_saves.update(prune_connections())

for identifier in updated_saves:
    save = saves[identifier]
    write_attributes(identifier, save.body)
    save.to_binary_file(output_folder / f"WorldSave_{identifier}.sav")
