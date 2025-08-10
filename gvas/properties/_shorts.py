import struct
from typing import Any, ClassVar, Self, final, override

from ._base import GVASProperty, GVASPropertyArray


class GVASShortProperty(GVASProperty):
    __slots__ = ("_value",)

    _ACCEPT: ClassVar[str] = "ShortProperty"

    _value: int

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, value = struct.unpack_from("<IIBh", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 2:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._value = value
        return self, offset + 3

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return {"type": self._ACCEPT, "value": self._value}


class GVASShortPropertyArray(GVASPropertyArray):
    __slots__ = ("_value",)

    _ACCEPT: ClassVar[str] = "ShortProperty"

    _value: list[int]

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != count * 2 + 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 5
        self = cls.__new__(cls)
        self._value = list(struct.unpack_from(f"<{count}h", data, offset))
        return self, offset + count * 2

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return {"type": self._ACCEPT, "value": self._value}
