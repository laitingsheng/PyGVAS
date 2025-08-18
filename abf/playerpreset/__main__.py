import itertools
import os
import re
import sys
from pathlib import Path
from typing import Any
from uuid import UUID

from .._saves import ABFPlayerSave
from .._utils import create_asset_id, create_empty_item, create_global_item, extract_item_asset_id
from ._presets import DEFAULT_EQUIPMENT, EQUIPMENT_PRESETS, HOTBAR_PRESETS, INVENTORY_PRESETS, JOB_PRESETS


__all__ = []

_JOB_MAPPING = {
    "Lab Assistant": "NoPhD",
    "Epimedical Bionomicist": "PhD_Medicine",
    "Trans-Kinematic Researcher": "PhD_HumanBio",
    "Archotechnic Consultant": "PhD_MechEng",
    "Phytogenetic Botanist": "PhD_Agriculture",
    "Somatic Gastrologist": "PhD_NutritonalSci",
    "Paratheoretical Physicist": "PhD_TheoreticalPhys",
    "Defense Analyst": "PhD_DefenseSecurity",
    "Summer Intern": "Intern",
}

entry, profile, name, *players = sys.argv

save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name / "PlayerData"

output_folder = Path("output") / profile / name / "PlayerData"
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

player_save_regex = re.compile(r"Player_([A-Za-z0-9]+)\.sav")

asset_ids: set[UUID] = set()

