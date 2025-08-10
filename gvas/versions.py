from typing import Any, Self, final
import itertools
import struct
import uuid

from .utils import read_string


class GVASSaveVersion:
    __slots__ = ("_major", "_minor", "_patch")

    _major: int
    _minor: int
    _patch: int

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @final
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        major, minor, patch = struct.unpack_from("<3I", data, offset)
        self = cls.__new__(cls)
        self._major = major
        self._minor = minor
        self._patch = patch
        return self, offset + 12

    @final
    def to_json(self) -> dict[str, Any]:
        return {"major": self._major, "minor": self._minor, "patch": self._patch}


class GVASUEVersion:
    __slots__ = ("_major", "_minor", "_patch", "_tweak", "_build", "_branch")

    _major: int
    _minor: int
    _patch: int
    _tweak: int
    _build: int
    _branch: str

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @final
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        major, minor, patch, tweak, build = struct.unpack_from("<5H", data, offset)
        offset += 10
        branch, bytes_read = read_string(data, offset)
        offset += bytes_read
        self = cls.__new__(cls)
        self._major = major
        self._minor = minor
        self._patch = patch
        self._tweak = tweak
        self._build = build
        self._branch = branch
        return self, offset

    @final
    def to_json(self) -> dict[str, Any]:
        return {
            "major": self._major,
            "minor": self._minor,
            "patch": self._patch,
            "tweak": self._tweak,
            "build": self._build,
            "branch": self._branch,
        }


class GVASCustomVersions:
    __slots__ = ("_versions",)

    _versions: dict[uuid.UUID, int]

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @final
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        customs_version, customs_count = struct.unpack_from("<2I", data, offset)
        if customs_version != 3:
            raise ValueError(f"Expected customs version 3, got {customs_version}")
        offset += 8
        self = cls.__new__(cls)
        if customs_count > 0:
            self._versions = {
                uuid.UUID(bytes_le=custom_uuid): custom_version
                for custom_uuid, custom_version in itertools.batched(
                    struct.unpack_from("<" + "16sI" * customs_count, data, offset), 2
                )
            }
            offset += 20 * customs_count
        else:
            self._versions = {}
        return self, offset

    @final
    def to_json(self) -> dict[str, Any]:
        return {str(k): v for k, v in self._versions.items()}
