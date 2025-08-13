import struct
from typing import ClassVar, Self, final, override

from ._base import GVASProperty


class GVASBoolProperty(GVASProperty):
    __slots__ = ("_value",)

    _TYPE: ClassVar[str] = "Bool"

    _value: bool

    @classmethod
    @final
    @override
    def parse_array(cls, data: bytes, offset: int) -> tuple[list[Self], int]:
        padding, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        if count + 4 != size:
            raise ValueError(f"Invalid count at {offset}")
        offset += 4
        selfs: list[Self] = []
        for value in struct.unpack_from(f"<{count}B", data, offset):
            self = cls.__new__(cls)
            if value == 0:
                self._value = False
            elif value == 0x1:
                self._value = True
            else:
                raise ValueError(f"Invalid value at {offset}")
            selfs.append(self)
        return selfs, offset + count

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, value = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 0:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        instance = cls.__new__(cls)
        if value == 0:
            instance._value = False
        elif value == 0x10:
            instance._value = True
        else:
            raise ValueError(f"Invalid value at {offset}")
        return instance, offset + 1

    @final
    @override
    def to_json(self) -> bool:
        return self._value
