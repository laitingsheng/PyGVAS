import struct
import uuid

class GVASCursor:
    __slots__ = (
        "_data",
        "offset",
    )

    def __init__(self, data: bytes, offset: int) -> None:
        self._data = data
        self.offset = offset

    def _advance(self, count: int) -> None:
        if any(self._data[self.offset : self.offset + count]):
            raise ValueError("Advancing cursor with non-zero bytes")
        self.offset += count

    def _read_uint8(self, count: int) -> list[int]:
        ret = list(map(int, struct.unpack_from(f"<{count}B", self._data, self.offset)))
        self.offset += count
        return ret

    def _read_uint16(self, count: int) -> list[int]:
        ret = list(map(int, struct.unpack_from(f"<{count}H", self._data, self.offset)))
        self.offset += 2 * count
        return ret

    def _read_uint32(self, count: int) -> list[int]:
        ret = list(map(int, struct.unpack_from(f"<{count}L", self._data, self.offset)))
        self.offset += 4 * count
        return ret

    def _read_int32(self, count: int) -> list[int]:
        ret = list(map(int, struct.unpack_from(f"<{count}l", self._data, self.offset)))
        self.offset += 4 * count
        return ret

    def _read_float32(self, count: int) -> list[float]:
        ret = list(map(float, struct.unpack_from(f"<{count}f", self._data, self.offset)))
        self.offset += 4 * count
        return ret

    def _read_float64(self, count: int) -> list[float]:
        ret = list(map(float, struct.unpack_from(f"<{count}d", self._data, self.offset)))
        self.offset += 8 * count
        return ret

    def _read_uuid128(self) -> uuid.UUID:
        ret = uuid.UUID(bytes_le=self._data[self.offset : self.offset + 16])
        self.offset += 16
        return ret

    def _read_string(self) -> str:
        length = struct.unpack_from("<1L", self._data, self.offset)[0]
        self.offset += 4
        if length < 1:
            return ""
        ret = self._data[self.offset : self.offset + length - 1].decode("utf-8")
        self.offset += length
        return ret
