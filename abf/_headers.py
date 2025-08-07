import itertools
import struct
import uuid
from typing import Any, Self, final

from gvas.utils import read_string, write_string


class ABFPlayerSaveHeader:
    __slots__ = (
        "_blueprint",
        "_branch",
        "_customs",
        "_customs_version",
        "_save_version",
        "_ue_version",
    )

    _blueprint: str
    _branch: str
    _customs: dict[uuid.UUID, int]
    _customs_version: int
    _save_version: tuple[int, int, int]
    _ue_version: tuple[int, int, int, int, int]

    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        if data[:4] != b"GVAS":
            raise ValueError("Invalid GVAS header")
        self = cls.__new__(cls)
        offset = 4
        major, minor, patch = struct.unpack_from("<3L", data, offset)
        self._save_version = major, minor, patch
        offset += 12
        major, minor, patch, tweak, build = struct.unpack_from("<5H", data, offset)
        self._ue_version = major, minor, patch, tweak, build
        offset += 10
        self._branch, bytes_read = read_string(data, offset)
        offset += bytes_read
        self._customs_version, customs_count = struct.unpack_from("<2L", data, offset)
        offset += 8
        if customs_count > 0:
            self._customs = {
                uuid.UUID(bytes_le=custom_uuid): custom_version
                for custom_uuid, custom_version in itertools.batched(
                    struct.unpack_from(
                        "<" + "16sL" * customs_count,
                        data,
                        offset,
                    ),
                    2,
                )
            }
            offset += 20 * customs_count
        else:
            self._customs = {}
        self._blueprint, bytes_read = read_string(data, offset)
        offset += bytes_read
        return self, offset

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    def json(self) -> dict[str, Any]:
        return {
            "blueprint": self._blueprint,
            "customs": {
                "entries": {str(k): v for k, v in self._customs.items()},
                "version": self._customs_version,
            },
            "save_version": ".".join(map(str, self._save_version)),
            "ue_version": ".".join(map(str, self._ue_version)) + self._branch,
        }

    def unparse(self) -> bytes:
        return (
            b"GVAS" +
            struct.pack("<3L5H", *self._save_version, *self._ue_version) +
            write_string(self._branch) +
            struct.pack(
                "<2L" + "16sL" * len(self._customs),
                self._customs_version,
                len(self._customs),
                *(
                    arg
                    for custom_id, custom_version in self._customs.items()
                    for arg in (custom_id.bytes_le, custom_version)
                ),
            )
        )
