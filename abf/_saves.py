import struct
from typing import Any, final, override

from gvas import GVASSave
from gvas.utils import read_string, write_string
from gvas.v3.headers import GVASHeaderSerde
from gvas.v3.properties import GVASBlueprintStructPropertySerde


class ABFCommonHeaderSerde(GVASHeaderSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        result, offset = super().from_bytes(data, offset)
        if struct.unpack_from("<B", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at {offset}")
        return result, offset + 1

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        return super().from_dict(data) + struct.pack("<B", 0)


class ABFCommonSave(GVASSave):
    __slots__ = ()

    _BODY_SERDE = GVASBlueprintStructPropertySerde
    _HEADER_SERDE = ABFCommonHeaderSerde


class ABFPlayerHeaderSerde(GVASHeaderSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        result, offset = super().from_bytes(data, offset)
        flag, size, padding = struct.unpack_from("<IIB", data, offset)
        if flag != 1:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 8
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        result["bodysize"] = size - 1
        return result, offset + 1

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        return super().from_dict(data) + struct.pack("<IIB", 1, data["bodysize"] + 1, 0)


class ABFPlayerSave(GVASSave):
    __slots__ = ()

    _BODY_SERDE = GVASBlueprintStructPropertySerde
    _HEADER_SERDE = ABFPlayerHeaderSerde


class ABFWorldHeaderSerde(GVASHeaderSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        result, offset = super().from_bytes(data, offset)
        attribute, bytes_read = read_string(data, offset)
        if attribute != "ABF_SAVE_VERSION":
            raise ValueError(f"Invalid attribute at {offset}")
        offset += bytes_read
        version, flag, size, padding = struct.unpack_from("<IIIB", data, offset)
        if version != 3:
            raise ValueError(f"Invalid version at {offset}")
        offset += 4
        if flag != 1:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 8
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        result["bodysize"] = size - 1
        return result, offset + 1

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        return (
            super().from_dict(data)
            + write_string("ABF_SAVE_VERSION")
            + struct.pack("<IIIB", 3, 1, data["bodysize"] + 1, 0)
        )


class ABFWorldSave(GVASSave):
    __slots__ = ()

    _BODY_SERDE = GVASBlueprintStructPropertySerde
    _HEADER_SERDE = ABFWorldHeaderSerde
