import itertools
from typing import Any

from .._items import create_empty_item, create_global_item
from .._utils import create_asset_id


ALL_FISHES: tuple[str, ...] = (
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
)

ALL_KILL_TARGETS: tuple[str, ...] = (
    "ElectroPest",
    "Exor",
    "ExorMonk",
    "GKChieftain",
    "GKHeavy",
    "GKMage",
    "GKWitch",
    "Tarasque",
    "Peccary",
    "Pest",
    "Pest_Volatile",
)

ALL_MAPS: tuple[str, ...] = (
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
)

ALL_POSITIVE_TRAITS: tuple[str, ...] = (
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
)

ALL_SOUP_RECIPES: tuple[str, ...] = (
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
)

DEFAULT_EQUIPMENT: dict[str, dict[str, Any]] = {
    "headlamp": {
        "name": "headlamp_nvg_t2",
        "liquid": 8,
    },
    "keypad": {
        "name": "gatekey",
    },
}

EQUIPMENT_KEYS: dict[str, int] = {
    "chest": 0,
    "helmet": 1,
    "legs": 2,
    "backpack": 3,
    "arms": 4,
    "suit": 5,
    "headlamp": 6,
    "trinket1": 7,
    "watch": 8,
    "keypad": 9,
    "offhand": 10,
    "trinket2": 11,
}

EQUIPMENT_PRESETS: dict[int, dict[str, dict[str, Any]]] = {
    1: {
        "helmet": {
            "name": "armor_helmet_mage",
        },
        "chest": {
            "name": "armor_chest_mage",
        },
        "arms": {
            "name": "armor_arms_mage",
        },
        "legs": {
            "name": "armor_legs_mage",
        },
        "suit": {
            "name": "suit_powerc",
        },
        "backpack": {
            "name": "backpack_longjumppack",
            "liquid": 8,
        },
        "offhand": {
            "name": "offhand_mageglove",
            "liquid": 15,
        },
        "trinket1": {
            "name": "trinket_gravitycube",
        },
        "trinket2": {
            "name": "trinket_light_purple",
        },
    },
}

HOTBAR_PRESETS: dict[int, dict[int, dict[str, Any]]] = {
    1: {
        0: {
            "name": "smg_military_u2",
            "ammo": -1,
        },
        1: {
            "name": "rocketlauncher",
            "ammo": 3,
        },
        2: {
            "name": "megalight_t2",
            "liquid": 8,
        },
        3: {
            "name": "heavy_laser",
            "liquid": 15,
        },
        4: {
            "name": "magnum_military_u1",
            "ammo": -1,
        },
        5: {
            "name": "vacuum_u2",
            "liquid": 8,
        },
        6: {
            "name": "flamethrower",
            "liquid": 15,
        },
        7: {
            "name": "knife_super",
        },
        8: {
            "name": "nullgrenade",
            "stack": 40,
        },
        9: {
            "name": "constructiongauntlet",
        },
    },
}

INVENTORY_PRESETS: dict[int, dict[int, dict[str, Any]]] = {
    1: {
        3: {
            "name": "backpack_jetpack",
            "liquid": 8,
        },
        4: {
            "name": "backpack_voidpack_u1b",
        },
        5: {
            "name": "backpack_dimension",
        },
        9: {
            "name": "bandage_t2",
            "stack": 40,
        },
        10: {
            "name": "syringe",
            "stack": 80,
        },
        11: {
            "name": "iodinetablets",
            "stack": 80,
        },
    },
}

JOB_MAPPING: dict[str, str] = {
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

JOB_PRESETS: dict[int, str] = {
    1: "Defense Analyst",
}

PREUNLOCKED_RECIPES: tuple[str, ...] = (
    "recipe_taxidermy_electropest",
    "recipe_taxidermy_pest",
    "recipe_taxidermy_volatilepest",
    "recipe_wallmount_exor",
    "recipe_wallmount_exormonk",
    "recipe_wallmount_peccary",
    "recipe_wallmount_tarasque",
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
