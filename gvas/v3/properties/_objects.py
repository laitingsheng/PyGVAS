import struct
from typing import ClassVar, final, override

from ...utils import read_string, write_string
from ._base import GVASPropertySerde


class GVASObjectPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Object"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[str, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        value, bytes_read = read_string(data, offset)
        offset += bytes_read
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return value, offset

    @classmethod
    @final
    @override
    def from_dict_full(cls, data: str) -> bytes:
        string_bytes = write_string(data)
        return struct.pack("<IIB", 0, len(string_bytes), 0) + string_bytes
