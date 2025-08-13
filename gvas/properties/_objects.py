import struct
from typing import ClassVar, Self, final, override

from ..utils import read_string
from ._base import GVASProperty
from ._strs import GVASStrProperty


class GVASObjectProperty(GVASStrProperty):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Object"


class GVASSoftObjectProperty(GVASProperty):
    __slots__ = ("_blueprint", "_reference")

    _TYPE: ClassVar[str] = "SoftObject"

    _blueprint: str
    _reference: str

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        self = cls.__new__(cls)
        self._blueprint, bytes_read = read_string(data, offset)
        offset += bytes_read
        self._reference, bytes_read = read_string(data, offset)
        offset += bytes_read
        if struct.unpack_from("<I", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at {offset}")
        return self, offset + 4

    @final
    @override
    def to_json(self) -> dict[str, str]:
        return {"blueprint": self._blueprint, "reference": self._reference}
