import itertools
import struct
import uuid
from typing import Any, Self


class GVASHeader:
    __slots__ = (
        "_branch",
        "_customs",
        "_customs_version",
        "_save_version",
        "_ue_version",
    )

    _branch: str
    _customs: dict[uuid.UUID, int]
    _customs_version: int
    _save_version: tuple[int, int, int]
    _ue_version: tuple[int, int, int, int, int]

    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        if data[:4] != b"GVAS":
            raise ValueError("Invalid GVAS header")

        obj = cls.__new__(cls)
        offset = 4

        major, minor, patch = map(int, struct.unpack_from("<3L", data, offset))
        obj._save_version = major, minor, patch
        offset += 12

        major, minor, patch, tweak, build = map(int, struct.unpack_from("<5H", data, offset))
        obj._ue_version = major, minor, patch, tweak, build
        offset += 10

        length = struct.unpack_from("<L", data, offset)[0]
        offset += 4
        if length > 0:
            obj._branch = struct.unpack_from(f"<{length - 1}sx", data, offset)[0].decode("utf-8")
            offset += length
        else:
            obj._branch = ""

        obj._customs_version, customs_count = list(
            map(int, struct.unpack_from("<2L", data, offset))
        )
        offset += 8
        if customs_count > 0:
            obj._customs = {
                uuid.UUID(bytes_le=custom_uuid): int(custom_version)
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
            obj._customs = {}

        return obj, offset

    def __init__(self) -> None:
        raise NotImplementedError

    def unparse(self) -> bytes:
        data = bytearray(b"GVAS")

        data.extend(struct.pack("<3L5H", *self._save_version, *self._ue_version))

        if self._branch:
            branch_bytes = self._branch.encode("utf-8")
            data.extend(struct.pack(f"<L{len(branch_bytes)}sx", len(branch_bytes) + 1, branch_bytes))
        else:
            data.extend(struct.pack("<L", 0))

        data.extend(struct.pack("<2L", self._customs_version, len(self._customs)))
        for custom_id, custom_version in self._customs.items():
            data.extend(struct.pack("<16sL", custom_id.bytes_le, custom_version))

        return bytes(data)

    def json(self) -> dict[str, Any]:
        return {
            "save_version": ".".join(map(str, self._save_version)),
            "ue_version": ".".join(map(str, self._ue_version)) + self._branch,
            "customs": {
                "version": self._customs_version,
                "entries": {
                    str(k): v
                    for k, v in self._customs.items()
                },
            },
        }
