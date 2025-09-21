from typing import override

from ...utils import read_string
from ._base import GVASPropertySerde


class GVASNamePropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE = "NameProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[str, int]:
        value, bytes_read = read_string(data, offset)
        return value, offset + bytes_read
