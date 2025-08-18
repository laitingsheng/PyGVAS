import itertools
import math
import os
import re
import sys
from pathlib import Path
from typing import Any
from uuid import UUID

from .._items import create_empty_item, create_plant_proxy
from .._objects import (
    DEPLOYED_BARREL,
    DEPLOYED_BED,
    DEPLOYED_FARM,
    DEPLOYED_STORAGE,
    create_object_inventory,
    deploy_facility_object,
    form_deployed_object_identifier,
    get_object_asset_id,
    object_extract_inventories,
    object_extract_proxied_item_ids,
    object_fill,
    object_label,
    object_move,
    object_paint,
    object_rename,
    object_repair,
    object_set_tags,
    object_set_variant,
)
from .._saves import ABFWorldSave
from .._utils import create_asset_id, create_datatable_row_handle
from ._presets import (
    DEPLOY_BARRELS,
    DEPLOY_BEDS,
    DEPLOY_FARMS,
    DEPLOY_STORAGES,
    IGNORE_LABELS,
    PICKUP_TARGETS,
    REPLACE_TARGETS,
    TARGET_IDENTIFIER,
)


entry, profile, name = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name

player_save_regex = re.compile(r"Player_([A-Za-z0-9]+)\.sav")

players: list[str] = []
for save_file in (save_folder / "PlayerData").glob("Player_*.sav"):
    matches = player_save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid player save file name {save_file.name}")
    players.append(matches[1])

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

world_save_regex = re.compile(r"WorldSave_(\w+)\.sav")
saves: dict[str, ABFWorldSave] = {}
updated_saves: dict[str, bool] = {}

unused_asset_ids: set[UUID] = set()

all_wall_power_sockets: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
wall_power_sockets_locations: dict[str, str] = {}
all_power_sockets: dict[str, dict[UUID, dict[int, dict[str, dict[str, Any]]]]] = {}
power_sockets_locations: dict[UUID, str] = {}
connections_to_wall: dict[UUID, str] = {}
connections: dict[UUID, tuple[UUID, int]] = {}

socket_id_regex = re.compile(r"([0-9A-F]{32})(\d+)")

all_builtin_objects: dict[str, dict[str, dict[str, Any]]] = {}
builtin_objects_identifiers: dict[str, str] = {}
all_deployed_objects: dict[str, dict[UUID, dict[str, dict[str, Any]]]] = {}
deployed_objects_identifiers: dict[UUID, str] = {}

dropped_items: list[dict[str, dict[str, Any]]] = []

candidates: dict[UUID, None] = {}

