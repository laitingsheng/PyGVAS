from __future__ import annotations

from abc import abstractmethod
from typing import Any, ClassVar, Final, Self, final

from ..utils import read_string


class GVASProperty:
    __slots__ = ()

    _ACCEPT: ClassVar[str] = ""
    _REGISTRY: Final[dict[str, type[GVASProperty]]] = {}

    @final
    def __init_subclass__(cls) -> None:
        if not cls._ACCEPT:
            return
        if cls._ACCEPT in cls._REGISTRY:
            raise ValueError("Duplicate registration")
        cls._REGISTRY[cls._ACCEPT] = cls

    @final
    @classmethod
    def parse_type(cls, data: bytes, offset: int) -> tuple[type[GVASProperty], int]:
        type_name, bytes_read = read_string(data, offset)
        return cls._REGISTRY[type_name], offset + bytes_read

    @classmethod
    @abstractmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        raise NotImplementedError(cls.__name__)

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @abstractmethod
    def to_json(self) -> Any:
        raise NotImplementedError(self.__class__.__name__)


class GVASPropertyArray:
    __slots__ = ()

    _ACCEPT: ClassVar[str] = ""
    _REGISTRY: Final[dict[str, type[GVASPropertyArray]]] = {}

    @final
    def __init_subclass__(cls) -> None:
        if not cls._ACCEPT:
            return
        if cls._ACCEPT in cls._REGISTRY:
            raise ValueError("Duplicate registration")
        cls._REGISTRY[cls._ACCEPT] = cls

    @final
    @classmethod
    def parse_type(cls, data: bytes, offset: int) -> tuple[type[GVASPropertyArray], int]:
        type_name, bytes_read = read_string(data, offset)
        return cls._REGISTRY[type_name], offset + bytes_read

    @classmethod
    @abstractmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        raise NotImplementedError(cls.__name__)

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @abstractmethod
    def to_json(self) -> Any:
        raise NotImplementedError(self.__class__.__name__)
