import os
import re
import struct
import sys
from pathlib import Path
from typing import Any

from gvas.v3.properties import GVASBlueprintStructPropertySerde

from .._headers import ABFWorldHeaderSerde


__all__ = []

entry, profile, name, *labels = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

world_save_regex = re.compile(r"WorldSave_(\w+)\.sav")
labels_regex = re.compile("|".join(map(re.escape, labels))) if len(labels) > 0 else None

real_saves = dict[str, tuple[dict[str, Any], dict[str, Any]]]()

pickup_ignored = {
    "deployed_figurine_polishskull_c",
}
pickup_regexes = (
    (re.compile("^deployed_bobblehead_scientist_c$"), "bobblehead_sci"),
    (re.compile("^deployed_bobblehead_secguard_c$"), "bobblehead_sec"),
    (re.compile(r"^deployed_bobblehead_(\w+)_c$"), r"bobblehead_\1"),
    (re.compile("^deployed_figurine_composer_c$"), "fig_comp"),
    (re.compile(r"^deployed_(\w*)figurine_(\w+)_c$"), r"fig_\1\2"),
    (re.compile(r"^deployed_(painting_\w+|poster)_c$"), r"\1"),
)

picked_items = list[tuple[str, str, dict[str, Any]]]()
for save_file in save_folder.glob("WorldSave_*.sav"):
    matches = world_save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid save file name: {save_file.name}")
    with save_file.open("rb") as f:
        data = f.read()
    header, offset = ABFWorldHeaderSerde.from_bytes(data, 0)
    bodysize = header.get("bodysize", None)
    if bodysize is None:
        expected_offset = None
    elif bodysize >= 4:
        expected_offset = offset + bodysize
    else:
        raise ValueError(f"Invalid body size at {offset}")
    body, offset = GVASBlueprintStructPropertySerde.from_bytes(data, offset)
    if struct.unpack_from("<I", data, offset)[0] != 0:
        raise ValueError(f"Invalid ending at {offset}")
    if expected_offset is not None and offset + 4 != expected_offset:
        raise ValueError(f"Invalid offset {offset}")
    identifier = matches[1]
    if identifier == "MetaData":
        real_saves[identifier] = header, body
        continue
    if identifier == "Facility":
        real_saves[identifier] = header, body
    updated = False
    deployed_object_map = body.get("DeployedObjectMap")
    if deployed_object_map is not None:
        deployed_objects = dict[str, dict[str, Any]]()
        for asset_id, deployed_object in deployed_object_map["value"]["values"]:
            if asset_id in deployed_objects:
                raise ValueError(f"Duplicate asset ID {asset_id}")
            matched = False
            object_name = deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()
            if object_name not in pickup_ignored:
                for pickup_regex, replacement in pickup_regexes:
                    mangled_name = pickup_regex.sub(replacement, object_name)
                    if mangled_name != object_name:
                        matched = True
                        picked_items.append(("/Game/Blueprints/Items/ItemTable_Global.ItemTable_Global", mangled_name, deployed_object["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]))
                        break
            if not matched:
                deployed_objects[asset_id] = deployed_object
        if len(deployed_objects) != len(deployed_object_map["value"]["values"]):
            updated = True
            deployed_object_map["value"]["values"] = list(map(list, deployed_objects.items()))
    dropped_item_map = body.get("DroppedItemMap")
    if dropped_item_map:
        updated = True
        for asset_id, dropped_item in dropped_item_map["value"]["values"]:
            if asset_id in picked_items:
                raise ValueError(f"Duplicate asset ID {asset_id}")
            slot = dropped_item["ItemData_41_A1D40E254568FE81F5A36EB0FFF12116"]["value"]
            data = slot["ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B"]["value"]
            picked_items.append((data["DataTable"]["value"], data["RowName"]["value"], slot["ChangeableData_12_2B90E1F74F648135579D39A49F5A2313"]))
        dropped_item_map["value"]["values"] = []
    if identifier != "Facility" and updated:
        body = GVASBlueprintStructPropertySerde.from_json(body) + struct.pack("<I", 0)
        header["bodysize"] = len(body)
        header = ABFWorldHeaderSerde.from_json(header)
        with (output_folder / f"WorldSave_{identifier}.sav").open("wb") as f:
            f.write(header)
            f.write(body)

if picked_items:
    storage_regex = re.compile(r"^deployed_storagecrate_makeshift_t[1-4]_c$")
    header, body = real_saves.pop("Facility")
    deployed_objects_map = body.get("DeployedObjectMap")
    if deployed_objects_map is None:
        raise ValueError("Missing deployed object map in main save")
    deployed_objects = dict[str, dict[str, Any]]()
    for asset_id, deployed_object in deployed_objects_map["value"]["values"]:
        if storage_regex.match(deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()) is None:
            continue
        if labels_regex is not None and labels_regex.match(deployed_object["CustomTextDisplay_152_B59A50C74001B5D2234D9E9B0D7CAB7F"]["value"].lower()) is None:
            continue
        for content in deployed_object["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"]:
            for slot in content["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"]:
                data = slot["ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B"]["value"]
                item_name = data["RowName"]["value"].lower()
                if item_name not in ("", "empty", "none"):
                    continue
                item_blueprint, item_name, item = picked_items.pop()
                data["DataTable"]["value"] = item_blueprint
                data["RowName"]["value"] = item_name
                slot["ChangeableData_12_2B90E1F74F648135579D39A49F5A2313"] = item
                if not picked_items:
                    break
            if not picked_items:
                break
        if not picked_items:
            break
    if picked_items:
        raise ValueError(f"Left {len(picked_items)} orphaned items")
    body = GVASBlueprintStructPropertySerde.from_json(body) + struct.pack("<I", 0)
    header["bodysize"] = len(body)
    header = ABFWorldHeaderSerde.from_json(header)
    with (output_folder / "WorldSave_Facility.sav").open("wb") as f:
        f.write(header)
        f.write(body)
