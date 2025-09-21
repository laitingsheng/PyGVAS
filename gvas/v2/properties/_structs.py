from __future__ import annotations

import struct
import uuid
from typing import Any, ClassVar, override

from ...utils import read_string
from ._base import GVASPropertySerde


_REGISTRY: dict[str, type[GVASStructPropertySerde]] = {}


class GVASStructPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _SUBTYPE: ClassVar[str]
    _TYPE: ClassVar[str] = "StructProperty"

    @override
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "_SUBTYPE"):
            raise ValueError(f"{cls.__name__} does not have a subtype")
        if cls._SUBTYPE in _REGISTRY:
            raise ValueError(f"{cls.__name__} has duplicate subtype {cls._SUBTYPE}")
        _REGISTRY[cls._SUBTYPE] = cls

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        result: dict[str, dict[str, Any]] = {}
        name, bytes_read = read_string(data, offset)
        while name != "None":
            start = offset
            property_type, size, offset = GVASPropertySerde.header_from_bytes(data, offset + bytes_read)
            expected_offset = offset + size
            value, offset = property_type.from_bytes(data, offset)
            if offset != expected_offset:
                raise ValueError(f"{property_type} in [{start}, {offset - 1}] expected ending at {expected_offset}")
            result[name] = property_type.header_to_dict() | {"value": value}
            name, bytes_read = read_string(data, offset)
        return result, offset + bytes_read

    @classmethod
    @override
    def _header_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASStructPropertySerde], int]:
        property_subtype, bytes_read = read_string(data, offset)
        offset += bytes_read
        padding, flag = struct.unpack_from("<16sB", data, offset)
        if any(padding):
            raise ValueError(f"Invalid padding at {offset}")
        offset += 16
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        property_serde = _REGISTRY.get(property_subtype)
        if property_serde is None:
            property_serde = type(
                f"GVAS{cls._TYPE}PropertySerde@{property_subtype}",
                (GVASStructPropertySerde,),
                {"__slots__": (), "_SUBTYPE": property_subtype},
            )
        return property_serde, offset + 1

    @classmethod
    @override
    def _header_to_dict(cls) -> dict[str, str]:
        return {"subtype": cls._SUBTYPE}


class GVASGUIDPropertySerde(GVASStructPropertySerde):
    __slots__ = ()

    _SUBTYPE: ClassVar[str] = "Guid"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[str, int]:
        value = struct.unpack_from("<16s", data, offset)[0]
        return str(uuid.UUID(bytes_le=value)), offset + 16

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[str], int]:
        raise NotImplementedError(cls.__name__)
