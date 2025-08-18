import struct
from typing import ClassVar, final, override

from ...utils import read_string, write_string
from ._base import GVASPropertySerde


class GVASNamePropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Name"

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[str, int]:
        value, bytes_read = read_string(data, offset)
        return value, offset + bytes_read

    @classmethod
    @final
    @override
    def from_dict(cls, data: str) -> bytes:
        return write_string(data)

    @classmethod
    @final
    @override
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[str], int]:
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
        expected_offset = offset + size
        offset += 4
        values: list[str] = []
        for _ in range(count):
            value, bytes_read = read_string(data, offset)
            offset += bytes_read
            values.append(value)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return values, offset

    @classmethod
    @final
    @override
    def from_bytes_set(cls, data: bytes, offset: int) -> tuple[list[str], int]:
        padding, size, unit_width, flag, count = struct.unpack_from("<IIBII", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 8
        values: dict[str, None] = {}
        for _ in range(count):
            value, bytes_read = read_string(data, offset)
            offset += bytes_read
            values[value] = None
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return list(values.keys()), offset

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

    @classmethod
    @override
    def from_dict_array(cls, data: list[str]) -> bytes:
        string_bytes = write_string(*data)
        return struct.pack("<IIBI", 0, len(string_bytes) + 4, 0, len(data)) + string_bytes

    @classmethod
    @final
    @override
    def from_dict_set(cls, data: list[str]) -> bytes:
        string_data = write_string(*dict.fromkeys(data).keys())
        return struct.pack("<IIBII", 0, len(string_data) + 8, 0, 0, len(dict.fromkeys(data))) + string_data
