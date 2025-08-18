import struct
from typing import ClassVar, final, override

from ._base import GVASPropertySerde


class GVASBoolPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Bool"

    @classmethod
    @final
    @override
    def from_bytes_array(cls, data: bytes, offset: int) -> tuple[list[bool], int]:
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
        if count + 4 != size:
            raise ValueError(f"Invalid count at {offset}")
        offset += 4
        values: list[bool] = []
        for value in struct.unpack_from(f"<{count}B", data, offset):
            if value == 0:
                values.append(False)
            elif value == 0x1:
                values.append(True)
            else:
                raise ValueError(f"Invalid value at {offset}")
        return values, offset + count

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[bool, int]:
        category, size, value = struct.unpack_from("<IIB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 0:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if value == 0:
            return False, offset + 1
        if value == 0x10:
            return True, offset + 1
        raise ValueError(f"Invalid value at {offset}")

    @classmethod
    @override
    def from_dict_array(cls, data: list[bool]) -> bytes:
        return struct.pack(f"<IIBI{len(data)}B", 0, len(data) + 4, 0, len(data), *(1 if b else 0 for b in data))

    @classmethod
    @final
    @override
    def from_dict_full(cls, data: bool) -> bytes:
        return struct.pack("<IIB", 0, 0, 0x10 if data else 0)