for save_file in save_folder.glob("WorldSave_*.sav"):
    matches = world_save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid save file name {save_file.name}")
    identifier = matches[1]
    if identifier in saves:
        raise ValueError(f"Duplicate save identifier {identifier}")
    save = ABFWorldSave.from_binary_file(save_file)
    saves[identifier] = save

    deployed_object_map = save.body.get("DeployedObjectMap")
    if deployed_object_map is not None:
        for asset_id, deployed_object in deployed_object_map["value"]["values"]:
            parsed_asset_id = get_object_asset_id(deployed_object)
            if parsed_asset_id is None:
                if asset_id in builtin_objects_identifiers:
                    raise ValueError(f"Duplicate built-in object ID {asset_id}")
                all_builtin_objects.setdefault(identifier, {})[asset_id] = deployed_object
                builtin_objects_identifiers[asset_id] = identifier
                continue
            if asset_id != parsed_asset_id.hex.upper():
                raise ValueError(f"Inconsistent asset ID in deployed object {asset_id}")
            if parsed_asset_id in deployed_objects_identifiers:
                raise ValueError(f"Duplicate deployed object ID {asset_id}")

            object_name = deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()
            picked = PICKUP_TARGETS.get(object_name)
            if picked is not None:
                data = deployed_object.pop("ChangableData_37_6153F4A94F01A776C108038B7F38E256")
                dropped_items.append(
                    {
                        "ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B": create_datatable_row_handle(
                            datatable="/Game/Blueprints/Items/ItemTable_Global.ItemTable_Global",
                            rowname=picked,
                        ),
                        "ChangeableData_12_2B90E1F74F648135579D39A49F5A2313": data,
                    },
                )
                continue

            all_deployed_objects.setdefault(identifier, {})[parsed_asset_id] = deployed_object
            deployed_objects_identifiers[parsed_asset_id] = identifier

            if object_name in REPLACE_TARGETS:
                candidates[parsed_asset_id] = None

    dropped_item_map = save.body.get("DroppedItemMap")
    if dropped_item_map is not None:
        unfolded_dropped_items = dropped_item_map["value"]["values"]
        if unfolded_dropped_items:
            for asset_id, dropped_item in unfolded_dropped_items:
                dropped_items.append(dropped_item.pop("ItemData_41_A1D40E254568FE81F5A36EB0FFF12116").pop("value"))
            dropped_item_map["value"]["values"] = []
            updated_saves[identifier] = True

    power_socket_map = save.body.get("PowerSocketMap")
    if power_socket_map is not None:
        wall_power_sockets = all_wall_power_sockets.setdefault(identifier, {})
        power_sockets = all_power_sockets.setdefault(identifier, {})
        for socket_id, socket in power_socket_map["value"]["values"]:
            device = socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"]
            if socket_id.startswith("/Game/"):
                if socket_id in wall_power_sockets_locations:
                    raise ValueError(f"Duplicate wall power socket {socket_id}")
                wall_power_sockets_locations[socket_id] = identifier
                wall_power_sockets[socket_id] = socket
                if device != "-1":
                    device = UUID(device)
                    if device in connections_to_wall or device in connections:
                        print(f"Cutting duplicate connections of {socket_id} from {device}")
                        socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"] = "-1"
                        updated_saves[identifier] = True
                    else:
                        connections_to_wall[device] = socket_id
                continue
            matches = socket_id_regex.match(socket_id)
            if matches is None:
                raise ValueError(f"Invalid power socket ID {socket_id}")
            asset_id = UUID(matches[1])
            existing_location = power_sockets_locations.get(asset_id)
            if existing_location is None:
                power_sockets_locations[asset_id] = identifier
            elif existing_location != identifier:
                raise ValueError(f"Inconsistent power socket board {asset_id}")
            socket_index = int(matches[2])
            board = power_sockets.setdefault(asset_id, {})
            if socket_index in board:
                raise ValueError(f"Duplicate socket {socket_index} for asset {asset_id}")
            board[socket_index] = socket
            if device != "-1":
                device = UUID(device)
                if device in connections_to_wall or device in connections:
                    print(f"Cutting duplicate connections of {asset_id} {socket_index} from {device}")
                    socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"] = "-1"
                    updated_saves[identifier] = True
                else:
                    connections[device] = asset_id, socket_index

new_objects: dict[UUID, dict[str, dict[str, Any]]] = {}

for index, (start, direction, spacing, locations) in enumerate(DEPLOY_BEDS):
    sx = start["x"]
    sy = start["y"]
    sz = start["z"]
    dx = spacing.get("x", 0.0)
    dy = spacing.get("y", 0.0)
    dz = spacing.get("z", 0.0)

    for player_index, (ix, iy, iz) in locations.items():
        px = sx + ix * dx
        py = sy + iy * dy
        pz = sz + iz * dz

        def key(asset_id: UUID) -> float:
            obj = all_deployed_objects[deployed_objects_identifiers[asset_id]][asset_id]
            tp = obj["Transform_50_85E8B13D40141C9B1308F4BB943BD753"]["value"]["Translation"]["value"]
            return math.dist((px, py, pz), (tp["x"], tp["y"], tp["z"]))

        if candidates:
            asset_id = min(candidates.keys(), key=key)
            if asset_id in new_objects:
                raise ValueError(f"Duplicate usage of liquid container {asset_id}")
            del candidates[asset_id]
            identifier = deployed_objects_identifiers.pop(asset_id)
            deployed_object = all_deployed_objects[identifier].pop(asset_id)
            updated_saves[identifier] = True
            dropped_items.extend(object_extract_inventories(deployed_object))
            unused_asset_ids.update(object_extract_proxied_item_ids(deployed_object))
            object_fill(deployed_object, 0)
            object_label(deployed_object, f"{players[player_index]}}}|!|{{")
            object_move(deployed_object, px, py, pz, direction)
            object_paint(deployed_object, 13)
            object_rename(deployed_object, *DEPLOYED_BED)
            object_repair(deployed_object)
            object_set_tags(deployed_object, [])
            object_set_variant(deployed_object, "", "None")
        else:
            asset_id = create_asset_id()
            while asset_id in all_deployed_objects or asset_id in new_objects:
                asset_id = create_asset_id()
            deployed_object = deploy_facility_object(
                asset_id,
                *form_deployed_object_identifier(*DEPLOYED_BED, 0x7FFFFF00),
                px,
                py,
                pz,
                direction,
                label=f"{players[player_index]}}}|!|{{",
                paint=13,
            )
        new_objects[asset_id] = deployed_object

