import itertools
import struct
import uuid
from typing import Any, final, override

from .._base import GVASSerde
from ..utils import read_string, write_string


@final
class GVASSaveVersionSerde(GVASSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        major, minor, patch = struct.unpack_from("<3I", data, offset)
        return {"major": major, "minor": minor, "patch": patch}, offset + 12

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        major = int(data["major"])
        minor = int(data["minor"])
        patch = int(data["patch"])
        return struct.pack("<3I", major, minor, patch)


@final
class GVASUEVersionSerde(GVASSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        major, minor, patch, tweak, build = struct.unpack_from("<5H", data, offset)
        offset += 10
        branch, bytes_read = read_string(data, offset)
        return {
            "major": major,
            "minor": minor,
            "patch": patch,
            "tweak": tweak,
            "build": build,
            "branch": branch,
        }, offset + bytes_read

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        major = int(data["major"])
        minor = int(data["minor"])
        patch = int(data["patch"])
        tweak = int(data["tweak"])
        build = int(data["build"])
        branch = str(data["branch"])
        return struct.pack("<5H", major, minor, patch, tweak, build) + write_string(branch)


@final
class GVASCustomVersionsSerde(GVASSerde):
    __slots__ = ()

    @classmethod
    @final
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[dict[str, Any], int]:
        version, count = struct.unpack_from("<2I", data, offset)
        if version != 3:
            raise ValueError(f"Invalid version at {offset}")
        offset += 8
        if count < 1:
            return {}, offset
        return {
            str(uuid.UUID(bytes_le=custom_uuid)): custom_version
            for custom_uuid, custom_version in itertools.batched(
                struct.unpack_from("<" + "16sI" * count, data, offset),
                2,
            )
        }, offset + 20 * count

    @classmethod
    @final
    @override
    def from_dict(cls, data: dict[str, Any]) -> bytes:
        return struct.pack(
            "<2I" + "16sI" * len(data),
            3,
            len(data),
            *itertools.chain.from_iterable((uuid.UUID(k).bytes_le, int(v)) for k, v in data.items()),
        )
