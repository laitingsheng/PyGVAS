import itertools
import struct


def read_string(data: bytes, offset: int) -> tuple[str, int]:
    length = struct.unpack_from("<I", data, offset)[0]
    if length < 1:
        return "", 4
    string_value = struct.unpack_from(f"<{length - 1}sx", data, offset + 4)[0].decode("utf-8")
    return string_value, 4 + length


def write_string(*strings: str) -> bytes:
    if not strings:
        return b""
    formats, args = zip(
        *(
            (f"I{len(encoded)}sx" if encoded else "I", (len(encoded) + 1, encoded) if encoded else (0,))
            for encoded in (value.encode("utf-8") for value in strings)
        ),
    )
    return struct.pack("<" + "".join(formats), *itertools.chain.from_iterable(args))
