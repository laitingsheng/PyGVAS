from __future__ import annotations

import struct
from typing import Any, ClassVar, override

from ...utils import read_string
from ._base import GVASPropertySerde


_REGISTRY: dict[str, type[GVASEnumPropertySerde]] = {}


class GVASEnumPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _SUBTYPE: ClassVar[str]
    _TYPE: ClassVar[str] = "EnumProperty"

    @override
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "_SUBTYPE"):
            raise ValueError(f"{cls.__name__} does not have a subtype")
        if cls._SUBTYPE in _REGISTRY:
            raise ValueError(f"{cls.__name__} has duplicate subtype {cls._SUBTYPE}")
        _REGISTRY[cls._SUBTYPE] = cls

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[str, int]:
        value, bytes_read = read_string(data, offset)
        if not value.startswith(f"{cls._SUBTYPE}::"):
            raise ValueError(f"Invalid name at {offset}")
        return value[len(cls._SUBTYPE) + 2 :], offset + bytes_read

    @classmethod
    @override
    def _header_to_dict(cls) -> dict[str, str]:
        return {"subtype": cls._SUBTYPE}

    @classmethod
    @override
    def _key_from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        value, bytes_read = read_string(data, offset)
        return value, offset + bytes_read

    @classmethod
    def _header_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASPropertySerde], int]:
        property_subtype, bytes_read = read_string(data, offset)
        offset += bytes_read
        flag = struct.unpack_from("<B", data, offset)[0]
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        property_serde = _REGISTRY.get(property_subtype)
        if property_serde is None:
            property_serde = type(
                f"GVAS{cls._TYPE}PropertySerde@{property_subtype}",
                (GVASEnumPropertySerde,),
                {"__slots__": (), "_SUBTYPE": property_subtype},
            )
        return property_serde, offset + 1
