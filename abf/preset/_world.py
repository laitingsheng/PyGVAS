import itertools
from typing import Any, Iterable, Sequence
from uuid import UUID

from .._items import create_empty_item, create_global_item, create_plant_proxy
from .._objects import (
    create_object_inventory,
    deploy_facility_object,
    form_deployed_object_identifier,
    object_get_asset_id,
)
from .._utils import create_asset_id


all_builtin_objects: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
builtin_objects_identifiers: dict[str, str] = {}
all_deployed_objects: dict[str, dict[UUID, dict[str, dict[str, Any]]]] = {}
deployed_objects_identifiers: dict[UUID, str] = {}


def preprocess_objects(identifier: str, world: dict[str, dict[str, Any]], ignore: set[str]) -> bool:
    updated = False

    deployed_object_map = world.get("DeployedObjectMap")
    if deployed_object_map is not None:
        if identifier in all_builtin_objects or identifier in all_deployed_objects:
            raise ValueError(f"Duplicate world identifier {identifier}")
        builtin_objects = all_builtin_objects[identifier] = {}
        deployed_objects = all_deployed_objects[identifier] = {}
        for asset_id, deployed_object in deployed_object_map["value"]["values"]:
            parsed_asset_id = object_get_asset_id(deployed_object)
            if parsed_asset_id is None:
                if asset_id in builtin_objects_identifiers:
                    raise ValueError(f"Duplicate built-in object ID {asset_id}")
                builtin_objects[asset_id] = deployed_object
                builtin_objects_identifiers[asset_id] = identifier
                continue
            if asset_id != parsed_asset_id.hex.upper():
                raise ValueError(f"Inconsistent asset ID in deployed object {asset_id}")
            object_name = deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()
            if object_name in ignore:
                updated = True
                continue
            if parsed_asset_id in deployed_objects_identifiers:
                raise ValueError(f"Duplicate deployed object ID {asset_id}")
            deployed_objects[parsed_asset_id] = deployed_object
            deployed_objects_identifiers[parsed_asset_id] = identifier

    dropped_item_map = world.get("DroppedItemMap")
    if dropped_item_map is not None:
        unfolded_dropped_items = dropped_item_map["value"]["values"]
        if unfolded_dropped_items:
            for asset_id, dropped_item in unfolded_dropped_items:
                data = dropped_item["ItemData_41_A1D40E254568FE81F5A36EB0FFF12116"]["value"]
                datatable = data["ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B"]["value"]
                name = datatable["RowName"]["value"].lower()
                print(f"{identifier}: Purged dropped item {asset_id} {name}")
            dropped_item_map["value"]["values"] = []
            updated = True

    return updated


all_wall_power_sockets: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
wall_power_sockets_identifiers: dict[str, str] = {}
all_power_sockets: dict[str, dict[UUID, dict[int, dict[str, dict[str, Any]]]]] = {}
power_sockets_identifiers: dict[UUID, str] = {}
wall_connections: dict[UUID, str] = {}
connections: dict[UUID, tuple[UUID, int]] = {}


def process_sockets(identifier: str, world: dict[str, dict[str, Any]]) -> bool:
    updated = False

    power_socket_map = world.get("PowerSocketMap")
    if power_socket_map is not None:
        if identifier in all_wall_power_sockets or identifier in all_power_sockets:
            raise ValueError(f"Duplicate world identifier {identifier}")
        wall_power_sockets = all_wall_power_sockets[identifier] = {}
        power_sockets = all_power_sockets[identifier] = {}
        for socket_id, socket in power_socket_map["value"]["values"]:
            device = socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"]
            if device == "-1":
                device = None
            else:
                device = UUID(device)
                if device not in deployed_objects_identifiers:
                    socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"] = "-1"
                    print(f"{identifier}: Dropped unknown connection from {device} to {socket_id}")
                    device = None
                    updated = True
            if socket_id.startswith("/Game/"):
                if socket_id in wall_power_sockets_identifiers:
                    raise ValueError(f"Duplicate wall power socket {socket_id}")
                wall_power_sockets_identifiers[socket_id] = identifier
                wall_power_sockets[socket_id] = socket
                if device is not None:
                    wall_connections[device] = socket_id
                continue
            asset_id = UUID(socket_id[:32])
            socket_index = int(socket_id[32:])
            if asset_id not in deployed_objects_identifiers:
                print(f"{identifier}: Dropped unknown power socket {asset_id} {socket_index}")
                updated = True
                continue
            existing_identifier = power_sockets_identifiers.get(asset_id)
            if existing_identifier is None:
                power_sockets_identifiers[asset_id] = identifier
            elif existing_identifier != identifier:
                raise ValueError(f"Inconsistent power socket board {asset_id}")
            board = power_sockets.setdefault(asset_id, {})
            if socket_index in board:
                raise ValueError(f"Duplicate socket {socket_index} for asset {asset_id}")
            board[socket_index] = socket
            if device is not None:
                connections[device] = asset_id, socket_index

    return updated


