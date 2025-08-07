import struct
from typing import ClassVar, Self, final, override

from ._base import GVASProperty, GVASPropertyArray


class GVASBoolProperty(GVASProperty):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "BoolProperty"

    _value: bool

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, value = struct.unpack_from("<LLB", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != 0:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        self = cls.__new__(cls)
        if value == 0:
            self._value = False
        elif value == 0x10:
            self._value = True
        else:
            raise ValueError(f"Invalid value at {offset}")
        return self, offset + 1


class GVASBoolPropertyArray(GVASPropertyArray):
    __slots__ = (
        "_value",
    )

    _ACCEPT: ClassVar[str] = "BoolProperty"

    _value: list[bool]

    @final
    @override
    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        category, size, unit_width, count = struct.unpack_from("<LLBL", data, offset)
        if category != 0:
            raise ValueError(f"Invalid category at {offset}")
        offset += 4
        if size != count + 4:
            raise ValueError(f"Invalid size at {offset}")
        offset += 4
        if unit_width != 0:
            raise ValueError(f"Invalid unit width at {offset}")
        offset += 5
        self = cls.__new__(cls)
        self._value = []
        for value in struct.unpack_from(f"<{count}B", data, offset):
            if value == 0:
                self._value.append(False)
            elif value == 0x1:
                self._value.append(True)
            else:
                raise ValueError(f"Invalid value at {offset}")
            offset += 1
        return self, offset
