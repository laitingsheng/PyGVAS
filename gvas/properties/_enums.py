from __future__ import annotations

import struct
from typing import ClassVar, Self, final, override

from ..utils import read_string
from ._base import GVASProperty

_REGISTRY: dict[str, type[GVASEnumProperty]] = {}


class GVASEnumProperty(GVASProperty):
    __slots__ = ("_value",)

    _BLUEPRINT: ClassVar[str]
    _NAME: ClassVar[str]
    _TYPE: ClassVar[str] = "Enum"

    _value: str

    @override
    def __init_subclass__(cls) -> None:
        if not cls._BLUEPRINT:
            raise ValueError(f"{cls.__name__} does not have a blueprint")
        if not cls._NAME:
            raise ValueError(f"{cls.__name__} does not have a name")
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in _REGISTRY:
            raise ValueError(f"Duplicate enum property {cls._NAME} in {cls._BLUEPRINT}")
        _REGISTRY[fullpath] = cls

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        value, bytes_read = read_string(data, offset)
        if not value.startswith(f"{cls._NAME}::"):
            raise ValueError(f"Invalid name at {offset}")
        self = cls.__new__(cls)
        self._value = value[len(cls._NAME) + 2 :]
        return self, offset + bytes_read

    @classmethod
    @final
    @override
    def type_json(cls) -> dict[str, str]:
        return super().type_json() | {"blueprint": cls._BLUEPRINT, "name": cls._NAME}

    @classmethod
    @final
    @override
    def _concrete_type(cls, data: bytes, offset: int) -> tuple[type[GVASEnumProperty], int]:
        if struct.unpack_from("<I", data, offset)[0] != 2:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        name, bytes_read = read_string(data, offset)
        if not name:
            raise ValueError(f"Invalid name at {offset}")
        offset += bytes_read
        index = struct.unpack_from("<I", data, offset)[0]
        if index != 1:
            raise ValueError(f"Invalid index at {offset}")
        offset += 4
        blueprint, bytes_read = read_string(data, offset)
        if not blueprint:
            raise ValueError(f"Invalid blueprint at {offset}")
        offset += bytes_read
        if struct.unpack_from("<I", data, offset)[0] != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 4
        type_name, bytes_read = read_string(data, offset)
        if type_name != "ByteProperty":
            raise ValueError(f"Invalid type at {offset}")
        return _REGISTRY[f"{blueprint}/{name}"], offset + bytes_read

    @final
    @override
    def to_json(self) -> str:
        return self._value
