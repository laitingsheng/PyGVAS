import struct
from typing import ClassVar, Self, final, override

from ..utils import read_string
from ._base import GVASProperty, GVASPropertyArray


class GVASStrProperty(GVASProperty):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "StrProperty"

    _value: str

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<LLB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        self = cls.__new__(cls)
        self._value, bytes_read = read_string(data, offset)
        if bytes_read != size:
            raise ValueError(f"Invalid string at {offset}")
        return self, offset + bytes_read


class GVASStrPropertyArray(GVASPropertyArray):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "StrProperty"

    _value: list[str]

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, count = struct.unpack_from("<LLBL", data, offset)
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
        offset += 4
        self = cls.__new__(cls)
        self._value = []
        for _ in range(count):
            value, bytes_read = read_string(data, offset)
            self._value.append(value)
            offset += bytes_read
        if offset != expected_offset:
            raise ValueError(f"Invalid string array at {offset}")
        return self, offset
