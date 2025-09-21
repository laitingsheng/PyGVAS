from typing import Any, override

from ._base import GVASSerde
from .utils import read_string, write_string
from .versions import (
    GVASCustomVersionsSerde,
    GVASSaveVersionSerde,
    GVASUEVersionSerde,
)


class GVASHeaderSerde(GVASSerde):
    __slots__ = ()

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        if data[offset : offset + 4] != b"GVAS":
            raise ValueError("Invalid GVAS header")
        offset += 4
        save_version, offset = GVASSaveVersionSerde.from_bytes(data, offset)
        ue_version, offset = GVASUEVersionSerde.from_bytes(data, offset)
        customs, offset = GVASCustomVersionsSerde.from_bytes(data, offset)
        blueprint, bytes_read = read_string(data, offset)
        return {
            "save_version": save_version,
            "ue_version": ue_version,
            "custom_version": customs,
            "blueprint": blueprint,
        }, offset + bytes_read

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        return (
            b"GVAS"
            + GVASSaveVersionSerde.from_dict(data["save_version"])
            + GVASUEVersionSerde.from_dict(data["ue_version"])
            + GVASCustomVersionsSerde.from_dict(data["custom_version"])
            + write_string(data["blueprint"])
        )
