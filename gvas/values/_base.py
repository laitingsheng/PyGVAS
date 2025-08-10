from __future__ import annotations

import struct
from abc import abstractmethod
from typing import Any, ClassVar, Final, Self, Sequence, final

from ..utils import read_string


class GVASByteValue:
    __slots__ = ("_value",)

    _BLUEPRINT: ClassVar[str] = ""
    _NAME: ClassVar[str] = ""
    _REGISTRY: Final[dict[str, type[GVASByteValue]]] = {}

    _value: str

    @final
    def __init_subclass__(cls) -> None:
        if not cls._NAME or not cls._BLUEPRINT:
            return
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in cls._REGISTRY:
            raise ValueError("Duplicate registration")
        cls._REGISTRY[fullpath] = cls

    @final
    @staticmethod
    def get_class(blueprint: str, name: str) -> type[GVASByteValue]:
        return GVASByteValue._REGISTRY[f"{blueprint}/{name}"]

    @final
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        size, unit_width = struct.unpack_from("<IB", data, offset)
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        self = cls.__new__(cls)
        self._value, bytes_read = read_string(data, offset)
        if bytes_read != size:
            raise ValueError(f"Invalid string at {offset}")
        return self, offset + bytes_read

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @final
    def to_json(self) -> dict[str, Any]:
        return {"name": self._NAME, "blueprint": self._BLUEPRINT, "value": self._value}


class GVASEnumValue:
    __slots__ = ("_value",)

    _BLUEPRINT: ClassVar[str] = ""
    _NAME: ClassVar[str] = ""
    _REGISTRY: Final[dict[str, type[GVASEnumValue]]] = {}

    _value: str

    @final
    def __init_subclass__(cls) -> None:
        if not cls._NAME or not cls._BLUEPRINT:
            return
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in cls._REGISTRY:
            raise ValueError("Duplicate registration")
        cls._REGISTRY[fullpath] = cls

    @final
    @staticmethod
    def get_class(blueprint: str, name: str) -> type[GVASEnumValue]:
        return GVASEnumValue._REGISTRY[f"{blueprint}/{name}"]

    @final
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        type_name, bytes_read = read_string(data, offset)
        if type_name != "ByteProperty":
            raise ValueError(f"Invalid type name at {offset}")
        offset += bytes_read
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
        self = cls.__new__(cls)
        self._value, bytes_read = read_string(data, offset)
        if bytes_read != size:
            raise ValueError(f"Invalid string at {offset}")
        return self, offset + bytes_read

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @final
    def to_json(self) -> dict[str, Any]:
        return {"name": self._NAME, "blueprint": self._BLUEPRINT, "value": self._value}


class GVASStructValue:
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = ""
    _GUID: ClassVar[str] = ""
    _NAME: ClassVar[str] = ""
    _REGISTRY: Final[dict[str, type[GVASStructValue]]] = {}

    @final
    def __init_subclass__(cls) -> None:
        if not cls._NAME or not cls._BLUEPRINT:
            return
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in cls._REGISTRY:
            raise ValueError("Duplicate registration")
        cls._REGISTRY[fullpath] = cls

    @final
    @staticmethod
    def get_class(blueprint: str, name: str) -> type[GVASStructValue]:
        return GVASStructValue._REGISTRY[f"{blueprint}/{name}"]

    @final
    @classmethod
    def match_guid(cls, guid: str) -> bool:
        return cls._GUID == guid

    @classmethod
    @abstractmethod
    def parse(cls, unit_width: int, data: bytes, offset: int) -> tuple[Self, int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def parse_many(cls, unit_width: int, data: bytes, offset: int) -> tuple[Sequence[Self], int]:
        raise NotImplementedError(cls.__name__)

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @abstractmethod
    def to_json(self) -> Any:
        raise NotImplementedError(self.__class__.__name__)


class GVASTextValue:
    __slots__ = ()

    _TYPE: ClassVar[int] = -1
    _REGISTRY: Final[dict[int, type[GVASTextValue]]] = {}

    @final
    def __init_subclass__(cls) -> None:
        if cls._TYPE < 0:
            return
        if cls._TYPE in cls._REGISTRY:
            raise ValueError("Duplicate registration")
        cls._REGISTRY[cls._TYPE] = cls

    @final
    @staticmethod
    def get_class(type_id: int) -> type[GVASTextValue]:
        return GVASTextValue._REGISTRY[type_id]

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
