from __future__ import annotations

import struct
from typing import ClassVar, final, override

from ...utils import read_string, write_string
from ._base import GVASPropertySerde


_REGISTRY: dict[str, type[GVASBytePropertySerde]] = {}


class GVASBytePropertySerde(GVASPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str]
    _NAME: ClassVar[str]
    _TYPE: ClassVar[str] = "Byte"

    @override
    def __init_subclass__(cls) -> None:
        if not cls._BLUEPRINT:
            raise ValueError(f"{cls.__name__} does not have a blueprint")
        if not cls._NAME:
            raise ValueError(f"{cls.__name__} does not have a name")
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in _REGISTRY:
            raise ValueError(f"Duplicate byte property {cls._NAME} in {cls._BLUEPRINT}")
        _REGISTRY[fullpath] = cls

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[str, int]:
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
        if bytes_read != size:
            raise ValueError(f"Invalid size at {offset}")
        if not value.startswith(f"{cls._NAME}::"):
            raise ValueError(f"Invalid name at {offset}")
        return value[len(cls._NAME) + 2 :], offset + bytes_read

    @classmethod
    @final
    @override
    def from_dict_full(cls, data: str) -> bytes:
        string_bytes = write_string(f"{cls._NAME}::{data}")
        return struct.pack("<IIB", 0, len(string_bytes), 0) + string_bytes

    @classmethod
    @final
    @override
    def type_to_dict(cls) -> dict[str, str]:
        return super().type_to_dict() | {"blueprint": cls._BLUEPRINT, "name": cls._NAME}

    @classmethod
    @final
    @override
    def _concrete_type_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASBytePropertySerde], int]:
        if struct.unpack_from("<I", data, offset)[0] != 1:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        name, bytes_read = read_string(data, offset)
        if not name:
            raise ValueError(f"Invalid name at {offset}")
        offset += bytes_read
        if struct.unpack_from("<I", data, offset)[0] != 1:
            raise ValueError(f"Invalid index at {offset}")
        offset += 4
        blueprint, bytes_read = read_string(data, offset)
        if not blueprint:
            raise ValueError(f"Invalid blueprint at {offset}")
        offset += bytes_read
        fullpath = f"{blueprint}/{name}"
        concrete_class = _REGISTRY.get(fullpath)
        if concrete_class is None:
            concrete_class = type(
                f"GVASBytePropertySerde@{fullpath}",
                (GVASBytePropertySerde,),
                {"__slots__": (), "_BLUEPRINT": blueprint, "_NAME": name},
            )
            _REGISTRY[fullpath] = concrete_class
        return concrete_class, offset

    @classmethod
    @final
    @override
    def _concrete_type_from_dict(cls, data: dict[str, str]) -> type[GVASBytePropertySerde]:
        blueprint = data["blueprint"]
        name = data["name"]
        fullpath = f"{blueprint}/{name}"
        concrete_class = _REGISTRY.get(fullpath)
        if concrete_class is None:
            concrete_class = type(
                f"GVASBytePropertySerde@{fullpath}",
                (GVASBytePropertySerde,),
                {"__slots__": (), "_BLUEPRINT": blueprint, "_NAME": name},
            )
            _REGISTRY[fullpath] = concrete_class
        return concrete_class

    @classmethod
    @final
    @override
    def type_to_bytes(cls) -> bytes:
        return (
            super().type_to_bytes()
            + struct.pack("<I", 1)
            + write_string(cls._NAME)
            + struct.pack("<I", 1)
            + write_string(cls._BLUEPRINT)
        )
