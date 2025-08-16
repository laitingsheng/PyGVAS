import struct
from typing import Any, final, override

from gvas.headers import GVASHeaderSerde


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
    def from_json(cls, data: dict[str, Any]) -> bytes:
        return super().from_json(data) + struct.pack("<B", 0)
