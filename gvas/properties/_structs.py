import struct
from typing import ClassVar, Self, Sequence, final, override

from ..utils import read_string
from ..values import GVASStructValue
from ._base import GVASProperty, GVASPropertyArray


def _parse_header(data: bytes, offset: int) -> tuple[type[GVASStructValue], int]:
    category = struct.unpack_from("<L", data, offset)[0]
    if category == 1:
        singleton = True
    elif category == 2:
        singleton = False
    else:
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
    if singleton:
        guid = ""
    else:
        index = struct.unpack_from("<L", data, offset)[0]
        if index != 0:
            raise ValueError(f"Invalid index at {offset}")
        offset += 4
        guid, bytes_read = read_string(data, offset)
        if not guid:
            raise ValueError(f"Invalid guid at {offset}")
        offset += bytes_read
    value_class = GVASStructValue.get_class(blueprint, name)
    if not value_class.match_guid(guid):
        raise ValueError(f"Invalid guid at {offset}")
    return value_class, offset


class GVASStructProperty(GVASProperty):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "StructProperty"

    _value: GVASStructValue

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        value_class, offset = _parse_header(data, offset)
        flag, size, unit_width = struct.unpack_from("<LLB", data, offset)
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 9
        expected_offset = offset + size
        self = cls.__new__(cls)
        self._value, offset = value_class.parse(unit_width, data, offset)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset at {offset}")
        return self, offset


class GVASStructPropertyArray(GVASPropertyArray):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "StructProperty"

    _value: Sequence[GVASStructValue]

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        value_class, offset = _parse_header(data, offset)
        flag, size, unit_width = struct.unpack_from("<LLB", data, offset)
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 9
        expected_offset = offset + size
        self = cls.__new__(cls)
        self._value, offset = value_class.parse_many(unit_width, data, offset)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset at {offset}")
        return self, offset
