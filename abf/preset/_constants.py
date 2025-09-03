from typing import Any


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
