from __future__ import annotations

import struct
from typing import Any, ClassVar, override

from ._base import GVASPropertySerde


_REGISTRY: dict[int, type[GVASBoolPropertySerde]] = {}


class GVASBoolPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "BoolProperty"
    _VALUE: ClassVar[int]

    @override
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "_VALUE"):
            raise ValueError(f"{cls.__name__} does not have a value")
        if cls._VALUE in _REGISTRY:
            raise ValueError(f"{cls.__name__} has duplicate value {cls._VALUE}")
        _REGISTRY[cls._VALUE] = cls

    @classmethod
    @override
    def _header_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASPropertySerde], int]:
        value, flag = struct.unpack_from("<BB", data, offset)
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        return _REGISTRY[value], offset + 2

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[Any], int]:
        value = struct.unpack_from(f"<{count}B", data, offset)
        values = [False] * count
        for i, v in enumerate(value):
            if v == 1:
                values[i] = True
            elif v != 0:
                raise ValueError(f"Invalid bool value at {offset + i}")
        return values, offset + count


class GVASTrueSerde(GVASBoolPropertySerde):
    __slots__ = ()

    _VALUE: ClassVar[int] = 1

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        return True, offset

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[Any], int]:
        raise NotImplementedError(cls.__name__)


class GVASFalseSerde(GVASBoolPropertySerde):
    __slots__ = ()

    _VALUE: ClassVar[int] = 0

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        return False, offset

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[Any], int]:
        raise NotImplementedError(cls.__name__)