for index, (start, direction, spacing, locations) in enumerate(DEPLOY_BARRELS):
    sx = start["x"]
    sy = start["y"]
    sz = start["z"]
    dx = spacing.get("x", 0.0)
    dy = spacing.get("y", 0.0)
    dz = spacing.get("z", 0.0)

    for liquid, (six, siy, siz), (cx, cy, cz) in locations:
        if liquid not in {1, 2, 3, 4, 11, 13, 16}:
            raise ValueError(f"Invalid liquid content in {index}")
        if cx < 0 or six < 0:
            raise ValueError(f"Invalid x-axis in {index}")
        if dx == 0.0 and (cx > 1 or six > 0):
            raise ValueError(f"Spanning across x-axis is not supported in {index}")
        if cy < 0 or siy < 0:
            raise ValueError(f"Invalid y-axis in {index}")
        if dy == 0.0 and (cy > 1 or siy > 0):
            raise ValueError(f"Spanning across y-axis is not supported in {index}")
        if cz < 0 or siz < 0:
            raise ValueError(f"Invalid z-axis in {index}")
        if dz == 0.0 and (cz > 1 or siz > 0):
            raise ValueError(f"Spanning across z-axis is not supported in {index}")

        for ix, iy, iz in itertools.product(range(cx), range(cy), range(cz)):
            px = sx + (six + ix) * dx
            py = sy + (siy + iy) * dy
            pz = sz + (siz + iz) * dz

            def key(asset_id: UUID) -> float:
                obj = all_deployed_objects[deployed_objects_identifiers[asset_id]][asset_id]
                tp = obj["Transform_50_85E8B13D40141C9B1308F4BB943BD753"]["value"]["Translation"]["value"]
                return math.dist((px, py, pz), (tp["x"], tp["y"], tp["z"]))

            if candidates:
                asset_id = min(candidates.keys(), key=key)
                if asset_id in new_objects:
                    raise ValueError(f"Duplicate usage of liquid container {asset_id}")
                del candidates[asset_id]
                identifier = deployed_objects_identifiers.pop(asset_id)
                deployed_object = all_deployed_objects[identifier].pop(asset_id)
                updated_saves[identifier] = True
                dropped_items.extend(object_extract_inventories(deployed_object))
                unused_asset_ids.update(object_extract_proxied_item_ids(deployed_object))
                object_fill(deployed_object, liquid)
                object_label(deployed_object, "")
                object_move(deployed_object, px, py, pz, direction)
                object_paint(deployed_object, 13)
                object_rename(deployed_object, *DEPLOYED_BARREL)
                object_repair(deployed_object)
                object_set_tags(deployed_object, [])
                object_set_variant(deployed_object, "", "None")
            else:
                asset_id = create_asset_id()
                while asset_id in all_deployed_objects or asset_id in new_objects:
                    asset_id = create_asset_id()
                deployed_object = deploy_facility_object(
                    asset_id,
                    *form_deployed_object_identifier(*DEPLOYED_BARREL, 0x7FFFFF00),
                    px,
                    py,
                    pz,
                    direction,
                    liquid=liquid,
                    paint=13,
                )
            new_objects[asset_id] = deployed_object

label_storages: dict[str, list[dict[str, dict[str, Any]]]] = {}

