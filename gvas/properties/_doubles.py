import struct
from typing import ClassVar, Self, Sequence, final, override

from ._base import GVASProperty


class GVASDoubleProperty(GVASProperty):
    __slots__ = ("_value",)

    _TYPE: ClassVar[str] = "Double"

    _value: float

    @classmethod
    @final
    @override
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self = cls.__new__(cls)
        self._value = struct.unpack_from("<d", data, offset)[0]
        return self, offset + 8

    @classmethod
    @final
    @override
    def parse_array(cls, data: bytes, offset: int) -> tuple[Sequence[Self], int]:
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
        if count * 8 + 4 != size:
            raise ValueError(f"Invalid count at {offset}")
        offset += 4
        selfs: list[Self] = []
        for value in struct.unpack_from(f"<{count}d", data, offset):
            self = cls.__new__(cls)
            self._value = value
            selfs.append(self)
        return selfs, offset + count * 8

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, value = struct.unpack_from("<IIBd", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._value = value
        return self, offset + 9

    @final
    @override
    def to_json(self) -> float:
        return self._value
