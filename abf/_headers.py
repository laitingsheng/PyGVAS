import struct
from typing import Any, Self, final, override

from gvas.headers import GVASHeader
from gvas.utils import read_string


class ABFPlayerSaveHeader(GVASHeader):
    __slots__ = ("size",)

    size: int

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self, offset = super().parse(data, offset)
        flag, size, padding = struct.unpack_from("<IIB", data, offset)
        if flag != 1:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 8
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        self.size = size - 1
        return self, offset + 1

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {"size": self.size}


class ABFWorldSaveHeader(GVASHeader):
    __slots__ = ("size",)

    size: int
    _blueprint_version: int

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self, offset = super().parse(data, offset)
        attribute, bytes_read = read_string(data, offset)
        if attribute != "ABF_SAVE_VERSION":
            raise ValueError(f"Invalid attribute at {offset}")
        offset += bytes_read
        if struct.unpack_from("<I", data, offset)[0] != 3:
            raise ValueError(f"Invalid version at {offset}")
        offset += 4
        flag, size, padding = struct.unpack_from("<IIB", data, offset)
        if flag != 1:
            raise ValueError(f"Invalid flag at {offset}")
        offset += 8
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        self.size = size - 1
        return self, offset + 1

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return super().to_json() | {"size": self.size}
