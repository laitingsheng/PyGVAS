import struct
from typing import Any, ClassVar, Self, Sequence, final, override

from ._base import GVASProperty


class GVASSetProperty(GVASProperty):
    __slots__ = ("_element_type", "_values")

    _TYPE: ClassVar[str] = "Set"

    _element_type: type[GVASProperty]
    _values: Sequence[GVASProperty]

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        if struct.unpack_from("<I", data, offset)[0] != 1:
            raise ValueError(f"Invalid category at {offset}")
        self = cls.__new__(cls)
        self._element_type, offset = GVASProperty.parse_type(data, offset + 4)
        self._values, offset = self._element_type.parse_set(data, offset)
        return self, offset

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return {"element_type": self._element_type.type_json(), "values": [value.to_json() for value in self._values]}
