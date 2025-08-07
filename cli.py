import json
import struct
import sys

import abf
from gvas.values import GVASCustomStructValue


def _main(
    entry: str,
    filename: str,
) -> None:
    with open(filename, "rb") as f:
        data = f.read()

    header, offset = abf.ABFPlayerSaveHeader.parse(data, 0)

    flag, size, unit_width = struct.unpack_from("<LLB", data, offset)
    if flag != 1:
        raise ValueError(f"Invalid flag at {offset}")
    offset += 9
    expected_offset = offset + size
    body, offset = GVASCustomStructValue.parse(unit_width, data, offset)
    if offset + 4 != expected_offset - 1:
        raise ValueError(f"Invalid offset at {offset}")
    offset += 4
    print(body)

    with open(f"gvas.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "header": header.json(),
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    _main(*sys.argv)
