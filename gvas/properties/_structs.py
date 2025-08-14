from __future__ import annotations

import itertools
import struct
from abc import abstractmethod
from typing import Any, ClassVar, Self, Sequence, final, override
import uuid

from ..utils import read_string
from ._base import GVASProperty

_REGISTRY: dict[str, type[GVASStructProperty]] = {}


class GVASStructProperty(GVASProperty):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Struct"

    @override
    def __init_subclass__(cls) -> None:
        pass

    @classmethod
    @override
    def parse_array(cls, data: bytes, offset: int) -> tuple[Sequence[Self], int]:
        padding, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        offset += 4
        selfs: list[Self] = []
        for _ in range(count):
            self, offset = cls.parse(data, offset)
            selfs.append(self)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return selfs, offset

    @classmethod
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 8
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        self, offset = cls.parse(data, offset)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return self, offset

    @classmethod
    @final
    @override
    def _concrete_type(cls, data: bytes, offset: int) -> tuple[type[GVASStructProperty], int]:
        category = struct.unpack_from("<I", data, offset)[0]
        if category == 1:
            singleton = True
        elif category == 2:
            singleton = False
        else:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        name, bytes_read = read_string(data, offset)
        if not name:
            raise ValueError(f"Invalid name at {offset}")
        offset += bytes_read
        index = struct.unpack_from("<I", data, offset)[0]
        if index != 1:
            raise ValueError(f"Invalid index at {offset}")
        offset += 4
        blueprint, bytes_read = read_string(data, offset)
        if not blueprint:
            raise ValueError(f"Invalid blueprint at {offset}")
        offset += bytes_read
        fullpath = f"{blueprint}/{name}"
        concrete_class = _REGISTRY.get(fullpath, None)
        if singleton:
            if concrete_class is None:
                concrete_class = type(
                    f"GVASStructProperty@{fullpath}",
                    (GVASBlueprintStructProperty,),
                    {"__slots__": (), "_BLUEPRINT": blueprint, "_NAME": name, "_GUID": ""},
                )
                _REGISTRY[fullpath] = concrete_class
            guid = ""
        else:
            if struct.unpack_from("<I", data, offset)[0] != 0:
                raise ValueError(f"Invalid index at {offset}")
            offset += 4
            guid, bytes_read = read_string(data, offset)
            if not guid:
                raise ValueError(f"Missing guid at {offset}")
            offset += bytes_read
            if concrete_class is None:
                concrete_class = type(
                    f"GVASStructProperty@{fullpath}",
                    (GVASBlueprintStructProperty,),
                    {"__slots__": (), "_BLUEPRINT": blueprint, "_NAME": name, "_GUID": guid},
                )
                _REGISTRY[fullpath] = concrete_class
        if not getattr(concrete_class, "_match_guid")(guid):
            raise ValueError(f"Mismatched GUID at {offset}")
        return concrete_class, offset

    @classmethod
    @abstractmethod
    def _match_guid(cls, guid: str) -> bool:
        raise NotImplementedError(cls.__name__)


class GVASUniqueStructProperty(GVASStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str]
    _NAME: ClassVar[str]

    @final
    @override
    def __init_subclass__(cls) -> None:
        if not cls._BLUEPRINT:
            raise ValueError(f"{cls.__name__} does not have a blueprint")
        if not cls._NAME:
            raise ValueError(f"{cls.__name__} does not have a name")
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in _REGISTRY:
            raise ValueError(f"Duplicate struct property {cls._NAME} in {cls._BLUEPRINT}")
        _REGISTRY[fullpath] = cls

    @classmethod
    @final
    @override
    def type_json(cls) -> dict[str, str]:
        return super().type_json() | {"blueprint": cls._BLUEPRINT, "name": cls._NAME}

    @classmethod
    @final
    @override
    def _match_guid(cls, guid: str) -> bool:
        return guid == ""


