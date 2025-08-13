import struct
from typing import ClassVar, Self, final, override

from ._base import GVASProperty


class GVASFloatProperty(GVASProperty):
    __slots__ = ("_value",)

    _TYPE: ClassVar[str] = "Float"

    _value: float

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, value = struct.unpack_from("<IIBf", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._value = value
        return self, offset + 5

    @final
    @override
    def to_json(self) -> float:
        return self._value
