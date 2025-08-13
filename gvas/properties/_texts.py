from __future__ import annotations

from abc import abstractmethod
import struct
from typing import Any, ClassVar, Self, final, override

from ..utils import read_string
from ._base import GVASProperty

_REGISTRY: dict[int, type[GVASText]] = {}


class GVASText:
    __slots__ = ()

    _TYPE: ClassVar[int]

    @final
    @override
    def __init_subclass__(cls) -> None:
        if cls._TYPE < 0:
            raise ValueError(f"{cls.__name__} has an invalid type")
        if cls._TYPE in _REGISTRY:
            raise ValueError(f"Duplicate text value {cls._TYPE}")
        _REGISTRY[cls._TYPE] = cls

    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        raise NotImplementedError(cls.__name__)

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @abstractmethod
    def to_json(self) -> Any:
        raise NotImplementedError(self.__class__.__name__)


class GVASTextProperty(GVASProperty):
    __slots__ = ("_value",)

    _TYPE: ClassVar[str] = "Text"

    _value: GVASText

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, flag, type_id = struct.unpack_from("<IIBIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 5:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        self = cls.__new__(cls)
        self._value, offset = _REGISTRY[type_id].parse(data, offset + 5)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return self, offset

    @final
    @override
    def to_json(self) -> Any:
        return self._value.to_json()


class GVASTextStringTable(GVASText):
    __slots__ = ("_index", "_table")

    _TYPE: ClassVar[int] = 11

    _index: str
    _table: str

    @classmethod
    @final
    @override
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self = cls.__new__(cls)
        self._table, bytes_read = read_string(data, offset)
        offset += bytes_read
        self._index, bytes_read = read_string(data, offset)
        offset += bytes_read
        return self, offset

    @final
    @override
    def to_json(self) -> dict[str, str]:
        return {"table": self._table, "index": self._index}


class GVASTextString(GVASText):
    __slots__ = ("_value",)

    _TYPE: ClassVar[int] = 255

    _value: str

    @classmethod
    @final
    @override
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self = cls.__new__(cls)
        self._value, bytes_read = read_string(data, offset)
        return self, offset + bytes_read

    @final
    @override
    def to_json(self) -> str:
        return self._value
