import struct
from typing import override

from ._base import GVASPropertySerde


class GVASFloatPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE = "FloatProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[float, int]:
        return struct.unpack_from("<f", data, offset)[0], offset + 4

    @classmethod
    @override
    def _multiple_from_bytes(cls, data: bytes, offset: int, count: int) -> tuple[list[float], int]:
        return list(struct.unpack_from(f"<{count}f", data, offset)), offset + 4 * count
