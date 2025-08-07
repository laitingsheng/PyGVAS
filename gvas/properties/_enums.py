import struct
from typing import ClassVar, Self, final, override

from ..utils import read_string
from ..values import GVASEnumValue
from ._base import GVASProperty


def _parse_header(data: bytes, offset: int) -> tuple[type[GVASEnumValue], int]:
    category = struct.unpack_from("<L", data, offset)[0]
    if category != 2:
        raise ValueError(f"Invalid category at {offset}")
    offset += 4
    name, bytes_read = read_string(data, offset)
    if not name:
        raise ValueError(f"Invalid name at {offset}")
    offset += bytes_read
    index = struct.unpack_from("<L", data, offset)[0]
    if index != 1:
        raise ValueError(f"Invalid index at {offset}")
    offset += 4
    blueprint, bytes_read = read_string(data, offset)
    if not blueprint:
        raise ValueError(f"Invalid blueprint at {offset}")
    offset += bytes_read
    value_class = GVASEnumValue.get_class(blueprint, name)
    if struct.unpack_from("<L", data, offset)[0] != 0:
        raise ValueError(f"Invalid flag at {offset}")
    return value_class, offset + 4


class GVASEnumProperty(GVASProperty):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "EnumProperty"

    _value: GVASEnumValue

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        value_class, offset = _parse_header(data, offset)
        self = cls.__new__(cls)
        self._value, offset = value_class.parse(data, offset)
        return self, offset
