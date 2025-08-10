import json
import sys

from . import ABFPlayerSaveHeader, ABFWorldSaveHeader
from gvas.values import GVASCustomStructValue

entry, mode, filename = sys.argv

if mode == "player":
    save_header_class = ABFPlayerSaveHeader
elif mode == "world":
    save_header_class = ABFWorldSaveHeader
else:
    raise ValueError(f"Unknown mode: {mode}")

with open(filename, "rb") as f:
    data = f.read()

header, offset = save_header_class.parse(data, 0)
expected_offset = offset + header.size
body, offset = GVASCustomStructValue.parse(0, data, offset)
if offset + 4 != expected_offset:
    raise ValueError(f"Invalid offset at {offset}")
offset += 4

with open(f"{filename}.json", "w", encoding="utf-8") as f:
    json.dump({"header": header.to_json(), "body": body.to_json()}, f, indent=2)
