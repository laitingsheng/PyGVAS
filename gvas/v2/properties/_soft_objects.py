from typing import ClassVar, override

from ...utils import read_string
from ._base import GVASPropertySerde


class GVASSoftObjectPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "SoftObjectProperty"

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, str], int]:
        blueprint, bytes_read = read_string(data, offset)
        offset += bytes_read
        reference, bytes_read = read_string(data, offset)
        return {"blueprint": blueprint, "reference": reference}, offset + bytes_read