for index, (start, direction, spacing, locations) in enumerate(DEPLOY_STORAGES):
    sx = start["x"]
    sy = start["y"]
    sz = start["z"]
    dx = spacing.get("x", 0.0)
    dy = spacing.get("y", 0.0)
    dz = spacing.get("z", 0.0)

    for label, (six, siy, siz), (cx, cy, cz) in locations:
        if cx < 0 or six < 0:
            raise ValueError(f"Invalid x-axis in {index}")
        if dx == 0.0 and (cx > 1 or six > 0):
            raise ValueError(f"Spanning across x-axis is not supported in {index}")
        if cy < 0 or siy < 0:
            raise ValueError(f"Invalid y-axis in {index}")
        if dy == 0.0 and (cy > 1 or siy > 0):
            raise ValueError(f"Spanning across y-axis is not supported in {index}")
        if cz < 0 or siz < 0:
            raise ValueError(f"Invalid z-axis in {index}")
        if dz == 0.0 and (cz > 1 or siz > 0):
            raise ValueError(f"Spanning across z-axis is not supported in {index}")

        if label in IGNORE_LABELS:
            label = ""

        for ix, iy, iz in itertools.product(range(cx), range(cy), range(cz)):
            px = sx + (six + ix) * dx
            py = sy + (siy + iy) * dy
            pz = sz + (siz + iz) * dz

            def key(asset_id: UUID) -> float:
                obj = all_deployed_objects[deployed_objects_identifiers[asset_id]][asset_id]
                tp = obj["Transform_50_85E8B13D40141C9B1308F4BB943BD753"]["value"]["Translation"]["value"]
                return math.dist((px, py, pz), (tp["x"], tp["y"], tp["z"]))

            if candidates:
                asset_id = min(candidates.keys(), key=key)
                if asset_id in new_objects:
                    raise ValueError(f"Duplicate usage of storage container {asset_id}")
                del candidates[asset_id]
                identifier = deployed_objects_identifiers.pop(asset_id)
                deployed_object = all_deployed_objects[identifier].pop(asset_id)
                updated_saves[identifier] = True
                dropped_items.extend(object_extract_inventories(deployed_object))
                unused_asset_ids.update(object_extract_proxied_item_ids(deployed_object))
                object_fill(deployed_object, 0)
                object_label(deployed_object, label)
                object_move(deployed_object, px, py, pz, direction)
                object_paint(deployed_object, 13)
                object_rename(deployed_object, *DEPLOYED_STORAGE)
                object_repair(deployed_object)
                object_set_tags(deployed_object, [])
                object_set_variant(deployed_object, "", "None")
            else:
                asset_id = create_asset_id()
                while asset_id in all_deployed_objects or asset_id in new_objects:
                    asset_id = create_asset_id()
                deployed_object = deploy_facility_object(
                    asset_id,
                    *form_deployed_object_identifier(*DEPLOYED_STORAGE, 0x7FFFFF00),
                    px,
                    py,
                    pz,
                    direction,
                    label=label,
                    paint=13,
                )
            new_objects[asset_id] = deployed_object
            label_storages.setdefault(label, []).append(deployed_object)

for index, (start, direction, spacing, locations) in enumerate(DEPLOY_FARMS):
    sx = start["x"]
    sy = start["y"]
    sz = start["z"]
    dx = spacing.get("x", 0.0)
    dy = spacing.get("y", 0.0)
    dz = spacing.get("z", 0.0)

    for (ix, iy, iz), plants in locations.items():
        px = sx + ix * dx
        py = sy + iy * dy
        pz = sz + iz * dz

        def key(asset_id: UUID) -> float:
            obj = all_deployed_objects[deployed_objects_identifiers[asset_id]][asset_id]
            tp = obj["Transform_50_85E8B13D40141C9B1308F4BB943BD753"]["value"]["Translation"]["value"]
            return math.dist((px, py, pz), (tp["x"], tp["y"], tp["z"]))

        if candidates:
            asset_id = min(candidates.keys(), key=key)
            if asset_id in new_objects:
                raise ValueError(f"Duplicate usage of liquid container {asset_id}")
            del candidates[asset_id]
            identifier = deployed_objects_identifiers.pop(asset_id)
            deployed_object = all_deployed_objects[identifier].pop(asset_id)
            updated_saves[identifier] = True
            dropped_items.extend(object_extract_inventories(deployed_object))
            unused_asset_ids.update(object_extract_proxied_item_ids(deployed_object))
            object_fill(deployed_object, 1)
            object_label(deployed_object, "")
            object_move(deployed_object, px, py, pz, direction)
            object_paint(deployed_object, 13)
            object_rename(deployed_object, *DEPLOYED_FARM)
            object_repair(deployed_object)
            object_set_tags(deployed_object, [])
            object_set_variant(deployed_object, "", "None")
        else:
            asset_id = create_asset_id()
            while asset_id in all_deployed_objects or asset_id in new_objects:
                asset_id = create_asset_id()
            deployed_object = deploy_facility_object(
                asset_id,
                *form_deployed_object_identifier(*DEPLOYED_FARM, 0x7FFFFF00),
                px,
                py,
                pz,
                direction,
                liquid=1,
                paint=13,
            )
        deployed_object["ItemProxies_149_E2E145CE4015C4EDFA89E2B0CE3F579A"]["value"]["values"] = [
            create_plant_proxy(
                index,
                unused_asset_ids.pop() if unused_asset_ids else create_asset_id(),
                plant,
            ) for index, plant in enumerate(plants)
        ]
        new_objects[asset_id] = deployed_object