def prune_connections() -> dict[str, None]:
    updated_identifiers: dict[str, None] = {}

    for identifier, deployed_objects in all_deployed_objects.items():
        reroutes: list[UUID] = []
        for asset_id, deployed_object in deployed_objects.items():
            if (
                deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower()
                == "deployed_cablereroute_c"
            ):
                reroutes.append(asset_id)
        if reroutes:
            for asset_id in reroutes:
                if deployed_objects_identifiers.pop(asset_id) != identifier:
                    raise ValueError(f"Inconsistent object identifier for {asset_id}")
                del deployed_objects[asset_id]
                if power_sockets_identifiers.pop(asset_id) != identifier:
                    raise ValueError(f"Inconsistent power socket identifier for {asset_id}")
                board = all_power_sockets[identifier].pop(asset_id)
                if len(board) != 1:
                    raise ValueError(f"Reroute {asset_id} should not have more than one connections")
                socket_index, socket = board.popitem()
                if socket_index != 1:
                    raise ValueError(f"Reroute {asset_id} should not have socket index {socket_index}")
                device = socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"]
                device = None if device == "-1" else UUID(device)
                source_id = wall_connections.pop(asset_id, None)
                if source_id is None:
                    source_id, source_index = connections.pop(asset_id)
                    source_identifier = power_sockets_identifiers[source_id]
                    source_socket = all_power_sockets[source_identifier][source_id][source_index]
                    if device is not None:
                        connections[device] = source_id, source_index
                else:
                    source_identifier = wall_power_sockets_identifiers[source_id]
                    source_socket = all_wall_power_sockets[source_identifier][source_id]
                    if device is not None:
                        wall_connections[device] = source_id
                source_socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"] = (
                    "-1" if device is None else device.hex.upper()
                )
                updated_identifiers[source_identifier] = None
                print(f"Removed route {asset_id}")
            updated_identifiers[identifier] = None

    return updated_identifiers


_BED_OBJECT_DESCRIPTOR = form_deployed_object_identifier(
    "Furniture",
    "Deployed_Furniture_CraftedBed_T2",
    0x7FFFFF00,
)


def deploy_beds(
    identifier: str,
    paint: int,
    players: list[str],
    beds: Iterable[
        tuple[
            tuple[float, float, float],
            tuple[float, float],
            str,
            dict[int, tuple[int, int]],
        ]
    ],
) -> None:
    deployed_objects = all_deployed_objects.setdefault(identifier, {})
    for start, spacing, direction, locations in beds:
        sx, sy, z = start
        dx, dy = spacing
        for player_index, (ix, iy) in locations.items():
            if ix < 0:
                raise ValueError(f"{player_index} has invalid x index {ix}")
            if dx == 0.0 and ix > 0:
                raise ValueError(f"{player_index} cannot span across x axis")
            if iy < 0:
                raise ValueError(f"{player_index} has invalid y index {iy}")
            if dy == 0.0 and iy > 0:
                raise ValueError(f"{player_index} cannot span across y axis")
            x = sx + ix * dx
            y = sy + iy * dy
            asset_id = create_asset_id()
            while asset_id in deployed_objects_identifiers:
                asset_id = create_asset_id()
            deployed_objects[asset_id] = deploy_facility_object(
                asset_id,
                *_BED_OBJECT_DESCRIPTOR,
                x,
                y,
                z,
                direction,
                label=f"{players[player_index]}}}|!|{{",
                paint=paint,
            )


_FARM_OBJECT_DESCRIPTOR = form_deployed_object_identifier(
    "Farming",
    "GardenPlot_Large",
    0x7FFFFF00,
)


