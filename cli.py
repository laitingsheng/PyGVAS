import json
import sys

from abf import GVASHeader
from gvas.utils import GVASCursor


class GVASBody(GVASCursor):
    __slots__ = (
        "_blueprint",
        "_version",
        "_value",
    )

    def __init__(self, data: bytes, offset: int) -> None:
        super(GVASBody, self).__init__(data, offset)

        self._blueprint = self._read_string()

        self._version, expected_size = self._read_uint32(2)
        self._advance(1)

        self._value: dict[str, object] = {}
        name = self._read_string()
        while name != "None":
            parsed_type = self._read_string()
            if name in self._value:
                raise ValueError(f"Duplicate field name {name} in root")
            self._value[name] = {
                "name": name,
                "type": parsed_type,
            } | getattr(self, f"_parse_{parsed_type}")()
            name = self._read_string()

    def json(self) -> object:
        return {
            "blueprint": self._blueprint,
            "version": self._version,
            "value": self._value,
        }

    def _parse_ArrayProperty(self) -> dict[str, object]:
        array_type = self._read_uint32(1)[0]
        if array_type != 1:
            raise ValueError(f"Unexpected array type {array_type}")
        element_type = self._read_string()
        return {
            "array_type": array_type,
            "element_type": element_type,
            "elements": getattr(self, f"_parse_multiple_{element_type}")(),
        }

    def _parse_BoolProperty(self) -> dict[str, object]:
        self._advance(8)
        value = self._read_uint8(1)[0]
        if value == 0:
            return {"value": False}
        if value == 0x10:
            return {"value": True}
        raise ValueError("Unexpected boolean value")

    def _parse_ByteProperty(self) -> dict[str, object]:
        subtype = self._read_uint32(1)[0]
        if subtype == 1:
            name = self._read_string()
            if self._read_uint32(1)[0] != 1:
                raise ValueError("Invalid blueprint index")
            blueprint = self._read_string()
            self._advance(4)
            expected_size = self._read_uint32(1)[0]
            self._advance(1)
            value = self._read_string()
            return {
                "subtype": subtype,
                "name": name,
                "blueprint": blueprint,
                "value": value,
            }
        raise ValueError(f"Unexpected byte property subtype {subtype}")

    def _parse_DoubleProperty(self) -> dict[str, object]:
        self._advance(4)
        if self._read_uint32(1)[0] != 8:
            raise ValueError("Unexpected double size")
        self._advance(1)
        return {
            "value": self._read_float64(1)[0],
        }

    def _parse_FloatProperty(self) -> dict[str, object]:
        self._advance(4)
        if self._read_uint32(1)[0] != 4:
            raise ValueError("Unexpected float size")
        self._advance(1)
        return {
            "value": self._read_float32(1)[0],
        }

    def _parse_IntProperty(self) -> dict[str, object]:
        self._advance(4)
        if self._read_uint32(1)[0] != 4:
            raise ValueError("Unexpected int size")
        self._advance(1)
        return {
            "value": self._read_int32(1)[0],
        }

    def _parse_NameProperty(self) -> dict[str, object]:
        self._advance(4)
        expected_size = self._read_uint32(1)[0]
        self._advance(1)
        if expected_size == 4:
            if self._read_string() == "":
                return {"value": ""}
            raise ValueError("Unexpected string size")
        value = self._read_string()
        if len(value) != expected_size - 5:
            raise ValueError("String size mismatch")
        return {"value": value}

    _parse_StrProperty = _parse_NameProperty

    def _parse_StructProperty(self) -> dict[str, object]:
        subtype = self._read_uint32(1)[0]
        short_name = self._read_string()
        if self._read_uint32(1)[0] != 1:
            raise ValueError("Invalid blueprint index")
        blueprint = self._read_string()
        if subtype == 2:
            if self._read_uint32(1)[0] != 0:
                raise ValueError("Invalid GUID index")
            guid = self._read_string()
            self._advance(4)
            expected_size = self._read_uint32(1)[0]
            self._advance(1)
            value: dict[str, object] = {}
            name = self._read_string()
            while name != "None":
                parsed_type = self._read_string()
                if name in value:
                    raise ValueError(f"Duplicate field name {name} in struct")
                value[name] = {
                    "name": name,
                    "type": parsed_type,
                } | getattr(self, f"_parse_{parsed_type}")()
                name = self._read_string()
        elif subtype == 1:
            guid = None
            self._advance(4)
            value = getattr(self, f"_parse_builtin_{short_name}")()
        else:
            raise ValueError(f"Unexpected struct subtype {subtype}")
        return {
            "subtype": subtype,
            "short_name": short_name,
            "blueprint": blueprint,
            "guid": guid,
            "value": value,
        }

    def _parse_TextProperty(self) -> dict[str, object]:
        self._advance(4)
        expected_size = self._read_uint32(1)[0]
        self._advance(5)
        if self._read_uint8(1)[0] != 0x0b:
            raise ValueError("Unexpected text property boundary")
        table = self._read_string()
        reference = self._read_string()
        if len(table) + len(reference) != expected_size - 15:
            raise ValueError("Text size mismatch")
        return {
            "table": table,
            "reference": reference,
        }

    def _parse_builtin_CompendiumEntryRowHandle(self) -> dict[str, object]:
        expected_size = self._read_uint32(1)[0]
        self._advance(1)
        if self._read_string() != "RowName":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "NameProperty":
            raise ValueError("Unexpected attribute type")
        attribute = self._parse_NameProperty()
        if self._read_string() != "None":
            raise ValueError("Unterminated CompendiumEntryRowHandle")
        return {
            "RowName": {
                "name": "RowName",
                "type": "NameProperty",
            } | attribute,
        }

    def _parse_builtin_CompendiumKillCount(self) -> dict[str, object]:
        if self._read_string() != "CompendiumRow":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "StructProperty":
            raise ValueError("Unexpected attribute type")
        attribute1 = {
            "name": "CompendiumRow",
            "type": "StructProperty",
            "value": self._parse_StructProperty(),
        }
        if self._read_string() != "Count":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "IntProperty":
            raise ValueError("Unexpected attribute type")
        attribute2 = {
            "name": "Count",
            "type": "IntProperty",
            "value": self._parse_IntProperty(),
        }
        if self._read_string() != "None":
            raise ValueError("Unterminated CompendiumKillCount")
        return {
            "CompendiumRow": attribute1,
            "Count": attribute2,
        }

    def _parse_builtin_DataTableRowHandle(self) -> dict[str, object]:
        expected_size = self._read_uint32(1)[0]
        self._advance(1)
        if self._read_string() != "DataTable":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "ObjectProperty":
            raise ValueError("Unexpected attribute type")
        attribute1 = {
            "name": "DataTable",
            "type": "ObjectProperty",
            "value": self._parse_StrProperty(),
        }
        if self._read_string() != "RowName":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "NameProperty":
            raise ValueError("Unexpected attribute type")
        attribute2 = {
            "name": "RowName",
            "type": "NameProperty",
            "value": self._parse_NameProperty(),
        }
        if self._read_string() != "None":
            raise ValueError("Unterminated DataTableRowHandle")
        return {
            "DataTable": attribute1,
            "RowName": attribute2,
        }

    def _parse_builtin_DynamicProperty(self) -> dict[str, object]:
        if self._read_string() != "Key":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "EnumProperty":
            raise ValueError("Unexpected attribute type")
        subtype = self._read_uint32(1)[0]
        if subtype == 2:
            name = self._read_string()
            if self._read_uint32(1)[0] != 1:
                raise ValueError("Invalid blueprint index")
            blueprint = self._read_string()
            self._advance(4)
            if self._read_string() != "ByteProperty":
                raise ValueError("Unexpected enum type")
            attribute1 = {
                "name": "Key",
                "type": "EnumProperty",
                "enum_name": name,
                "enum_blueprint": blueprint,
                "subtype": subtype,
                "value": self._parse_StrProperty(),
            }
        else:
            raise ValueError(f"Unexpected enum subtype {subtype}")
        if self._read_string() != "Value":
            raise ValueError("Unexpected attribute name")
        if self._read_string() != "IntProperty":
            raise ValueError("Unexpected attribute type")
        attribute2 = {
            "name": "Value",
            "type": "IntProperty",
            "value": self._parse_IntProperty(),
        }
        if self._read_string() != "None":
            raise ValueError("Unterminated DynamicProperty")
        return {
            "Key": attribute1,
            "Value": attribute2,
        }

    def _parse_builtin_GameplayTagContainer(self) -> dict[str, object]:
        if self._read_uint32(1)[0] != 4:
            raise ValueError("Unexpected GameplayTagContainer size")
        if self._read_uint32(1)[0] != 8:
            raise ValueError("Unexpected GameplayTagContainer type")
        self._advance(1)
        attribute_name = self._read_string()
        if self._read_string() != "ArrayProperty":
            raise ValueError("Unexpected attribute type")
        attribute = self._parse_ArrayProperty()
        return {
            attribute_name: {
                "name": attribute_name,
                "type": "ArrayProperty",
            } | attribute,
        }

    def _parse_builtin_Rotator(self) -> dict[str, object]:
        expected_size = self._read_uint32(1)[0]
        unit_size = self._read_uint8(1)[0]
        if expected_size % unit_size != 0:
            raise ValueError("Invalid rotator arrangement")
        count = expected_size // unit_size
        if count != 3:
            raise ValueError("Invalid rotator size")
        if unit_size == 4:
            x, y, z = self._read_float32(3)
        elif unit_size == 8:
            x, y, z = self._read_float64(3)
        else:
            raise ValueError(f"Unexpected rotator FP precision {unit_size}")
        return {
            "double": unit_size == 8,
            "x": x,
            "y": y,
            "z": z,
        }

    def _parse_builtin_Vector(self) -> dict[str, object]:
        expected_size = self._read_uint32(1)[0]
        unit_size = self._read_uint8(1)[0]
        if expected_size % unit_size != 0:
            raise ValueError("Invalid vector arrangement")
        count = expected_size // unit_size
        if count != 3:
            raise ValueError("Invalid vector size")
        if unit_size == 4:
            x, y, z = self._read_float32(3)
        elif unit_size == 8:
            x, y, z = self._read_float64(3)
        else:
            raise ValueError(f"Unexpected vector FP precision {unit_size}")
        return {
            "double": unit_size == 8,
            "x": x,
            "y": y,
            "z": z,
        }

    def _parse_multiple_BoolProperty(self) -> dict[str, object]:
        self._advance(4)
        expected_size = self._read_uint32(1)[0]
        self._advance(1)
        count = self._read_uint32(1)[0]
        if count != expected_size - 4:
            raise ValueError("Multiple booleans size mismatch")
        values: list[bool] = []
        for value in self._read_uint8(count):
            if value == 0:
                values.append(False)
            elif value == 0x1:
                values.append(True)
            else:
                raise ValueError("Unexpected boolean value in multiple BoolProperty")
        return {
            "values": values,
        }

    def _parse_multiple_NameProperty(self) -> dict[str, object]:
        self._advance(4)
        expected_size = self._read_uint32(1)[0]
        self._advance(1)
        count = self._read_uint32(1)[0]
        values: list[str] = []
        for _ in range(count):
            values.append(self._read_string())
        return {
            "values": values,
        }

    def _parse_multiple_StructProperty(self) -> dict[str, object]:
        subtype = self._read_uint32(1)[0]
        short_name = self._read_string()
        if self._read_uint32(1)[0] != 1:
            raise ValueError("Invalid blueprint index")
        blueprint = self._read_string()
        if subtype == 2:
            if self._read_uint32(1)[0] != 0:
                raise ValueError("Invalid GUID index")
            guid = self._read_string()
            self._advance(4)
            expected_size = self._read_uint32(1)[0]
            self._advance(1)
            count = self._read_uint32(1)[0]
            values: list[object] = []
            for _ in range(count):
                value: dict[str, object] = {}
                name = self._read_string()
                while name != "None":
                    parsed_type = self._read_string()
                    if name in value:
                        raise ValueError(f"Duplicate field name {name} in struct")
                    value[name] = {
                        "name": name,
                        "type": parsed_type,
                    } | getattr(self, f"_parse_{parsed_type}")()
                    name = self._read_string()
                values.append(value)
        elif subtype == 1:
            guid = None
            self._advance(4)
            expected_size = self._read_uint32(1)[0]
            self._advance(1)
            count = self._read_uint32(1)[0]
            values: list[object] = []
            for _ in range(count):
                values.append(getattr(self, f"_parse_builtin_{short_name}")())
        else:
            raise ValueError(f"Unexpected struct subtype {subtype}")
        return {
            "subtype": subtype,
            "short_name": short_name,
            "blueprint": blueprint,
            "guid": guid,
            "values": values,
        }


def _main(entry: str, filename: str) -> None:
    with open(filename, "rb") as f:
        data = f.read()

    header, offset = GVASHeader.parse(data, 0)
    body = GVASBody(data, offset)

    with open(f"gvas.json", "w", encoding="utf-8") as f:
        json.dump({
            "header": header.json(),
            "body": body.json(),
        }, f, indent=2)


if __name__ == "__main__":
    _main(*sys.argv)
