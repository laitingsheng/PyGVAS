from __future__ import annotations

from abc import abstractmethod
from typing import Any, ClassVar, Self, Sequence, final, override

from ..utils import read_string

_REGISTRY: dict[str, type[GVASProperty]] = {}


class GVASProperty:
    __slots__ = ()

    _TYPE: ClassVar[str]

    @final
    @staticmethod
    def parse_type(data: bytes, offset: int) -> tuple[type[GVASProperty], int]:
        property_type, bytes_read = read_string(data, offset)
        return _REGISTRY[property_type]._concrete_type(data, offset + bytes_read)

    @override
    def __init_subclass__(cls) -> None:
        if not cls._TYPE:
            raise ValueError(f"{cls.__name__} does not have a type")
        type_name = f"{cls._TYPE}Property"
        if type_name in _REGISTRY:
            raise ValueError(f"Duplicate type {cls._TYPE} for {cls.__name__}")
        if f"GVAS{type_name}" != cls.__name__:
            raise ValueError(f"Invalid class name {cls.__name__} for type {cls._TYPE}")
        _REGISTRY[type_name] = cls

    @classmethod
    @abstractmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def parse_array(cls, data: bytes, offset: int) -> tuple[Sequence[Self], int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def parse_set(cls, data: bytes, offset: int) -> tuple[Sequence[Self], int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    def type_json(cls) -> dict[str, Any]:
        return {"type": f"{cls._TYPE}Property"}

    @classmethod
    def _concrete_type(cls, data: bytes, offset: int) -> tuple[type[Self], int]:
        return cls, offset

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @abstractmethod
    def to_json(self) -> Any:
        raise NotImplementedError(self.__class__.__name__)
