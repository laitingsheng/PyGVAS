from __future__ import annotations

import struct
from typing import Any, ClassVar, override

from ...utils import read_string
from ._base import GVASPropertySerde
from ._structs import GVASStructPropertySerde


_REGISTRY: dict[str, type[GVASArrayPropertySerde]] = {}


class GVASArrayPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _ELEMENT_TYPE: ClassVar[str]
    _TYPE: ClassVar[str] = "ArrayProperty"

    @override
    def __init_subclass__(cls) -> None:
        if not cls._ELEMENT_TYPE:
            raise ValueError(f"{cls.__name__} does not have an element type")
        if cls._ELEMENT_TYPE in _REGISTRY:
            raise ValueError(f"{cls.__name__} has duplicate element type {cls._ELEMENT_TYPE}")
        if f"GVAS{cls._ELEMENT_TYPE}ArraySerde" != cls.__name__:
            raise ValueError(f"{cls.__name__} does not match element type {cls._ELEMENT_TYPE}")
        _REGISTRY[cls._ELEMENT_TYPE] = cls

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        count = struct.unpack_from("<I", data, offset)[0]
        values, offset = GVASPropertySerde.get_type(cls._ELEMENT_TYPE)._multiple_from_bytes(data, offset + 4, count)
        return {"values": values}, offset

    @classmethod
    @override
    def _header_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASArrayPropertySerde], int]:
        element_type, bytes_read = read_string(data, offset)
        offset += bytes_read
        flag = struct.unpack_from("<B", data, offset)[0]
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        element_serde = _REGISTRY.get(element_type)
        if element_serde is None:
            element_serde = type(
                f"GVAS{element_type}ArraySerde",
                (GVASArrayPropertySerde,),
                {"__slots__": (), "_ELEMENT_TYPE": element_type},
            )
        return element_serde, offset + 1

    @classmethod
    @override
    def _header_to_dict(cls) -> dict[str, str]:
        return {"element_type": cls._ELEMENT_TYPE}


class GVASStructPropertyArraySerde(GVASArrayPropertySerde):
    __slots__ = ()

    _ELEMENT_TYPE: ClassVar[str] = "StructProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        count = struct.unpack_from("<I", data, offset)[0]
        offset += 4
        name, bytes_read = read_string(data, offset)
        element_serde, size, offset = GVASStructPropertySerde.header_from_bytes(data, offset + bytes_read)
        start = offset
        expected_offset = offset + size
        values, offset = element_serde._multiple_from_bytes(data, offset, count)
        if offset != expected_offset:
            raise ValueError(f"{cls._ELEMENT_TYPE} in [{start}, {offset - 1}] expected ending at {expected_offset}")
        return element_serde.header_to_dict() | {"name": name, "values": values}, offset
