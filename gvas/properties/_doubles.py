import struct
from typing import ClassVar, final, override

from ._base import GVASPropertySerde


class GVASDoublePropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Double"

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[float, int]:
        return struct.unpack_from("<d", data, offset)[0], offset + 8

    @classmethod
    @final
    @override
    def from_json(cls, data: float) -> bytes:
        return struct.pack("<d", data)

    @classmethod
    @final
    @override
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[float], int]:
        padding, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        if count * 8 + 4 != size:
            raise ValueError(f"Invalid count at {offset}")
        offset += 4
        return list(struct.unpack_from(f"<{count}d", data, offset)), offset + count * 8

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[float, int]:
        category, size, unit_width, value = struct.unpack_from("<IIBd", data, offset)
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
    def from_json_full(cls, data: float) -> bytes:
        return struct.pack("<IIBd", 0, 8, 0, data)

    @classmethod
    @final
    @override
    def from_json_array(cls, data: list[float]) -> bytes:
        return struct.pack(f"<IIBI{len(data)}d", 0, len(data) * 8 + 4, 0, len(data), *data)
