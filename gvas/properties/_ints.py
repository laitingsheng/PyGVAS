import struct
from typing import ClassVar, Self, final, override

from ._base import GVASProperty


class GVASIntProperty(GVASProperty):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "IntProperty"

    _value: int

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, value = struct.unpack_from("<LLBl", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        self = cls.__new__(cls)
        self._value = value
        return self, offset + 4