print(f"Attempting to put {len(dropped_items)} dropped items into storages.")

arbitrary_storages = label_storages.pop("", [])
for storage in arbitrary_storages:
    items = dropped_items[-42:]
    del dropped_items[-42:]
    items.extend(create_empty_item() for _ in range(42 - len(items)))
    inventory = create_object_inventory(0)
    inventory["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"] = items
    storage["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"] = [inventory]

target_save = saves.pop(TARGET_IDENTIFIER)

for identifier, save in saves.items():
    updated = updated_saves.pop(identifier, False)

    deployed_object_map = save.body.get("DeployedObjectMap")
    if deployed_object_map is None:
        if identifier in all_builtin_objects or identifier in all_deployed_objects:
            raise ValueError(f"Missing deployed object map in save {identifier}")
    else:
        unfolded_deployed_objects: list[tuple[str, dict[str, dict[str, Any]]]] = []
        builtin_objects = all_builtin_objects.pop(identifier, None)
        if builtin_objects is not None:
            for asset_id in builtin_objects:
                del builtin_objects_identifiers[asset_id]
            unfolded_deployed_objects.extend(
                (asset_id, builtin_object) for asset_id, builtin_object in builtin_objects.items()
            )
        deployed_objects = all_deployed_objects.pop(identifier, None)
        if deployed_objects is not None:
            for asset_id in deployed_objects:
                del deployed_objects_identifiers[asset_id]
            unfolded_deployed_objects.extend(
                (asset_id.hex.upper(), deployed_object) for asset_id, deployed_object in deployed_objects.items()
            )
        if len(unfolded_deployed_objects) != len(deployed_object_map["value"]["values"]):
            deployed_object_map["value"]["values"] = unfolded_deployed_objects
            updated = True

    if updated:
        save.to_binary_file(output_folder / f"WorldSave_{identifier}.sav")

deployed_object_map = target_save.body["DeployedObjectMap"]
unfolded_deployed_objects: list[tuple[str, dict[str, dict[str, Any]]]] = []
builtin_objects = all_builtin_objects.pop(TARGET_IDENTIFIER, None)
if builtin_objects is not None:
    for asset_id in builtin_objects:
        del builtin_objects_identifiers[asset_id]
    unfolded_deployed_objects.extend((asset_id, builtin_object) for asset_id, builtin_object in builtin_objects.items())
deployed_objects = all_deployed_objects.pop(TARGET_IDENTIFIER, None)
if deployed_objects is not None:
    for asset_id in deployed_objects:
        del deployed_objects_identifiers[asset_id]
    unfolded_deployed_objects.extend(
        (asset_id.hex.upper(), deployed_object) for asset_id, deployed_object in deployed_objects.items()
    )
unfolded_deployed_objects.extend(
    (asset_id.hex.upper(), deployed_object) for asset_id, deployed_object in new_objects.items()
)
deployed_object_map["value"]["values"] = unfolded_deployed_objects

if all_builtin_objects or all_deployed_objects or builtin_objects_identifiers or deployed_objects_identifiers:
    raise ValueError("Unprocessed objects remain.")

print(f"Left {len(candidates)} containers unused.")
print(f"Left {len(dropped_items)} dropped items unprocessed.")
print(f"Left {len(unused_asset_ids)} unused asset IDs.")

target_save.to_binary_file(output_folder / f"WorldSave_{TARGET_IDENTIFIER}.sav")
