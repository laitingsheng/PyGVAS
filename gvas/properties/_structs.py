from __future__ import annotations

import itertools
import struct
import uuid
from abc import abstractmethod
from typing import Any, ClassVar, final, override

from ..utils import read_string, write_string
from ._base import GVASPropertySerde


_REGISTRY: dict[str, type[GVASStructPropertySerde]] = {}


class GVASStructPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Struct"

    @override
    def __init_subclass__(cls) -> None:
        pass

    @classmethod
    @final
    @override
    def _concrete_type_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASStructPropertySerde], int]:
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
        concrete_class = _REGISTRY.get(fullpath)
        if singleton:
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
                (GVASBlueprintStructPropertySerde,),
                {"__slots__": (), "_BLUEPRINT": blueprint, "_NAME": name, "_GUID": guid},
            )
            _REGISTRY[fullpath] = concrete_class
        if not getattr(concrete_class, "_match_guid")(guid):
            raise ValueError(f"Mismatched GUID at {offset}")
        return concrete_class, offset

    @classmethod
    @final
    @override
    def _concrete_type_from_json(cls, data: dict[str, str]) -> type[GVASStructPropertySerde]:
        blueprint = data["blueprint"]
        name = data["name"]
        guid = data.get("guid", "")
        fullpath = f"{blueprint}/{name}"
        concrete_class = _REGISTRY.get(fullpath)
        if concrete_class is None:
            concrete_class = type(
                f"GVASStructProperty@{fullpath}",
                (GVASBlueprintStructPropertySerde,),
                {"__slots__": (), "_BLUEPRINT": blueprint, "_NAME": name, "_GUID": guid},
            )
            _REGISTRY[fullpath] = concrete_class
        if not getattr(concrete_class, "_match_guid")(guid):
            raise ValueError(f"Mismatched GUID for {fullpath}")
        return concrete_class

    @classmethod
    @abstractmethod
    def _match_guid(cls, guid: str) -> bool:
        raise NotImplementedError(cls.__name__)


class GVASUniqueStructPropertySerde(GVASStructPropertySerde):
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
    def type_to_json(cls) -> dict[str, str]:
        return super().type_to_json() | {"blueprint": cls._BLUEPRINT, "name": cls._NAME}

    @classmethod
    @final
    @override
    def type_to_bytes(cls) -> bytes:
        return (
            super().type_to_bytes()
            + struct.pack("<I", 1)
            + write_string(cls._NAME)
            + struct.pack("<I", 1)
            + write_string(cls._BLUEPRINT)
        )

    @classmethod
    @final
    @override
    def _match_guid(cls, guid: str) -> bool:
        return guid == ""


class GVASCoreDateTimeSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "DateTime"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[int, int]:
        category, size, unit_width, timestamp = struct.unpack_from("<IIBQ", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        return timestamp, offset + 9

    @classmethod
    @final
    @override
    def from_json_full(cls, data: int) -> bytes:
        return struct.pack("<IIBQ", 0, 8, 8, data)


class GVASCoreGameplayTagContainerSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/GameplayTags"
    _NAME: ClassVar[str] = "GameplayTagContainer"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[list[str], int]:
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
        tags: dict[str, bool] = {}
        for _ in range(count):
            tag, bytes_read = read_string(data, offset)
            offset += bytes_read
            tags[tag] = True
        if offset != expected_offset:
            raise ValueError(f"Invalid size at {offset}")
        return list(tags.keys()), offset

    @classmethod
    @final
    @override
    def from_json_full(cls, data: list[str]) -> bytes:
        tag_bytes = write_string(*data)
        return struct.pack("<IIBI", 0, len(tag_bytes) + 4, 8, len(data)) + tag_bytes


class GVASCoreGUIDSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Guid"

    @classmethod
    @final
    @override
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[str], int]:
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
        return [
            str(uuid.UUID(bytes_le=guid_bytes)) for guid_bytes in struct.unpack_from("<" + "16s" * count, data, offset)
        ], offset + count * 16

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[str, int]:
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
        guid = uuid.UUID(bytes_le=struct.unpack_from("<16s", data, offset)[0])
        return str(guid), offset + 16

    @classmethod
    @final
    @override
    def from_json_full(cls, data: str) -> bytes:
        return struct.pack("<IIB16s", 0, 16, 8, uuid.UUID(data).bytes_le)

    @classmethod
    @final
    @override
    def from_json_array(cls, data: list[str]) -> bytes:
        return struct.pack(
            "<IIBI" + "16s" * len(data),
            0,
            len(data) * 16 + 4,
            8,
            len(data),
            *(uuid.UUID(guid).bytes_le for guid in data),
        )


class GVASCoreSoftObjectPathSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "SoftObjectPath"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, str], int]:
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
        blueprint, bytes_read = read_string(data, offset)
        offset += bytes_read
        name, bytes_read = read_string(data, offset)
        offset += bytes_read
        value, bytes_read = read_string(data, offset)
        offset += bytes_read
        if offset != expected_offset:
            raise ValueError(f"Invalid size at {offset}")
        return {"blueprint": blueprint, "name": name, "value": value}, offset

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, str]) -> bytes:
        body = write_string(data["blueprint"], data["name"], data["value"])
        return struct.pack("<IIB", 0, len(body), 8) + body


class GVASCoreTimespanSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Timespan"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[int, int]:
        category, size, unit_width, duration = struct.unpack_from("<IIBQ", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        return duration, offset + 9

    @classmethod
    @final
    @override
    def from_json_full(cls, data: int) -> bytes:
        return struct.pack("<IIBQ", 0, 8, 8, data)


class GVASCoreUniqueNetIDSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/Engine"
    _NAME: ClassVar[str] = "UniqueNetIdRepl"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, str], int]:
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
        source, bytes_read = read_string(data, offset)
        offset += bytes_read
        identifier, bytes_read = read_string(data, offset)
        if len(identifier) + 1 != length:
            raise ValueError(f"Invalid identifier length at {offset}")
        offset += bytes_read
        if offset != expected_offset:
            raise ValueError(f"Invalid size at {offset}")
        return {"source": source, "identifier": identifier}, offset

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, str]) -> bytes:
        identifier = data["identifier"]
        body = struct.pack("<I", len(identifier) + 1) + write_string(data["source"], identifier)
        return struct.pack("<IIB", 0, len(body), 8) + body


class GVASCoreVectorSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Vector"

    @classmethod
    @final
    @override
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[dict[str, float]], int]:
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
        values: list[dict[str, float]] = []
        for x, y, z in itertools.batched(struct.unpack_from(f"<{count * 3}d", data, offset), 3):
            values.append({"x": x, "y": y, "z": z})
        return values, offset + count * 24

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, float], int]:
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
        return {"x": x, "y": y, "z": z}, offset + 24

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, float]) -> bytes:
        return struct.pack("<IIB3d", 0, 24, 8, data["x"], data["y"], data["z"])

    @classmethod
    @final
    @override
    def from_json_array(cls, data: list[dict[str, float]]) -> bytes:
        return struct.pack(
            f"<IIBI{len(data) * 3}d",
            0,
            len(data) * 24 + 4,
            8,
            len(data),
            *itertools.chain.from_iterable((item["x"], item["y"], item["z"]) for item in data),
        )


class GVASCoreRotatorSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Rotator"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, float], int]:
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
        return {"x": x, "y": y, "z": z}, offset + 24

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, float]) -> bytes:
        return struct.pack("<IIB3d", 0, 24, 8, data["x"], data["y"], data["z"])


class GVASCoreQuatSerde(GVASUniqueStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"
    _NAME: ClassVar[str] = "Quat"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, float], int]:
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
        return {"x": x, "y": y, "z": z, "w": w}, offset + 32

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, float]) -> bytes:
        return struct.pack("<IIB4d", 0, 32, 8, data["x"], data["y"], data["z"], data["w"])


class GVASBlueprintStructPropertySerde(GVASStructPropertySerde):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str]
    _GUID: ClassVar[str]
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
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, dict[str, Any]], int]:
        result: dict[str, dict[str, Any]] = {}
        name, bytes_read = read_string(data, offset)
        while name != "None":
            property_type, offset = GVASPropertySerde.type_from_bytes(data, offset + bytes_read)
            value, offset = property_type.from_bytes_full(data, offset)
            result[name] = {"type": property_type.type_to_json(), "value": value}
            name, bytes_read = read_string(data, offset)
        return result, offset + bytes_read

    @classmethod
    @override
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[dict[str, dict[str, Any]]], int]:
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
        values: list[dict[str, dict[str, Any]]] = []
        for _ in range(count):
            value, offset = cls.from_bytes(data, offset)
            values.append(value)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return values, offset

    @classmethod
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, dict[str, Any]], int]:
        padding, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 8
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        result, offset = cls.from_bytes(data, offset)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return result, offset

    @classmethod
    @final
    @override
    def type_to_json(cls) -> dict[str, str]:
        result = super().type_to_json() | {"blueprint": cls._BLUEPRINT, "name": cls._NAME}
        if cls._GUID:
            result["guid"] = cls._GUID
        return result

    @classmethod
    @final
    @override
    def _match_guid(cls, guid: str) -> bool:
        return guid == cls._GUID

    @classmethod
    @final
    @override
    def type_to_bytes(cls) -> bytes:
        if cls._GUID:
            return (
                super().type_to_bytes()
                + struct.pack("<I", 2)
                + write_string(cls._NAME)
                + struct.pack("<I", 1)
                + write_string(cls._BLUEPRINT)
                + struct.pack("<I", 0)
                + write_string(cls._GUID)
            )
        return (
            super().type_to_bytes()
            + struct.pack("<I", 1)
            + write_string(cls._NAME)
            + struct.pack("<I", 1)
            + write_string(cls._BLUEPRINT)
        )

    @classmethod
    @final
    @override
    def from_json(cls, data: dict[str, dict[str, Any]]) -> bytes:
        result = bytearray()
        for name, property_data in data.items():
            result.extend(write_string(name))
            property_type = GVASPropertySerde.type_from_json(property_data["type"])
            result.extend(property_type.type_to_bytes())
            result.extend(property_type.from_json_full(property_data["value"]))
        result.extend(write_string("None"))
        return bytes(result)

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, dict[str, Any]]) -> bytes:
        body = cls.from_json(data)
        return struct.pack("<IIB", 0, len(body), 0) + body

    @classmethod
    @override
    def from_json_array(cls, data: list[dict[str, dict[str, Any]]]) -> bytes:
        result = b"".join(cls.from_json(item) for item in data)
        return struct.pack("<IIBI", 0, len(result) + 4, 0, len(data)) + result
