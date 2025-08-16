import struct
from typing import ClassVar, final, override

from ._base import GVASPropertySerde


class GVASIntPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Int"

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[int, int]:
        return struct.unpack_from("<i", data, offset)[0], offset + 4

    @classmethod
    @final
    @override
    def from_json(cls, data: int) -> bytes:
        return struct.pack("<i", data)

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[int, int]:
        category, size, unit_width, value = struct.unpack_from("<IIBi", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        return value, offset + 5

    @classmethod
    @final
    @override
    def from_json_full(cls, data: int) -> bytes:
        return struct.pack("<IIBi", 0, 4, 0, data)
