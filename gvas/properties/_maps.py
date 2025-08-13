import struct
from typing import Any, ClassVar, Self, override

from ._base import GVASProperty


class GVASMapProperty(GVASProperty):
    __slots__ = ("_key_type", "_value_type", "_values")

    _TYPE: ClassVar[str] = "Map"

    _key_type: type[GVASProperty]
    _value_type: type[GVASProperty]
    _values: list[tuple[GVASProperty, GVASProperty]]

    @classmethod
    @override
    def parse_full(cls, data: bytes, offset: int) -> tuple[Self, int]:
        if struct.unpack_from("<I", data, offset)[0] != 2:
            raise ValueError(f"Invalid category at {offset}")
        self = cls.__new__(cls)
        self._key_type, offset = GVASProperty.parse_type(data, offset + 4)
        if struct.unpack_from("<I", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at offset {offset}")
        self._value_type, offset = GVASProperty.parse_type(data, offset + 4)
        flag, size, unit_width, padding, count = struct.unpack_from("<IIBII", data, offset)
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 4
        if size < 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 8
        self._values = []
        for _ in range(count):
            key, offset = self._key_type.parse(data, offset)
            value, offset = self._value_type.parse(data, offset)
            self._values.append((key, value))
        return self, offset

    @override
    def to_json(self) -> dict[str, Any]:
        return {
            "key_type": self._key_type.type_json(),
            "value_type": self._value_type.type_json(),
            "values": [{"key": key.to_json(), "value": value.to_json()} for key, value in self._values],
        }
