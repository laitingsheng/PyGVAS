from typing import override

from ...utils import read_string
from ._base import GVASPropertySerde


class GVASStrPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE = "StrProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[str, int]:
        value, bytes_read = read_string(data, offset)
        return value, offset + bytes_read
