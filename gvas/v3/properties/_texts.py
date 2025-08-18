import struct
from typing import Any, ClassVar, final, override

from ...utils import read_string, write_string
from ._base import GVASPropertySerde


class GVASTextPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Text"

    @staticmethod
    @final
    def _type_11_from_bytes(data: bytes, offset: int) -> tuple[dict[str, str], int]:
        table, bytes_read = read_string(data, offset)
        offset += bytes_read
        index, bytes_read = read_string(data, offset)
        return {"table": table, "index": index}, offset + bytes_read

    @staticmethod
    @final
    def _type_255_from_bytes(data: bytes, offset: int) -> tuple[str, int]:
        value, bytes_read = read_string(data, offset)
        return value, offset + bytes_read

    @staticmethod
    @final
    def _type_11_from_dict(data: dict[str, str]) -> bytes:
        return write_string(data["table"], data["index"])

    @staticmethod
    @final
    def _type_255_from_dict(data: str) -> bytes:
        return write_string(data)

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
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
        value, offset = getattr(cls, f"_type_{type_id}_from_bytes")(data, offset + 5)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return {"type": type_id, "value": value}, offset

    @classmethod
    @final
    @override
    def from_dict_full(cls, data: dict[str, Any]) -> bytes:
        type_id = data["type"]
        value_bytes = getattr(cls, f"_type_{type_id}_from_dict")(data["value"])
        return struct.pack("<IIBIB", 0, len(value_bytes) + 5, 0, 0, type_id) + value_bytes
