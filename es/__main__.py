import struct
import sys
from pathlib import Path
from typing import Any, final, override

from gvas import GVASSave
from gvas.v3.headers import GVASHeaderSerde
from gvas.v3.properties import GVASBlueprintStructPropertySerde


class ESHeaderSerde(GVASHeaderSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        result, offset = super().from_bytes(data, offset)
        if struct.unpack_from("<B", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at {offset}")
        return result, offset + 1

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        return super().from_dict(data) + struct.pack("<B", 0)


class ESSave(GVASSave):
    __slots__ = ()

    _BODY_SERDE = GVASBlueprintStructPropertySerde
    _HEADER_SERDE = ESHeaderSerde


entry, filename = sys.argv
filepath = Path(filename).absolute()
exporting = {".sav": True, ".json": False}[filepath.suffix]
if exporting:
    ESSave.from_binary_file(filepath).to_json_file(filepath.with_suffix(".json"))
else:
    ESSave.from_json_file(filepath).to_binary_file(filepath.with_suffix(".sav.new"))