class GVASCoreDateTime(GVASUniqueStructProperty):
    __slots__ = ("_timestamp",)

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "DateTime"

    _timestamp: int

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, timestamp = struct.unpack_from("<IIBQ", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._timestamp = timestamp
        return self, offset + 9

    @final
    @override
    def to_json(self) -> int:
        return self._timestamp


class GVASCoreGameplayTagContainer(GVASUniqueStructProperty):
    __slots__ = ("_tags",)

    _BLUEPRINT: ClassVar[str] = "/Script/GameplayTags"
    _NAME: ClassVar[str] = "GameplayTagContainer"

    _tags: dict[str, bool]

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        offset += 4
        self = cls.__new__(cls)
        self._tags = {}
        for _ in range(count):
            tag, bytes_read = read_string(data, offset)
            offset += bytes_read
            self._tags[tag] = True
        if offset != expected_offset:
            raise ValueError(f"Invalid size at {offset}")
        return self, offset

    @final
    @override
    def to_json(self) -> list[str]:
        return list(self._tags.keys())


class GVASCoreGUID(GVASUniqueStructProperty):
    __slots__ = ("_guid",)

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Guid"

    _guid: uuid.UUID

    @classmethod
    @final
    @override
    def parse_array(cls, data: bytes, offset: int) -> tuple[list[Self], int]:
        padding, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        if count * 16 + 4 != size:
            raise ValueError(f"Invalid count at {offset}")
        offset += 4
        selfs: list[Self] = []
        for guid_bytes in struct.unpack_from("<" + "16s" * count, data, offset):
            self = cls.__new__(cls)
            self._guid = uuid.UUID(bytes_le=guid_bytes)
            selfs.append(self)
        return selfs, offset + count * 16

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 16:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        self = cls.__new__(cls)
        self._guid = uuid.UUID(bytes_le=struct.unpack_from("<16s", data, offset)[0])
        return self, offset + 16

    @final
    @override
    def to_json(self) -> str:
        return str(self._guid)


class GVASCoreSoftObjectPath(GVASUniqueStructProperty):
    __slots__ = ("_blueprint", "_name", "_value")

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "SoftObjectPath"

    _blueprint: str
    _name: str
    _value: str

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 12:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        self = cls.__new__(cls)
        self._blueprint, bytes_read = read_string(data, offset)
        offset += bytes_read
        self._name, bytes_read = read_string(data, offset)
        offset += bytes_read
        self._value, bytes_read = read_string(data, offset)
        offset += bytes_read
        if offset != expected_offset:
            raise ValueError(f"Invalid size at {offset}")
        return self, offset

    @final
    @override
    def to_json(self) -> dict[str, str]:
        return {"blueprint": self._blueprint, "name": self._name, "value": self._value}


class GVASCoreTimespan(GVASUniqueStructProperty):
    __slots__ = ("_duration",)

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Timespan"

    _duration: int

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, duration = struct.unpack_from("<IIBQ", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._duration = duration
        return self, offset + 9

    @final
    @override
    def to_json(self) -> int:
        return self._duration


class GVASCoreUniqueNetID(GVASUniqueStructProperty):
    __slots__ = ("_source", "_identifier")

    _BLUEPRINT: ClassVar[str] = "/Script/Engine"
    _NAME: ClassVar[str] = "UniqueNetIdRepl"

    _source: str
    _identifier: str

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, length = struct.unpack_from("<IIBI", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        offset += 4
        self = cls.__new__(cls)
        self._source, bytes_read = read_string(data, offset)
        offset += bytes_read
        self._identifier, bytes_read = read_string(data, offset)
        if len(self._identifier) + 1 != length:
            raise ValueError(f"Invalid identifier length at {offset}")
        offset += bytes_read
        if offset != expected_offset:
            raise ValueError(f"Invalid size at {offset}")
        return self, offset

    @final
    @override
    def to_json(self) -> dict[str, str]:
        return {
            "source": self._source,
            "identifier": self._identifier,
        }


class GVASCoreVector(GVASUniqueStructProperty):
    __slots__ = ("_value",)

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Vector"

    _value: tuple[float, float, float]

    @classmethod
    @final
    @override
    def parse_array(cls, data: bytes, offset: int) -> tuple[list[Self], int]:
        padding, size, unit_width, count = struct.unpack_from("<IIBI", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        if count * 24 + 4 != size:
            raise ValueError(f"Invalid count at {offset}")
        offset += 4
        selfs: list[Self] = []
        for x, y, z in itertools.batched(struct.unpack_from(f"<{count * 3}d", data, offset), 3):
            self = cls.__new__(cls)
            self._value = x, y, z
            selfs.append(self)
        return selfs, offset + count * 24

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 24:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        x, y, z = struct.unpack_from("<3d", data, offset)
        self = cls.__new__(cls)
        self._value = x, y, z
        return self, offset + 24

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        x, y, z = self._value
        return {"x": x, "y": y, "z": z}


class GVASCoreRotator(GVASUniqueStructProperty):
    __slots__ = ("_value",)

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Rotator"

    _value: tuple[float, float, float]

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 24:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        x, y, z = struct.unpack_from("<3d", data, offset)
        self = cls.__new__(cls)
        self._value = x, y, z
        return self, offset + 24

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        x, y, z = self._value
        return {"x": x, "y": y, "z": z}


class GVASCoreQuat(GVASUniqueStructProperty):
    __slots__ = ("_value",)

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Quat"

    _value: tuple[float, float, float, float]

    @classmethod
    @final
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 32:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        x, y, z, w = struct.unpack_from("<4d", data, offset)
        self = cls.__new__(cls)
        self._value = x, y, z, w
        return self, offset + 32

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        x, y, z, w = self._value
        return {"x": x, "y": y, "z": z, "w": w}


class GVASBlueprintStructProperty(GVASStructProperty):
    __slots__ = ("_attributes",)

    _BLUEPRINT: ClassVar[str]
    _GUID: ClassVar[str]
    _NAME: ClassVar[str]

    _attributes: dict[str, GVASProperty]

    @final
    @override
    def __init_subclass__(cls) -> None:
        if not cls._BLUEPRINT:
            raise ValueError(f"{cls.__name__} does not have a blueprint")
        if not cls._NAME:
            raise ValueError(f"{cls.__name__} does not have a name")
        fullpath = f"{cls._BLUEPRINT}/{cls._NAME}"
        if fullpath in _REGISTRY:
            raise ValueError(f"Duplicate struct property {cls._NAME} in {cls._BLUEPRINT}")
        _REGISTRY[fullpath] = cls

    @classmethod
    @final
    @override
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self = cls.__new__(cls)
        self._attributes = {}
        name, bytes_read = read_string(data, offset)
        while name != "None":
            property_type, offset = GVASProperty.parse_type(data, offset + bytes_read)
            attribute, offset = property_type.parse_full(data, offset)
            self._attributes[name] = attribute
            name, bytes_read = read_string(data, offset)
        offset += bytes_read
        return self, offset

    @classmethod
    @final
    @override
    def type_json(cls) -> dict[str, str]:
        result = super().type_json() | {"blueprint": cls._BLUEPRINT, "name": cls._NAME}
        if cls._GUID:
            result["guid"] = cls._GUID
        return result

    @classmethod
    @final
    @override
    def _match_guid(cls, guid: str) -> bool:
        return guid == cls._GUID

    @final
    @override
    def to_json(self) -> dict[str, dict[str, dict[str, Any]]]:
        return {key: {"type": value.type_json(), "value": value.to_json()} for key, value in self._attributes.items()}
