from __future__ import annotations

from abc import abstractmethod
from typing import Any, ClassVar, Self, final, override

from .._base import GVASSerde
from ..utils import read_string, write_string


_REGISTRY: dict[str, type[GVASPropertySerde]] = {}


class GVASPropertySerde(GVASSerde):
    __slots__ = ()

    _TYPE: ClassVar[str]

    @staticmethod
    @final
    def type_from_bytes(data: bytes, offset: int) -> tuple[type[GVASPropertySerde], int]:
        property_type, bytes_read = read_string(data, offset)
        return _REGISTRY[property_type]._concrete_type_from_bytes(data, offset + bytes_read)

    @staticmethod
    @final
    def type_from_json(data: dict[str, str]) -> type[GVASPropertySerde]:
        return _REGISTRY[data["type"]]._concrete_type_from_json(data)

    @override
    def __init_subclass__(cls) -> None:
        if not cls._TYPE:
            raise ValueError(f"{cls.__name__} does not have a type")
        type_name = f"{cls._TYPE}Property"
        if type_name in _REGISTRY:
            raise ValueError(f"Duplicate type {cls._TYPE} for {cls.__name__}")
        if f"GVAS{type_name}Serde" != cls.__name__:
            raise ValueError(f"Invalid class name {cls.__name__} for type {cls._TYPE}")
        _REGISTRY[type_name] = cls

    @classmethod
    @abstractmethod
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[Any], int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[Any, int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_bytes_set(cls, data: bytes, offset: int) -> tuple[list[Any], int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_json_array(cls, data: list[Any]) -> bytes:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_json_full(cls, data: Any) -> bytes:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_json_set(cls, data: list[Any]) -> bytes:
        raise NotImplementedError(cls.__name__)

    @classmethod
    def type_to_bytes(cls) -> bytes:
        return write_string(f"{cls._TYPE}Property")

    @classmethod
    def type_to_json(cls) -> dict[str, str]:
        return {"type": f"{cls._TYPE}Property"}

    @classmethod
    def _concrete_type_from_bytes(cls, data: bytes, offset: int) -> tuple[type[Self], int]:
        return cls, offset

    @classmethod
    def _concrete_type_from_json(cls, data: dict[str, str]) -> type[Self]:
        return cls