def deploy_farms(
    identifier: str,
    paint: int,
    farms: Iterable[
        tuple[
            tuple[float, float, float],
            tuple[float, float],
            str,
            dict[tuple[int, int], Sequence[str]],
        ]
    ],
) -> None:
    deployed_objects = all_deployed_objects.setdefault(identifier, {})
    for fi, (start, spacing, direction, locations) in enumerate(farms):
        sx, sy, z = start
        dx, dy = spacing
        for li, ((ix, iy), plants) in enumerate(locations.items()):
            if ix < 0:
                raise ValueError(f"({fi}, {li}) has invalid x index {ix}")
            if dx == 0.0 and ix > 0:
                raise ValueError(f"({fi}, {li}) cannot span across x axis")
            if iy < 0:
                raise ValueError(f"({fi}, {li}) has invalid y index {iy}")
            if dy == 0.0 and iy > 0:
                raise ValueError(f"({fi}, {li}) cannot span across y axis")
            if len(plants) > 8:
                raise ValueError(f"({fi}, {li}) has too many plants")
            x = sx + ix * dx
            y = sy + iy * dy
            asset_id = create_asset_id()
            while asset_id in deployed_objects_identifiers:
                asset_id = create_asset_id()
            deployed_object = deploy_facility_object(
                asset_id,
                *_FARM_OBJECT_DESCRIPTOR,
                x,
                y,
                z,
                direction,
                liquid=1,
                made_string=",|,".join(itertools.repeat("0", len(plants))),
                paint=paint,
            )
            deployed_object["ItemProxies_149_E2E145CE4015C4EDFA89E2B0CE3F579A"]["value"]["values"] = [
                create_plant_proxy(index, create_asset_id(), plant) for index, plant in enumerate(plants)
            ]
            deployed_objects[asset_id] = deployed_object


_LIQUID_CONTAINER_OBJECT_DESCRIPTOR = form_deployed_object_identifier(
    "Furniture",
    "Deployed_LiquidContainer_Barrel",
    0x7FFFFF00,
)
_NON_USABLE_LIQUIDS = {6, 7, 9}
_ENERGY_LIQUIDS = {8, 15}
_VARIANT_SPEC_LIQUIDS = {14}
_VALID_LIQUIDS = {1, 2, 3, 4, 11, 13, 16}


def deploy_liquid_containers(
    identifier: str,
    paint: int,
    containers: Iterable[
        tuple[
            tuple[float, float, float],
            tuple[float, float],
            str,
            tuple[int, int],
            Sequence[int],
        ]
    ],
) -> None:
    deployed_objects = all_deployed_objects.setdefault(identifier, {})
    for fi, (start, spacing, direction, dimensions, liquids) in enumerate(containers):
        sx, sy, z = start
        dx, dy = spacing
        cx, cy = dimensions
        if cx < 0:
            raise ValueError(f"{fi} has invalid x dimension {cx}")
        if dx == 0.0 and cx > 1:
            raise ValueError(f"{fi} cannot span across x axis")
        if cy < 0:
            raise ValueError(f"{fi} has invalid y dimension {cy}")
        if dy == 0.0 and cy > 1:
            raise ValueError(f"{fi} cannot span across y axis")
        if cx == 0 or cy == 0:
            continue
        coordinates = list(itertools.product(range(cx), range(cy)))
        if len(liquids) != len(coordinates):
            raise ValueError(f"{fi} liquids length mismatched")
        for (ix, iy), liquid in zip(coordinates, liquids):
            if liquid in _NON_USABLE_LIQUIDS:
                raise ValueError(f"{fi} has non-usable liquid {liquid}")
            if liquid in _ENERGY_LIQUIDS:
                raise ValueError(f"{fi} has energy liquid {liquid}")
            if liquid in _VARIANT_SPEC_LIQUIDS:
                raise ValueError(f"{fi} has liquid {liquid} that must have variant spec")
            if liquid not in _VALID_LIQUIDS:
                raise ValueError(f"{fi} has unknown liquid {liquid}")
            asset_id = create_asset_id()
            while asset_id in deployed_objects_identifiers:
                asset_id = create_asset_id()
            deployed_objects[asset_id] = deploy_facility_object(
                asset_id,
                *_LIQUID_CONTAINER_OBJECT_DESCRIPTOR,
                sx + ix * dx,
                sy + iy * dy,
                z,
                direction,
                liquid=liquid,
                paint=paint,
            )


