import struct
from typing import override

from ._base import GVASPropertySerde


class GVASInt64PropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE = "Int64Property"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[int, int]:
        return struct.unpack_from("<q", data, offset)[0], offset + 8

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[int], int]:
        return list(struct.unpack_from(f"<{count}q", data, offset)), offset + 8 * count
