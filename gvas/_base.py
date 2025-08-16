from abc import abstractmethod
from typing import Any, Self, final


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
    def from_json(cls, data: Any) -> bytes:
        raise NotImplementedError(cls.__name__)

    @final
    def __init__(self) -> None:
        raise NotImplementedError(self.__class__.__name__)