_STORAGE_OBJECT_DESCRIPTOR = form_deployed_object_identifier(
    "Furniture",
    "Deployed_StorageCrate_Makeshift_T4",
    0x7FFFFF00,
)


def deploy_storages(
    identifier: str,
    paint: int,
    containers: Iterable[
        tuple[
            tuple[float, float, float],
            tuple[float, float, float],
            str,
            tuple[int, int, int],
            Sequence[tuple[str, Sequence[dict[str, Any]]]],
        ]
    ],
) -> None:
    deployed_objects = all_deployed_objects.setdefault(identifier, {})
    for fi, (start, spacing, direction, dimensions, inventories) in enumerate(containers):
        sx, sy, sz = start
        dx, dy, dz = spacing
        cx, cy, cz = dimensions
        if cx < 0:
            raise ValueError(f"{fi} has invalid x dimension {cx}")
        if dx == 0.0 and cx > 1:
            raise ValueError(f"{fi} cannot span across x axis")
        if cy < 0:
            raise ValueError(f"{fi} has invalid y dimension {cy}")
        if dy == 0.0 and cy > 1:
            raise ValueError(f"{fi} cannot span across y axis")
        if cz < 0:
            raise ValueError(f"{fi} has invalid z dimension {cz}")
        if dz == 0.0 and cz > 1:
            raise ValueError(f"{fi} cannot span across z axis")
        if cx == 0 or cy == 0 or cz == 0:
            continue
        coordinates = list(itertools.product(range(cx), range(cy), range(cz)))
        if len(inventories) > len(coordinates):
            raise ValueError(f"{fi} has too many inventories")
        for (ix, iy, iz), (label, items) in zip(coordinates, itertools.chain(inventories, itertools.repeat(("", ())))):
            if len(items) > 42:
                raise ValueError(f"{fi} has too many items in storage")
            asset_id = create_asset_id()
            while asset_id in deployed_objects_identifiers:
                asset_id = create_asset_id()
            deployed_object = deploy_facility_object(
                asset_id,
                *_STORAGE_OBJECT_DESCRIPTOR,
                sx + ix * dx,
                sy + iy * dy,
                sz + iz * dz,
                direction,
                label=label,
                paint=paint,
            )
            inventory = create_object_inventory(0)
            inventory["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"] = [
                create_empty_item() for _ in range(42 - len(items))
            ] + [create_global_item(create_asset_id(), **item) for item in items]
            deployed_object["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"] = [
                inventory,
            ]
            deployed_objects[asset_id] = deployed_object


_HAZARD_STORAGE_OBJECT_DESCRIPTOR = form_deployed_object_identifier(
    "Furniture",
    "Deployed_HazardCrate",
    0x7FFFFF00,
)


def deploy_hazard_storages(
    identifier: str,
    paint: int,
    containers: Iterable[
        tuple[
            tuple[float, float, float],
            tuple[float, float, float],
            str,
            tuple[int, int, int],
            Sequence[Sequence[dict[str, Any]]],
        ]
    ],
) -> None:
    deployed_objects = all_deployed_objects.setdefault(identifier, {})
    for fi, (start, spacing, direction, dimensions, inventories) in enumerate(containers):
        sx, sy, sz = start
        dx, dy, dz = spacing
        cx, cy, cz = dimensions
        if cx < 0:
            raise ValueError(f"{fi} has invalid x dimension {cx}")
        if dx == 0.0 and cx > 1:
            raise ValueError(f"{fi} cannot span across x axis")
        if cy < 0:
            raise ValueError(f"{fi} has invalid y dimension {cy}")
        if dy == 0.0 and cy > 1:
            raise ValueError(f"{fi} cannot span across y axis")
        if cz < 0:
            raise ValueError(f"{fi} has invalid z dimension {cz}")
        if dz == 0.0 and cz > 1:
            raise ValueError(f"{fi} cannot span across z axis")
        if cx == 0 or cy == 0 or cz == 0:
            continue
        coordinates = list(itertools.product(range(cx), range(cy), range(cz)))
        if len(inventories) > len(coordinates):
            raise ValueError(f"{fi} has too many inventories")
        for (ix, iy, iz), items in zip(coordinates, itertools.chain(inventories, itertools.repeat(()))):
            if len(items) > 30:
                raise ValueError(f"{fi} has too many items in storage")
            asset_id = create_asset_id()
            while asset_id in deployed_objects_identifiers:
                asset_id = create_asset_id()
            deployed_object = deploy_facility_object(
                asset_id,
                *_HAZARD_STORAGE_OBJECT_DESCRIPTOR,
                sx + ix * dx,
                sy + iy * dy,
                sz + iz * dz,
                direction,
                label="Radioactive",
                paint=paint,
            )
            inventory = create_object_inventory(0)
            inventory["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"] = [
                create_empty_item() for _ in range(30 - len(items))
            ] + [create_global_item(create_asset_id(), **item) for item in items]
            deployed_object["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"] = [
                inventory,
            ]
            deployed_objects[asset_id] = deployed_object


