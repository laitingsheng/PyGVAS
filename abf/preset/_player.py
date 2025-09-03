import itertools
from typing import Any

from .._items import create_empty_item, create_global_item
from .._utils import create_asset_id
from ._constants import (
    ALL_FISHES,
    ALL_KILL_TARGETS,
    ALL_MAPS,
    ALL_POSITIVE_TRAITS,
    ALL_SOUP_RECIPES,
    DEFAULT_EQUIPMENT,
    EQUIPMENT_KEYS,
    EQUIPMENT_PRESETS,
    HOTBAR_PRESETS,
    INVENTORY_PRESETS,
    JOB_MAPPING,
    JOB_PRESETS,
    PREUNLOCKED_RECIPES,
)


def improve_player(index: int, player: dict[str, dict[str, Any]]) -> None:
    items = player["EquipmentInventory_11_78EC662B493ED43BF306CD8FD82EA45A"]["value"]["values"]
    items.extend(create_empty_item() for _ in range(len(EQUIPMENT_KEYS) - len(items)))
    for key, item in (EQUIPMENT_PRESETS.get(index, {}) | DEFAULT_EQUIPMENT).items():
        items[EQUIPMENT_KEYS[key]] = create_global_item(create_asset_id(), **item)

    items = player["HotbarInventory_12_EB0E545B44BB772E1CCFCEBF8F0170A1"]["value"]["values"]
    items.extend(create_empty_item() for _ in range(10 - len(items)))
    for key, item in HOTBAR_PRESETS.get(index, {}).items():
        items[key] = create_global_item(create_asset_id(), **item)

    items = player["Inventory_8_758B207A48BE5E12B0022C91938F32BD"]["value"]["values"]
    locked = player["FavoritedSlots_125_BD14BA2A40F37FA19BC7C6816BCC3F3C"]["value"]["values"]
    for key, item in INVENTORY_PRESETS.get(index, {}).items():
        items[key] = create_global_item(create_asset_id(), **item)
        locked[key] = True

    player["Traits_15_0039F2B34D2A43327122E9960B328E55"]["value"]["values"] = list(ALL_POSITIVE_TRAITS)

    job = JOB_PRESETS.get(index)
    if job is not None:
        player["PhD_42_91C6570A451A177090EE25AF113045D2"]["value"] = JOB_MAPPING[job]

    for skill in player["Skills_22_3287F93C42DD32FCD04E9E8295C6EDC3"]["value"]["values"]:
        skill["CurrentSkillXP_20_8F7934CD4A4542F036AE5C9649362556"]["value"] = 1e6
        skill["CurrentXPMultiplier_15_9DA8B8A24B4F5B134743CDBE828520F0"]["value"] = 1.0

    recipes = dict.fromkeys(player["RecipesUnlock_41_C6D066A3416620A76188D2A39E4D8DF9"]["value"]["values"])
    recipes.update((recipe, None) for recipe in itertools.chain(ALL_SOUP_RECIPES, PREUNLOCKED_RECIPES))
    player["RecipesUnlock_41_C6D066A3416620A76188D2A39E4D8DF9"]["value"]["values"] = list(recipes.keys())

    player["CurrentMoney_85_7425E5BF43364C11279E4C8C26F5A7CA"] = {
        "type": {
            "type": "IntProperty",
        },
        "value": 1000000,
    }

    player["MapsUnlocked_93_E9A91D554F338AD17C73E7A6EC41EB87"] = {
        "type": {
            "type": "ArrayProperty",
        },
        "value": {
            "type": {
                "type": "NameProperty",
            },
            "values": list(ALL_MAPS),
        },
    }

    player["Compendium_Fish_130_F3328DBD41952E919E4BF48486764935"] = {
        "type": {
            "type": "ArrayProperty",
        },
        "value": {
            "type": {
                "type": "NameProperty",
            },
            "values": list(ALL_FISHES),
        },
    }

    player["Compendium_Kill_134_68DA7D3440838FFFA0A3E996BC33C549"] = {
        "type": {
            "type": "ArrayProperty",
        },
        "value": {
            "type": {
                "type": "NameProperty",
            },
            "values": list(ALL_KILL_TARGETS),
        },
    }
    player["Compendium_KillCount_137_580C4765460383FB00B3A0B49694B010"] = {
        "type": {
            "type": "ArrayProperty",
        },
        "value": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/AbioticFactor",
                "name": "CompendiumKillCount",
            },
            "values": [
                {
                    "CompendiumRow": {
                        "type": {
                            "type": "StructProperty",
                            "blueprint": "/Script/AbioticFactor",
                            "name": "CompendiumEntryRowHandle",
                        },
                        "value": {
                            "RowName": {
                                "type": {
                                    "type": "NameProperty",
                                },
                                "value": target,
                            },
                        },
                    },
                    "Count": {
                        "type": {
                            "type": "IntProperty",
                        },
                        "value": 10000,
                    },
                }
                for target in ALL_KILL_TARGETS
            ],
        },
    }

    player["CharacterHealth_51_C8B0855046256D908ECD3FAC9FD050C0"]["value"] = {
        "Head_2_9DF5F0D3418FEA87915307B0916F71F1": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "Torso_9_C71E40B64A3CFA07EB7D569FDF7E27FA": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "LeftArm_10_DBC1F7CB470045555A9179BC1E18BFC3": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "RightArm_11_19F1E62945ADCC1BFD286F9A266F4101": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "LeftLeg_12_3FAFACB443CC3A390EFB3BA1BA33E54D": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "RightLeg_13_93AC33BD4A3F5CAF6132C6A8834E2D9B": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
    }
    player["CurrentSurvivalStats_61_828D08B64E0E5CCA5B7C968C1EFA0E07"]["value"] = {
        "Hunger_2_A6C5CC6E41993323B119FA9E0B3894CA": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "Thirst_7_E620D3DA44520EAC8EBFA28ECD77E6DA": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "Sanity_8_1EA1DBDE4CEA799B882ABBB9EF766161": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 1e6,
        },
        "Fatigue_9_D4A267F046B9CD6F07518AAF88356DBE": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0,
        },
        "Continence_11_29DC4A474C89E8B517691D8C627AA2F9": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0,
        },
        "Radiation_16_CBCAFEC549FC3D10D8D4418FD3D5FB77": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0,
        },
    }

    player["NewestRecipes_141_C7277E904ACCEB6C26F1FB967CADCAFA"] = {
        "type": {
            "type": "ArrayProperty",
        },
        "value": {
            "type": {
                "type": "NameProperty",
            },
            "values": [],
        },
    }
