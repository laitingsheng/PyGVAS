import struct
from typing import ClassVar, Self, final, override

from ._base import GVASProperty, GVASPropertyArray


class GVASArrayProperty(GVASProperty):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "ArrayProperty"

    _value: GVASPropertyArray

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        if struct.unpack_from("<L", data, offset)[0] != 1:
            raise ValueError(f"Unexpected array flag at {offset}")
        property_class, offset = GVASPropertyArray.parse_type(data, offset + 4)
        self = cls.__new__(cls)
        self._value, offset = property_class.parse(data, offset)
        return self, offset
