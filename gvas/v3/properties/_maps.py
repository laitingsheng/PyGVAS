import struct
from typing import Any, ClassVar, final, override

from ._base import GVASPropertySerde


class GVASMapPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Map"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        if struct.unpack_from("<I", data, offset)[0] != 2:
            raise ValueError(f"Invalid category at {offset}")
        key_type, offset = GVASPropertySerde.type_from_bytes(data, offset + 4)
        if struct.unpack_from("<I", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at {offset}")
        value_type, offset = GVASPropertySerde.type_from_bytes(data, offset + 4)
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
        expected_offset = offset + size
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 8
        values: list[tuple[Any, Any]] = []
        for _ in range(count):
            key, offset = key_type.from_bytes(data, offset)
            value, offset = value_type.from_bytes(data, offset)
            values.append((key, value))
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return {
            "key_type": key_type.type_to_dict(),
            "value_type": value_type.type_to_dict(),
            "values": values,
        }, offset

    @classmethod
    @final
    @override
    def from_dict_full(cls, data: dict[str, Any]) -> bytes:
        key_type = GVASPropertySerde.type_from_dict(data["key_type"])
        value_type = GVASPropertySerde.type_from_dict(data["value_type"])
        values = data["values"]
        body = b"".join(key_type.from_dict(key) + value_type.from_dict(value) for key, value in values)
        return (
            struct.pack("<I", 2)
            + key_type.type_to_bytes()
            + struct.pack("<I", 0)
            + value_type.type_to_bytes()
            + struct.pack("<IIBII", 0, len(body) + 8, 0, 0, len(values))
            + body
        )
