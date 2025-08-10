import struct
from typing import Any, ClassVar, Self, final, override

from ..values._base import GVASTextValue
from ._base import GVASProperty


class GVASTextProperty(GVASProperty):
    __slots__ = ("_value",)

    _ACCEPT: ClassVar[str] = "TextProperty"

    _value: GVASTextValue

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, flag, type_id = struct.unpack_from("<IIBIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 5:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 5
        value_class = GVASTextValue.get_class(type_id)
        self = cls.__new__(cls)
        self._value, offset = value_class.parse(data, offset)
        if offset != expected_offset:
            raise ValueError(f"Text size mismatch at {offset}")
        return self, offset

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return {"type": self._ACCEPT, "value": self._value.to_json()}
