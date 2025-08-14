import json
import struct
import sys

from gvas.properties import GVASBlueprintStructProperty

from ._headers import ABFCommonSaveHeader, ABFPlayerSaveHeader, ABFWorldSaveHeader

entry, mode, filename = sys.argv
save_header_class = {"player": ABFPlayerSaveHeader, "world": ABFWorldSaveHeader, "common": ABFCommonSaveHeader}[mode]
with open(filename, "rb") as f:
    data = f.read()
header, offset = save_header_class.parse(data, 0)
bodysize = getattr(header, "bodysize", None)
if bodysize is None:
    expected_offset = None
elif bodysize >= 4:
    expected_offset = offset + bodysize
else:
    raise ValueError(f"Invalid body size at {offset}")
body, offset = GVASBlueprintStructProperty.parse(data, offset)
if struct.unpack_from("<I", data, offset)[0] != 0:
    raise ValueError(f"Invalid ending at {offset}")
if expected_offset is not None and offset + 4 != expected_offset:
    raise ValueError(f"Invalid offset {offset}")
with open(f"{filename}.json", "w", encoding="utf-8") as f:
    json.dump({"header": header.to_json(), "body": body.to_json()}, f, indent=2)
