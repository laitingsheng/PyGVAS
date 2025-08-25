import os
import re
import struct
import sys
from pathlib import Path
from typing import Any

from gvas.v3.properties import GVASBlueprintStructPropertySerde

from .._headers import ABFWorldHeaderSerde


__all__ = []

entry, profile, name = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

world_save_regex = re.compile(r"WorldSave_(\w+)\.sav")
saves = dict[str, tuple[dict[str, Any], dict[str, Any]]]()

socket_id_regex = re.compile(r"([0-9A-F]{32})(\d+)")

reroutes = list[str]()

all_deployed_objects = dict[str, dict[str, dict[str, Any]]]()
deployed_objects_locations = dict[str, str]()
all_wall_power_sockets = dict[str, dict[str, dict[str, Any]]]()
wall_power_sockets_locations = dict[str, str]()
all_power_sockets = dict[str, dict[str, dict[int, dict[str, Any]]]]()
power_sockets_locations = dict[str, str]()
for save_file in save_folder.glob("WorldSave_*.sav"):
    matches = world_save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid save file name {save_file.name}")
    identifier = matches[1]
    if identifier == "MetaData":
        continue
    if identifier in saves:
        raise ValueError(f"Duplicate save identifier {identifier}")
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
    saves[identifier] = header, body
    deployed_object_map = body.get("DeployedObjectMap")
    if deployed_object_map is not None:
        deployed_objects = all_deployed_objects.setdefault(identifier, {})
        for asset_id, deployed_object in deployed_object_map["value"]["values"]:
            if asset_id in deployed_objects_locations:
                raise ValueError(f"Duplicate asset ID {asset_id}")
            if deployed_object["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]["reference"].lower() == "deployed_cablereroute_c":
                reroutes.append(asset_id)
            deployed_objects_locations[asset_id] = identifier
            deployed_objects[asset_id] = deployed_object
    power_socket_map = body.get("PowerSocketMap")
    if power_socket_map is not None:
        wall_power_sockets = all_wall_power_sockets.setdefault(identifier, {})
        power_sockets = all_power_sockets.setdefault(identifier, {})
        for socket_id, socket in power_socket_map["value"]["values"]:
            if socket_id.startswith("/Game/Maps/"):
                if socket_id in wall_power_sockets_locations:
                    raise ValueError(f"Duplicate wall power socket {socket_id}")
                wall_power_sockets_locations[socket_id] = identifier
                wall_power_sockets[socket_id] = socket
                continue
            matches = socket_id_regex.match(socket_id)
            if matches is None:
                raise ValueError(f"Invalid power socket ID {socket_id}")
            asset_id = matches[1]
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

connections = dict[str, tuple[str, int]]()
for identifier, power_sockets in all_power_sockets.items():
    orphaned_sockets = list[str]()
    for socket_id, board in power_sockets.items():
        if socket_id not in deployed_objects_locations:
            orphaned_sockets.append(socket_id)
            continue
        for socket_index, socket in board.items():
            device = socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"]
            if device == "-1":
                continue
            if device not in deployed_objects_locations:
                socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"] = "-1"
                continue
            if device in connections:
                raise ValueError(f"Duplicate connection for device {device}")
            connections[device] = socket_id, socket_index
    for socket_id in orphaned_sockets:
        del power_sockets_locations[socket_id]
        del power_sockets[socket_id]

for asset_id in reroutes:
    identifier = deployed_objects_locations.pop(asset_id)
    del all_deployed_objects[identifier][asset_id]
    if power_sockets_locations.pop(asset_id) != identifier:
        raise ValueError(f"Inconsistent power socket board {asset_id}")
    board = all_power_sockets[identifier].pop(asset_id)
    if len(board) != 1:
        raise ValueError(f"Reroute {asset_id} has multiple sockets")
    socket_index, socket = board.popitem()
    if socket_index != 1:
        raise ValueError(f"Reroute {asset_id} has incorrect socket index")
    source_id, source_index = connections.pop(asset_id)
    device = socket["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"]
    all_power_sockets[power_sockets_locations[source_id]][source_id][source_index]["PluggedInDeviceAssetID_20_EDF3C1474C00B1AC29424D8B05460265"]["value"] = device
    if device != "-1":
        connections[device] = source_id, source_index

for identifier, (header, body) in saves.items():
    updated = False
    deployed_objects = all_deployed_objects.pop(identifier, None)
    if deployed_objects is not None:
        deployed_object_map = body["DeployedObjectMap"]
        if len(deployed_objects) != len(deployed_object_map["value"]["values"]):
            updated = True
            deployed_object_map["value"]["values"] = list(map(list, deployed_objects.items()))
    power_sockets = all_power_sockets.pop(identifier, None)
    if power_sockets is not None:
        unfolded_power_sockets = list(map(list, all_wall_power_sockets.pop(identifier, {}).items()))
        unfolded_power_sockets.extend(
            [f"{asset_id}{socket_index}", socket]
            for asset_id, board in power_sockets.items()
            for socket_index, socket in board.items()
        )
        power_socket_map = body["PowerSocketMap"]
        if len(unfolded_power_sockets) != len(power_socket_map["value"]["values"]):
            updated = True
            power_socket_map["value"]["values"] = unfolded_power_sockets
    if updated:
        body = GVASBlueprintStructPropertySerde.from_json(body) + struct.pack("<I", 0)
        header["bodysize"] = len(body)
        header = ABFWorldHeaderSerde.from_json(header)
        with (output_folder / f"WorldSave_{identifier}.sav").open("wb") as f:
            f.write(header)
            f.write(body)
