import json
import struct
from abc import abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Self, final


class GVASSerde:
    __slots__ = ()

    @final
    def __new__(cls) -> Self:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes, offset: int) -> tuple[Any, int]:
        raise NotImplementedError(cls.__name__)

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Any) -> bytes:
        raise NotImplementedError(cls.__name__)

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)


class GVASSave:
    __slots__ = ("header", "body")

    _BODY_SERDE: ClassVar[type[GVASSerde]]
    _HEADER_SERDE: ClassVar[type[GVASSerde]]

    body: Any
    header: Any

    @final
    @classmethod
    def from_binary_file(cls, filepath: Path) -> Self:
        with filepath.open("rb") as f:
            data = f.read()
        header, offset = cls._HEADER_SERDE.from_bytes(data, 0)
        bodysize = header.get("bodysize")
        if bodysize is not None and offset + bodysize != len(data):
            raise ValueError(f"Invalid body size {bodysize} at {offset}")
        body, offset = cls._BODY_SERDE.from_bytes(data, offset)
        if struct.unpack_from("<I", data, offset)[0] != 0:
            raise ValueError(f"Invalid ending at {offset}")
        offset += 4
        if offset != len(data):
            raise ValueError(f"More bytes are available at {offset}")
        self = cls.__new__(cls)
        self.header = header
        self.body = body
        return self

    @final
    @classmethod
    def from_json_file(cls, filepath: Path) -> Self:
        with filepath.open("r", encoding="utf-8") as f:
            data = json.load(f)
        header = data.pop("header")
        body = data.pop("body")
        if data:
            raise ValueError(f"Unknown keys in JSON: {', '.join(data.keys())}")
        self = cls.__new__(cls)
        self.header = header
        self.body = body
        return self

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)

    @final
    def to_binary_file(self, filepath: Path) -> None:
        body = self._BODY_SERDE.from_dict(self.body) + struct.pack("<I", 0)
        self.header["bodysize"] = len(body)
        header = self._HEADER_SERDE.from_dict(self.header)
        with filepath.open("wb") as f:
            f.write(header)
            f.write(body)

    @final
    def to_json_file(self, filepath: Path) -> None:
        with filepath.open("w", encoding="utf-8") as f:
            json.dump({"header": self.header, "body": self.body}, f, indent=2)
