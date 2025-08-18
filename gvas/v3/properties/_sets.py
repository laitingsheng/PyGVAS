import struct
from typing import Any, ClassVar, final, override

from ._base import GVASPropertySerde


class GVASSetPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Set"

    @classmethod
    @final
    @override
    def from_bytes_full(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        if struct.unpack_from("<I", data, offset)[0] != 1:
            raise ValueError(f"Invalid category at {offset}")
        element_type, offset = GVASPropertySerde.type_from_bytes(data, offset + 4)
        values, offset = element_type.from_bytes_set(data, offset)
        return {"type": element_type.type_to_json(), "values": values}, offset

    @classmethod
    @final
    @override
    def from_json_full(cls, data: dict[str, Any]) -> bytes:
        element_type = GVASPropertySerde.type_from_json(data["type"])
        return struct.pack("<I", 1) + element_type.type_to_bytes() + element_type.from_json_set(data["values"])
