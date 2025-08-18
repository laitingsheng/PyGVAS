import struct
from typing import ClassVar, final, override

from ._base import GVASPropertySerde


class GVASInt64PropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Int64"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[int, int]:
        category, size, unit_width, value = struct.unpack_from("<IIBq", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        return value, offset + 9

    @classmethod
    @final
    @override
    def from_json_full(cls, data: int) -> bytes:
        return struct.pack("<IIBq", 0, 8, 0, data)
