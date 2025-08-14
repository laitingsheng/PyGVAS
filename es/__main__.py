import json
import struct
import sys

from gvas.properties import GVASBlueprintStructProperty

from ._headers import ESSaveHeader

entry, filename = sys.argv
with open(filename, "rb") as f:
    data = f.read()
header, offset = ESSaveHeader.parse(data, 0)
body, offset = GVASBlueprintStructProperty.parse(data, offset)
if struct.unpack_from("<I", data, offset)[0] != 0:
    raise ValueError(f"Invalid padding at {offset}")
with open(f"{filename}.json", "w", encoding="utf-8") as f:
    json.dump({"header": header.to_json(), "body": body.to_json()}, f, indent=2)
