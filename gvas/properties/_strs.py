import struct
from typing import ClassVar, Self, final, override

from ..utils import read_string
from ._base import GVASProperty


class GVASStrProperty(GVASProperty):
    __slots__ = ("_value",)

    _TYPE: ClassVar[str] = "Str"

    _value: str

    @classmethod
    @final
    @override
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self = cls.__new__(cls)
        self._value, bytes_read = read_string(data, offset)
        return self, offset + bytes_read

    @classmethod
    @final
    @override
    def parse_array(cls, data: bytes, offset: int) -> tuple[list[Self], int]:
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
        selfs: list[Self] = []
        for _ in range(count):
            self, offset = cls.parse(data, offset)
            selfs.append(self)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return selfs, offset

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
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
        self, offset = cls.parse(data, offset)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return self, offset

    @classmethod
    @final
    @override
    def parse_set(cls, data: bytes, offset: int) -> tuple[list[Self], int]:
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
        selfs: list[Self] = []
        for _ in range(count):
            self, offset = cls.parse(data, offset)
            selfs.append(self)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return selfs, offset

    @final
    @override
    def to_json(self) -> str:
        return self._value
