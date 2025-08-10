from typing import Self, final

from .utils import read_string
from .versions import Any, GVASCustomVersions, GVASSaveVersion, GVASUEVersion


class GVASHeader:
    __slots__ = ("_blueprint", "_customs", "_save_version", "_ue_version")

    _blueprint: str
    _customs: GVASCustomVersions
    _save_version: GVASSaveVersion
    _ue_version: GVASUEVersion

    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        if data[:4] != b"GVAS":
            raise ValueError("Invalid GVAS header")
        self = cls.__new__(cls)
        offset = 4
        self._save_version, offset = GVASSaveVersion.parse(data, offset)
        self._ue_version, offset = GVASUEVersion.parse(data, offset)
        self._customs, offset = GVASCustomVersions.parse(data, offset)
        self._blueprint, bytes_read = read_string(data, offset)
        return self, offset + bytes_read

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    def to_json(self) -> dict[str, Any]:
        return {
            "ue_version": self._ue_version.to_json(),
            "save_version": self._save_version.to_json(),
            "customs": self._customs.to_json(),
            "blueprint": self._blueprint,
        }
