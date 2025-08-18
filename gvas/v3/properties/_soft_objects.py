import struct
from typing import ClassVar, final, override

from ...utils import read_string, write_string
from ._base import GVASPropertySerde


class GVASSoftObjectPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "SoftObject"

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, str], int]:
        blueprint, bytes_read = read_string(data, offset)
        offset += bytes_read
        reference, bytes_read = read_string(data, offset)
        offset += bytes_read
        if struct.unpack_from("<I", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at {offset}")
        return {"blueprint": blueprint, "reference": reference}, offset + 4

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, str], int]:
        category, size, unit_width = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size < 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
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
    def from_bytes_set(cls, data: bytes, offset: int) -> tuple[list[dict[str, str]], int]:
        padding, size, unit_width, flag, count = struct.unpack_from("<IIBII", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 4
        if size < 8:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 1
        expected_offset = offset + size
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 8
        values: list[dict[str, str]] = []
        for _ in range(count):
            value, offset = cls.from_bytes(data, offset)
            values.append(value)
        if offset != expected_offset:
            raise ValueError(f"Invalid offset {offset}")
        return values, offset

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, str]) -> bytes:
        return write_string(data["blueprint"], data["reference"]) + struct.pack("<I", 0)

    @classmethod
    @final
    @override
    def from_dict_full(cls, data: dict[str, str]) -> bytes:
        body = cls.from_dict(data)
        return struct.pack("<IIB", 0, len(body), 0) + body

    @classmethod
    @final
    @override
    def from_dict_set(cls, data: list[dict[str, str]]) -> bytes:
        body = b"".join(cls.from_dict(item) for item in data)
        return struct.pack("<IIBII", 0, len(body) + 8, 0, 0, len(data)) + body
