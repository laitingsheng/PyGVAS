from typing import Any


DIRECTIONS: dict[str, dict[str, float]] = {
    "PZN": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "w": 1.0,
    },
    "PZS": {
        "x": 0.0,
        "y": 0.0,
        "z": 1.0,
        "w": 0.0,
    },
}

TARGET_LOCATION = "Facility"

INTERCEPT_CONTAINERS: set[str] = {
    "deployed_container_filingcabinet_small_c",
    "deployed_container_filingcabinet_medium_c",
    "deployed_container_filingcabinet_large_c",
    "deployed_container_filingcabinet_huge_c",
    "deployed_container_magazine_stand_c",
    "deployed_container_medkit_c",
    "deployed_container_toolbox_c",
    "deployed_container_toolbox_plant_c",
    "deployed_container_trashcan_c",
    "deployed_container_trashcan_small_c",
    "deployed_container_parktrashbin_c",
    "deployed_container_chest_vintage_c",
    "deployed_storagecrate_makeshift_c",
    "deployed_storagecrate_makeshift_t2_c",
    "deployed_storagecrate_makeshift_t3_c",
    "deployed_storagecrate_makeshift_t4_c",
    "deployed_armor_stand_c",
    "deployed_armor_stand_woodf_c",
    "deployed_armor_stand_woodm_c",
    "deployed_crate_hgatekeeper_c",
    "deployed_crate_hmusicbox_c",
    "deployed_crate_hornate_c",
    "deployed_crate_hsecurity_c",
    "deployed_crate_hinquisitor_c",
    "deployed_watercooler_c",
}

TARGET_STORAGE: dict[str, Any] = {
    "blueprint": "/Game/Blueprints/DeployedObjects/Furniture/Deployed_StorageCrate_Makeshift_T4",
    "reference": "Deployed_StorageCrate_Makeshift_T4_C",
    "actor": "PersistentLevel.Deployed_StorageCrate_Makeshift_T4_C_2147470199",
    "size": 42,
    "paint": 13,
}

STORAGE_IGNORE_LABEL: set[str] = {
    "Marker",
    "Placeholder",
}

STORAGE_DISTRIBUTIONS: list[dict[str, Any]] = [
    {
        "start": {
            "x": -16385.0,
            "y": 10458.0,
            "z": 1111.0,
        },
        "direction": "PZS",
        "spacing": {
            "y": 100.0,
            "z": 79.0,
        },
        "labels": [
            ("", (0, 0, 0), (1, 7, 5)),
        ],
    },
    {
        "start": {
            "x": -16293.0,
            "y": 10184.0,
            "z": 1211.0,
        },
        "direction": "PZN",
        "spacing": {
            "y": 100.0,
            "z": 79.0,
        },
        "labels": [
            # ("", (0, 0, 0), (1, 1, 7)),
            # ("", (0, 1, 0), (1, 2, 8)),
        ],
    },
    {
        "start": {
            "x": -16385.0,
            "y": 10776.0,
            "z": 1571.0,
        },
        "direction": "PZS",
        "spacing": {
            "y": 100.0,
            "z": 79.0,
        },
        "labels": [
            ("", (0, 0, 0), (1, 4, 4)),
        ],
    },
    {
        "start": {
            "x": -16697.0,
            "y": 10760.0,
            "z": 991.0,
        },
        "direction": "PZN",
        "spacing": {
            "z": 79.0,
        },
        "labels": [
            ("", (0, 0, 0), (1, 1, 4)),
        ],
    },
    {
        "start": {
            "x": -16765.0,
            "y": 10760.0,
            "z": 991.0,
        },
        "direction": "PZS",
        "spacing": {
            "z": 79.0,
        },
        "labels": [
            ("", (0, 0, 0), (1, 1, 4)),
        ],
    },
]
