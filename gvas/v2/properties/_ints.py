import struct
from typing import override

from ._base import GVASPropertySerde


class GVASIntPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE = "IntProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[int, int]:
        return struct.unpack_from("<i", data, offset)[0], offset + 4

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[int], int]:
        return list(struct.unpack_from(f"<{count}i", data, offset)), offset + 4 * count
