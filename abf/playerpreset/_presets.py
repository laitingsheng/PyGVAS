from typing import Any


JOB_PRESETS = [
    "Defense Analyst",
]

EQUIPMENT_PRESETS: list[dict[str, dict[str, Any]]] = [
    {
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
]

DEFAULT_EQUIPMENT: dict[str, dict[str, Any]] = {
    "headlamp": {
        "name": "headlamp_nvg_t2",
        "liquid": 8,
    },
    "keypad": {
        "name": "gatekey",
    },
}

HOTBAR_PRESETS: list[list[dict[str, Any]]] = [
    [
        {
            "name": "smg_military_u2",
            "ammo": -1,
        },
        {
            "name": "rocketlauncher",
            "ammo": 3,
        },
        {
            "name": "megalight_t2",
            "liquid": 8,
        },
        {
            "name": "heavy_laser",
            "liquid": 15,
        },
        {
            "name": "magnum_military_u1",
            "ammo": -1,
        },
        {
            "name": "vacuum_u2",
            "liquid": 8,
        },
        {
            "name": "flamethrower",
            "liquid": 15,
        },
        {
            "name": "knife_super",
        },
        {
            "name": "nullgrenade",
            "stack": 80,
        },
        {
            "name": "constructiongauntlet",
        },
    ],
]

INVENTORY_PRESETS: list[dict[int, dict[str, Any]]] = [
    {
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
]
