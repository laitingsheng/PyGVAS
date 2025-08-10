from typing import Any, ClassVar, Self, final, override

from ..utils import read_string
from ._base import GVASTextValue


class GVASTextStringTable(GVASTextValue):
    __slots__ = ("_reference", "_table")

    _TYPE: ClassVar[int] = 11

    _reference: str
    _table: str

    @final
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self = cls.__new__(cls)

        self._table, bytes_read = read_string(data, offset)
        offset += bytes_read

        self._reference, bytes_read = read_string(data, offset)
        offset += bytes_read

        return self, offset

    @final
    @override
    def to_json(self) -> dict[str, Any]:
        return {"type": self._TYPE, "table": self._table, "reference": self._reference}