_ITEM_STAND_OBJECT_DESCRIPTOR = form_deployed_object_identifier(
    "Furniture",
    "Deployed_ItemStand_ParentBP",
    0x7FFFFF00,
)


def deploy_item_stands(
    identifier: str,
    paint: int,
    containers: Iterable[
        tuple[
            tuple[float, float, float],
            tuple[float, float],
            str,
            tuple[int, int],
            Sequence[dict[str, Any]],
        ]
    ],
) -> None:
    deployed_objects = all_deployed_objects.setdefault(identifier, {})
    for fi, (start, spacing, direction, dimensions, items) in enumerate(containers):
        sx, sy, z = start
        dx, dy = spacing
        cx, cy = dimensions
        if cx < 0:
            raise ValueError(f"{fi} has invalid x dimension {cx}")
        if dx == 0.0 and cx > 1:
            raise ValueError(f"{fi} cannot span across x axis")
        if cy < 0:
            raise ValueError(f"{fi} has invalid y dimension {cy}")
        if dy == 0.0 and cy > 1:
            raise ValueError(f"{fi} cannot span across y axis")
        if cx == 0 or cy == 0:
            continue
        coordinates = list(itertools.product(range(cx), range(cy)))
        if len(items) > len(coordinates):
            raise ValueError(f"{fi} has too many inventories")
        for (ix, iy), item in zip(coordinates, itertools.chain(items, itertools.repeat(None))):
            asset_id = create_asset_id()
            while asset_id in deployed_objects_identifiers:
                asset_id = create_asset_id()
            deployed_object = deploy_facility_object(
                asset_id,
                *_ITEM_STAND_OBJECT_DESCRIPTOR,
                sx + ix * dx,
                sy + iy * dy,
                z,
                direction,
                paint=paint,
            )
            inventory = create_object_inventory(0)
            inventory["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"] = [
                create_empty_item() if item is None else create_global_item(create_asset_id(), **item),
            ]
            deployed_object["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"] = [
                inventory,
            ]
            deployed_objects[asset_id] = deployed_object


def write_attributes(identifier: str, world: dict[str, dict[str, Any]]) -> None:
    deployed_object_map = world.get("DeployedObjectMap")
    if deployed_object_map is None:
        if identifier in all_builtin_objects or identifier in all_deployed_objects:
            raise ValueError(f"Inconsistent state for {identifier}")
    else:
        builtin_objects = all_builtin_objects.get(identifier, {})
        deployed_objects = all_deployed_objects.get(identifier, {})
        deployed_object_map["value"]["values"] = [
            [asset_id, builtin_object] for asset_id, builtin_object in builtin_objects.items()
        ] + [[asset_id.hex.upper(), deployed_object] for asset_id, deployed_object in deployed_objects.items()]

    power_socket_map = world.get("PowerSocketMap")
    if power_socket_map is None:
        if identifier in all_wall_power_sockets or identifier in all_power_sockets:
            raise ValueError(f"Inconsistent state for {identifier}")
    else:
        wall_power_sockets = all_wall_power_sockets.get(identifier, {})
        power_sockets = all_power_sockets.get(identifier, {})
        power_socket_map["value"]["values"] = [
            [socket_id, socket] for socket_id, socket in wall_power_sockets.items()
        ] + [
            [f"{asset_id.hex.upper()}{socket_index}", socket]
            for asset_id, board in power_sockets.items()
            for socket_index, socket in board.items()
        ]
