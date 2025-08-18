from typing import Any
from uuid import UUID

from .._objects import get_object_asset_id


TARGET_IDENTIFIER = "Facility"

all_builtin_objects: dict[str, dict[str, dict[str, dict[str, Any]]]] = {}
builtin_objects_identifiers: dict[str, str] = {}
all_deployed_objects: dict[str, dict[UUID, dict[str, dict[str, Any]]]] = {}
deployed_objects_identifiers: dict[UUID, str] = {}


def preprocess_objects(identifier: str, world: dict[str, dict[str, Any]]) -> None:
    deployed_object_map = world.get("DeployedObjectMap")
    if deployed_object_map is not None:
        if identifier in all_builtin_objects or identifier in all_deployed_objects:
            raise ValueError(f"Duplicate world identifier {identifier}")
        builtin_objects = all_builtin_objects[identifier] = {}
        deployed_objects = all_deployed_objects[identifier] = {}
        for asset_id, deployed_object in deployed_object_map["value"]["values"]:
            parsed_asset_id = get_object_asset_id(deployed_object)
            if parsed_asset_id is None:
                if asset_id in builtin_objects_identifiers:
                    raise ValueError(f"Duplicate built-in object ID {asset_id}")
                builtin_objects[asset_id] = deployed_object
                builtin_objects_identifiers[asset_id] = identifier
                continue
            if asset_id != parsed_asset_id.hex.upper():
                raise ValueError(f"Inconsistent asset ID in deployed object {asset_id}")
            if parsed_asset_id in deployed_objects_identifiers:
                raise ValueError(f"Duplicate deployed object ID {asset_id}")
            deployed_objects[parsed_asset_id] = deployed_object
            deployed_objects_identifiers[parsed_asset_id] = identifier


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
