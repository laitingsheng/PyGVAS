from typing import ClassVar, override

from ...utils import read_string
from ._base import GVASPropertySerde


class GVASObjectPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "ObjectProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[str, int]:
        value, bytes_read = read_string(data, offset)
        return value, offset + bytes_read