for index, player in enumerate(players):
    save = ABFPlayerSave.from_binary_file(save_folder / f"Player_{player}.sav")
    data = save.body["CharacterSaveData"]["value"]
    for item in itertools.chain(
        data["EquipmentInventory_11_78EC662B493ED43BF306CD8FD82EA45A"]["value"]["values"],
        data["HotbarInventory_12_EB0E545B44BB772E1CCFCEBF8F0170A1"]["value"]["values"],
    ):
        asset_id = extract_item_asset_id(item)
        if asset_id is not None:
            asset_ids.add(asset_id)
    equipments = EQUIPMENT_PRESETS[index] | DEFAULT_EQUIPMENT
    items: list[dict[str, dict[str, Any]]] = []
    for key in (
        "chest",
        "helmet",
        "legs",
        "backpack",
        "arms",
        "suit",
        "headlamp",
        "trinket1",
        None,
        "keypad",
        "offhand",
        "trinket2",
    ):
        if key is None:
            items.append(create_empty_item())
            continue
        asset_id = asset_ids.pop() if asset_ids else create_asset_id()
        items.append(create_global_item(asset_id, **equipments[key]))
    data["EquipmentInventory_11_78EC662B493ED43BF306CD8FD82EA45A"]["value"]["values"] = items
    items = []
    for item in HOTBAR_PRESETS[index]:
        asset_id = asset_ids.pop() if asset_ids else create_asset_id()
        items.append(create_global_item(asset_id, **item))
    data["HotbarInventory_12_EB0E545B44BB772E1CCFCEBF8F0170A1"]["value"]["values"] = items
    items = data["Inventory_8_758B207A48BE5E12B0022C91938F32BD"]["value"]["values"]
    locked = data["FavoritedSlots_125_BD14BA2A40F37FA19BC7C6816BCC3F3C"]["value"]["values"]
    for inventory_index, item in INVENTORY_PRESETS[index].items():
        asset_id = extract_item_asset_id(items[inventory_index])
        if asset_id is None:
            asset_id = asset_ids.pop() if asset_ids else create_asset_id()
        items[inventory_index] = create_global_item(asset_id, **item)
        locked[inventory_index] = True
    data["Traits_15_0039F2B34D2A43327122E9960B328E55"]["value"]["values"] = [
        "Trait_Decathlon",
        "Trait_WrinklyBrainmeat",
        "Trait_NightOwl",
        "Trait_Chef",
        "Trait_Inconspicuous",
        "Trait_FannyPack",
        "Trait_SteelBladder",
        "Trait_Strong",
        "Trait_ThickSkinned",
        "Trait_FirstAidCert",
        "Trait_Gardener",
        "Trait_LightEater",
        "Trait_LeadBelly",
        "Trait_Moist",
        "Trait_SelfDefense",
        "Trait_FormerGuard",
        "Trait_Outdoorsman",
        "Trait_Sundisk",
    ]
    data["PhD_42_91C6570A451A177090EE25AF113045D2"]["value"] = _JOB_MAPPING[JOB_PRESETS[index]]
    for skill in data["Skills_22_3287F93C42DD32FCD04E9E8295C6EDC3"]["value"]["values"]:
        skill["CurrentSkillXP_20_8F7934CD4A4542F036AE5C9649362556"]["value"] = 1e6
        skill["CurrentXPMultiplier_15_9DA8B8A24B4F5B134743CDBE828520F0"]["value"] = 1.0
    recipes = dict.fromkeys(data["RecipesUnlock_41_C6D066A3416620A76188D2A39E4D8DF9"]["value"]["values"])
    recipes.update(
        (srecipe, None)
        for srecipe in [
            "recipe_taxidermy_electropest",
            "recipe_taxidermy_pest",
            "recipe_taxidermy_volatilepest",
            "recipe_wallmount_exor",
            "recipe_wallmount_exormonk",
            "recipe_wallmount_peccary",
            "recipe_wallmount_tarasque",
            "srecipe_anteversegumbo",
            "srecipe_armandleg",
            "srecipe_balanced",
            "srecipe_carbdumplings",
            "srecipe_cheesewheel",
            "srecipe_creamycorn_raw",
            "srecipe_creamytomato",
            "srecipe_fishglue",
            "srecipe_fishstew",
            "srecipe_glacialgazpacho",
            "srecipe_glue",
            "srecipe_gooeymushroom_raw",
            "srecipe_greyebchowder",
            "srecipe_harmonyrice",
            "srecipe_hearty",
            "srecipe_inkyeggdrop",
            "srecipe_lunarbisque",
            "srecipe_mashedpotatoes",
            "srecipe_meatrio",
            "srecipe_meaty",
            "srecipe_pasta_homey",
            "srecipe_pea",
            "srecipe_peccarygoulash",
            "srecipe_peccmush",
            "srecipe_peccnoodles",
            "srecipe_pestgoulash",
            "srecipe_pestgoulash_test",
            "srecipe_poop",
            "srecipe_potatosausage",
            "srecipe_pumpkin",
            "srecipe_radchowder",
            "srecipe_ravioli_pumpkin_raw",
            "srecipe_reservoir_reserve",
            "srecipe_rice",
            "srecipe_risotto",
            "srecipe_silkyconsomme_raw",
            "srecipe_simpletomato",
            "srecipe_solder",
            "srecipe_solder_test",
            "srecipe_splitpea",
            "srecipe_sugarslop",
            "srecipe_supertomato",
            "srecipe_sustenance",
            "srecipe_sweetporridge",
            "srecipe_veggie",
            "srecipe_witchinghour_raw",
        ]
    )
    data["RecipesUnlock_41_C6D066A3416620A76188D2A39E4D8DF9"]["value"]["values"] = list(recipes.keys())
    data["CurrentMoney_85_7425E5BF43364C11279E4C8C26F5A7CA"] = {
        "type": {
            "type": "IntProperty",
        },
        "value": 1000000,
    }
    data["MapsUnlocked_93_E9A91D554F338AD17C73E7A6EC41EB87"] = {
        "type": {
            "type": "ArrayProperty",
        },
        "value": {
            "type": {
                "type": "NameProperty",
            },
            "values": [
                "Map_Containment",
                "Map_Dam",
                "Map_Lab",
                "Map_Labs",
                "Map_MF",
                "Map_Office1",
                "Map_Office2",
                "Map_Office3",
                "Map_Pens",
                "Map_Reactor",
                "Map_Reactors",
                "Map_Residence",
                "Map_ResidenceTerribleMap",
                "Map_Security",
            ],
        },
    }
    data["Compendium_Fish_130_F3328DBD41952E919E4BF48486764935"]["value"]["values"] = [
        "Antefish",
        "Antefish_rare1",
        "Portalfish",
        "Portalfish_rare1",
        "Portalfish_rare2",
        "Portalfish_rare_torii",
        "IS0098",
        "IS0098_rare1",
        "MoonFish",
        "MoonFish_rare1",
        "GemCrab",
        "GemCrab_rare1",
        "Fogfish",
        "Fogfish_rare1",
        "ReaperFish",
        "ReaperFish_rare1",
        "Eel",
        "Eel_rare1",
        "Eel_rare2",
        "Eel_rare3",
        "DarkwaterFish",
        "DarkwaterFish_rare1",
        "IceFish",
        "IceFish_rare1",
        "Radfish",
        "Radfish_rare1",
        "SilkFish",
        "SilkFish_rare1",
        "UmbraFish",
        "UmbraFish_rare1",
    ]
    data["CharacterHealth_51_C8B0855046256D908ECD3FAC9FD050C0"]["value"] = {
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
    data["CurrentSurvivalStats_61_828D08B64E0E5CCA5B7C968C1EFA0E07"]["value"] = {
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
    save.to_binary_file(output_folder / f"Player_{player}.sav")
