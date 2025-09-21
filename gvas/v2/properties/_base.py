from __future__ import annotations

import struct
from typing import Any, ClassVar, override

from ..._base import GVASSerde
from ...utils import read_string


_REGISTRY: dict[str, type[GVASPropertySerde]] = {}


class GVASPropertySerde(GVASSerde):
    __slots__ = ()

    _TYPE: ClassVar[str]

    @staticmethod
    def get_type(name: str) -> type[GVASPropertySerde]:
        return _REGISTRY[name]

    @staticmethod
    def header_from_bytes(data: bytes, offset: int) -> tuple[type[GVASPropertySerde], int, int]:
        property_type, bytes_read = read_string(data, offset)
        offset += bytes_read
        size, padding = struct.unpack_from("<II", data, offset)
        offset += 4
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        property_serde, offset = _REGISTRY[property_type]._header_from_bytes(data, offset + 4)
        return property_serde, size, offset

    @override
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "_TYPE"):
            raise ValueError(f"{cls.__name__} does not have a type")
        if cls._TYPE in _REGISTRY:
            raise ValueError(f"{cls.__name__} has duplicate type {cls._TYPE}")
        if f"GVAS{cls._TYPE}Serde" != cls.__name__:
            raise ValueError(f"{cls.__name__} does not match type {cls._TYPE}")
        _REGISTRY[cls._TYPE] = cls

    @classmethod
    def header_to_dict(cls) -> dict[str, Any]:
        return {"type": cls._TYPE} | cls._header_to_dict()

    @classmethod
    def _header_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASPropertySerde], int]:
        flag = struct.unpack_from("<B", data, offset)[0]
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        return cls, offset + 1

    @classmethod
    def _header_to_dict(cls) -> dict[str, Any]:
        return {}

    @classmethod
    def _key_from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        return cls.from_bytes(data, offset)

    @classmethod
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[Any], int]:
        result: list[Any] = [None] * count
        for i in range(count):
            result[i], offset = cls.from_bytes(data, offset)
        return result, offset

    @classmethod
    def _value_from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        return cls.from_bytes(data, offset)
