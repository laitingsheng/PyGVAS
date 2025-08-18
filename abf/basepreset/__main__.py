import copy
import os
import re
import sys
from pathlib import Path
from typing import Any

from .._saves import ABFWorldSave
from .._utils import (
    create_asset_id,
    create_empty_item,
    create_facility_object,
    create_object_inventory,
    extract_object_asset_id,
)
from ._presets import (
    DIRECTIONS,
    INTERCEPT_CONTAINERS,
    STORAGE_DISTRIBUTIONS,
    STORAGE_IGNORE_LABEL,
    TARGET_LOCATION,
    TARGET_STORAGE,
)


__all__ = []

transform_storages: dict[str, list[dict[str, dict[str, Any]]]] = {}
for storage_distribution in STORAGE_DISTRIBUTIONS:
    start = storage_distribution["start"]
    rotation = DIRECTIONS[storage_distribution["direction"]]
    spacing = storage_distribution["spacing"]
    for label, (sx, sy, sz), (cx, cy, cz) in storage_distribution["labels"]:
        dx = spacing.get("x", 0.0)
        dy = spacing.get("y", 0.0)
        dz = spacing.get("z", 0.0)
        transform_storages.setdefault(label, []).extend(
            {
                "rotation": copy.deepcopy(rotation),
                "translation": {
                    "x": start["x"] + (sx + ix) * dx,
                    "y": start["y"] + (sy + iy) * dy,
                    "z": start["z"] + (sz + iz) * dz,
                },
            }
            for ix in range(cx)
            for iy in range(cy)
            for iz in range(cz)
        )

entry, profile, name = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

world_save_regex = re.compile(r"WorldSave_(\w+)\.sav")

target_storages: dict[str, list[dict[str, dict[str, Any]]]] = {}
for save_file in save_folder.glob("WorldSave_*.sav"):
    matches = world_save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid save file name {save_file.name}")
    identifier = matches[1]
    if identifier == TARGET_LOCATION:
        continue
    updated = False
    save = ABFWorldSave.from_binary_file(save_file)
    deployed_object_map = save.body.get("DeployedObjectMap")
    if deployed_object_map is not None:
        deployed_objects: list[tuple[str, dict[str, dict[str, Any]]]] = []
        for asset_id, deployed_object in deployed_object_map["value"]["values"]:
            object_name = deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()
            if object_name not in INTERCEPT_CONTAINERS or extract_object_asset_id(deployed_object) is None:
                deployed_objects.append((asset_id, deployed_object))
                continue
            updated = True
            label = deployed_object["CustomTextDisplay_152_B59A50C74001B5D2234D9E9B0D7CAB7F"]["value"]
            if not label or label in STORAGE_IGNORE_LABEL:
                target_storages.setdefault("", []).append(deployed_object)
            else:
                transformations = transform_storages.get(label, [])
                label_storages = target_storages.setdefault(label, [])
                if len(transformations) > len(label_storages):
                    label_storages.append(deployed_object)
                else:
                    target_storages.setdefault("", []).append(deployed_object)
        if updated:
            deployed_object_map["value"]["values"] = deployed_objects
    if updated:
        save.to_binary_file(output_folder / f"WorldSave_{identifier}.sav")

target_save = ABFWorldSave.from_binary_file(save_folder / f"WorldSave_{TARGET_LOCATION}.sav")
deployed_object_map = target_save.body["DeployedObjectMap"]
deployed_objects: list[tuple[str, dict[str, dict[str, Any]]]] = []
for asset_id, deployed_object in deployed_object_map["value"]["values"]:
    object_name = deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()
    if object_name not in INTERCEPT_CONTAINERS or extract_object_asset_id(deployed_object) is None:
        deployed_objects.append((asset_id, deployed_object))
        continue
    label = deployed_object["CustomTextDisplay_152_B59A50C74001B5D2234D9E9B0D7CAB7F"]["value"]
    if not label or label in STORAGE_IGNORE_LABEL:
        target_storages.setdefault("", []).append(deployed_object)
    else:
        transformations = transform_storages.get(label, [])
        label_storages = target_storages.setdefault(label, [])
        if len(transformations) > len(label_storages):
            label_storages.append(deployed_object)
        else:
            target_storages.setdefault("", []).append(deployed_object)
unlabelled_storages = target_storages.pop("", [])
for label, transformations in transform_storages.items():
    label_storages = target_storages.pop(label, [])
    for transformation in transformations:
        if label_storages:
            label_storage = label_storages.pop()
            asset_id = extract_object_asset_id(label_storage)
            inventories = label_storage.pop("ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB")
        elif unlabelled_storages:
            label_storage = unlabelled_storages.pop()
            asset_id = extract_object_asset_id(label_storage)
            inventories = label_storage.pop("ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB")
        else:
            asset_id = None
            inventories = None
        if asset_id is None:
            asset_id = create_asset_id()
        deployed_object = create_facility_object(
            asset_id,
            TARGET_STORAGE["blueprint"],
            TARGET_STORAGE["reference"],
            TARGET_STORAGE["actor"],
            transformation["rotation"],
            transformation["translation"],
            0,
            TARGET_STORAGE["paint"],
        )
        object_inventory = create_object_inventory()
        slots = object_inventory["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"]
        if inventories is not None:
            slots.extend(
                slot
                for content in inventories["value"]["values"]
                for slot in content["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"]
                if slot["ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B"]["value"]["RowName"]["value"].lower()
                not in ("empty", "none", "")
            )
        slots.extend(create_empty_item() for _ in range(TARGET_STORAGE["size"] - len(slots)))
        deployed_object["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"] = [
            object_inventory,
        ]
        deployed_objects.append((asset_id.hex.upper(), deployed_object))
    if label_storages:
        raise ValueError(f"Unprocessed {label} storages remain.")
deployed_object_map["value"]["values"] = deployed_objects
if target_storages:
    raise ValueError("Unprocessed target storages remain.")
target_save.to_binary_file(output_folder / f"WorldSave_{TARGET_LOCATION}.sav")
