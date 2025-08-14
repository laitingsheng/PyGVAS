import struct
from typing import Self, final, override

from gvas.headers import GVASHeader


class ESSaveHeader(GVASHeader):
    __slots__ = ()

    @classmethod
    @final
    @override
    def parse(cls, data: bytes, offset: int) -> tuple[Self, int]:
        self, offset = super().parse(data, offset)
        if struct.unpack_from("<B", data, offset)[0] != 0:
            raise ValueError(f"Invalid padding at {offset}")
        return self, offset + 1
