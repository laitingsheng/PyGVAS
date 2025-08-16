import json
import struct
import sys
from pathlib import Path

from gvas.properties import GVASBlueprintStructPropertySerde

from ._headers import ESHeaderSerde


entry, filename = sys.argv
filepath = Path(filename).absolute()
exporting = {".sav": True, ".json": False}[filepath.suffix]
if exporting:
    with filepath.open("rb") as f:
        data = f.read()
    header, offset = ESHeaderSerde.from_bytes(data, 0)
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
    with filepath.with_suffix(".json").open("w", encoding="utf-8") as f:
        json.dump({"header": header, "body": body}, f, indent=2)
else:
    with filepath.open("r", encoding="utf-8") as f:
        data = json.load(f)
    body = GVASBlueprintStructPropertySerde.from_json(data["body"]) + struct.pack("<I", 0)
    data["header"]["bodysize"] = len(body)
    header = ESHeaderSerde.from_json(data["header"])
    with filepath.with_suffix(".new.sav").open("wb") as f:
        f.write(header)
        f.write(body)
