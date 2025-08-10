import struct
from typing import Any, ClassVar, Self, final, override

from ._base import GVASProperty, GVASPropertyArray


class GVASFloatProperty(GVASProperty):
    __slots__ = ("_value",)

    _ACCEPT: ClassVar[str] = "FloatProperty"

    _value: float

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
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
    def to_json(self) -> dict[str, Any]:
        return {"type": self._ACCEPT, "value": self._value}


class GVASFloatPropertyArray(GVASPropertyArray):
    __slots__ = ("_value",)

    _ACCEPT: ClassVar[str] = "FloatProperty"

    _value: list[float]

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != count * 4 + 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 5
        self = cls.__new__(cls)
        self._value = list(struct.unpack_from(f"<{count}f", data, offset))
        return self, offset + count * 4

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return {"type": self._ACCEPT, "value": self._value}
