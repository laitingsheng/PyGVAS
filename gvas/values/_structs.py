import itertools
import struct
from typing import ClassVar, Self, Sequence

from ..properties import GVASProperty
from ..utils import read_string
from ._base import GVASStructValue


class GVASCoreVector(GVASStructValue):
    __slots__ = (
        "_double",
        "_value",
    )

    _NAME: ClassVar[str] = "Vector"
    _BLUEPRINT: ClassVar[str] = "/Script/CoreUObject"

    _double: bool
    _value: tuple[float, float, float]

    @classmethod
    def parse(cls, unit_width: int, data: bytes, offset: int) -> tuple[Self, int]:
        if unit_width == 4:
            double = False
            x, y, z = struct.unpack_from("<3f", data, offset)
            offset += 12
        elif unit_width == 8:
            double = True
            x, y, z = struct.unpack_from("<3d", data, offset)
            offset += 24
        else:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._double = double
        self._value = x, y, z
        return self, offset


class GVASCoreRotator(GVASCoreVector):
    __slots__ = ()

    _NAME: ClassVar[str] = "Rotator"


class GVASCoreGameplayTagContainer(GVASStructValue):
    __slots__ = (
        "_tags",
    )

    _NAME: ClassVar[str] = "GameplayTagContainer"
    _BLUEPRINT: ClassVar[str] = "/Script/GameplayTags"

    _tags: list[tuple[int, int]]

    @classmethod
    def parse(cls, unit_width: int, data: bytes, offset: int) -> tuple[Self, int]:
        if unit_width != 8:
            raise ValueError(f"Invalid unit width at {offset}")
        count = struct.unpack_from("<L", data, offset)[0]
        offset += 4
        self = cls.__new__(cls)
        self._tags = [
            (instance, index)
            for instance, index in itertools.batched(
                struct.unpack_from(f"<{count * 2}L", data, offset),
                2,
            )
        ]
        offset += count * 8
        return self, offset


class GVASCustomStructValue(GVASStructValue):
    __slots__ = (
        "_attributes",
    )

    _attributes: dict[str, GVASProperty]

    @staticmethod
    def _parse_content(data: bytes, offset: int) -> tuple[dict[str, GVASProperty], int]:
        attributes: dict[str, GVASProperty] = {}
        name, bytes_read = read_string(data, offset)
        while name != "None":
            property_class, offset = GVASProperty.parse_type(
                data,
                offset + bytes_read,
            )
            value, offset = property_class.parse(data, offset)
            attributes[name] = value
            name, bytes_read = read_string(data, offset)
        offset += bytes_read
        return attributes, offset

    @classmethod
    def parse(cls, unit_width: int, data: bytes, offset: int) -> tuple[Self, int]:
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        self = cls.__new__(cls)
        self._attributes, offset = cls._parse_content(data, offset)
        return self, offset

    @classmethod
    def parse_many(cls, unit_width: int, data: bytes, offset: int) -> tuple[Sequence[Self], int]:
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        count = struct.unpack_from("<L", data, offset)[0]
        offset += 4
        selfs = [cls.__new__(cls) for _ in range(count)]
        for self in selfs:
            self._attributes, offset = cls._parse_content(data, offset)
        return selfs, offset
