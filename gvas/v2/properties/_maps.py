import struct
from typing import Any, ClassVar, override

from ...utils import read_string
from ._base import GVASPropertySerde


_REGISTRY: dict[tuple[str, str], type[GVASPropertySerde]] = {}


class GVASMapPropertySerde(GVASPropertySerde):
    __slots__ = ()

    _KEY_TYPE: ClassVar[str]
    _TYPE = "MapProperty"
    _VALUE_TYPE: ClassVar[str]

    @override
    def __init_subclass__(cls) -> None:
        if not hasattr(cls, "_KEY_TYPE"):
            raise ValueError(f"{cls.__name__} does not have a key type")
        if not hasattr(cls, "_VALUE_TYPE"):
            raise ValueError(f"{cls.__name__} does not have a value type")
        if (cls._KEY_TYPE, cls._VALUE_TYPE) in _REGISTRY:
            raise ValueError(f"Duplicate map property {cls._KEY_TYPE} to {cls._VALUE_TYPE}")
        _REGISTRY[(cls._KEY_TYPE, cls._VALUE_TYPE)] = cls

    @classmethod
    @override
    def from_bytes(cls, data: bytes, offset: int) -> tuple[list[tuple[Any, Any]], int]:
        key_serde = GVASPropertySerde.get_type(cls._KEY_TYPE)
        value_serde = GVASPropertySerde.get_type(cls._VALUE_TYPE)
        padding, count = struct.unpack_from("<II", data, offset)
        if padding != 0:
            raise ValueError(f"Invalid padding at {offset}")
        offset += 8
        values: list[tuple[Any, Any]] = []
        for _ in range(count):
            key, offset = key_serde._key_from_bytes(data, offset)
            value, offset = value_serde._value_from_bytes(data, offset)
            values.append((key, value))
        return values, offset

    @classmethod
    @override
    def _header_from_bytes(cls, data: bytes, offset: int) -> tuple[type[GVASPropertySerde], int]:
        key_type, bytes_read = read_string(data, offset)
        offset += bytes_read
        value_type, bytes_read = read_string(data, offset)
        offset += bytes_read
        flag = struct.unpack_from("<B", data, offset)[0]
        if flag != 0:
            raise ValueError(f"Invalid flag at {offset}")
        property_serde = _REGISTRY.get((key_type, value_type))
        if property_serde is None:
            property_serde = type(
                f"GVASMapPropertySerde@{key_type}->{value_type}",
                (GVASMapPropertySerde,),
                {"__slots__": (), "_KEY_TYPE": key_type, "_VALUE_TYPE": value_type},
            )
        return property_serde, offset + 1

    @classmethod
    @override
    def _header_to_dict(cls) -> dict[str, str]:
        return {"key_type": cls._KEY_TYPE, "value_type": cls._VALUE_TYPE}
