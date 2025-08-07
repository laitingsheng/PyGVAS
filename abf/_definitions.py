from typing import ClassVar

from gvas.values import GVASByteValue, GVASCustomStructValue, GVASEnumValue


class GVASBodyLimbHealth(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/BodyLimbHealth_Struct"
    _GUID: ClassVar[str] = "8bc2938b-4cb1-33c4-160e-01b73a0c5f43"
    _NAME: ClassVar[str] = "BodyLimbHealth_Struct"


class GVASCharacterSave(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_CharacterSave_Struct"
    _GUID: ClassVar[str] = "b646f4d9-4fe4-eb1e-053d-3e95b840a395"
    _NAME: ClassVar[str] = "SaveData_CharacterSave_Struct"


class GVASCharacterStatsSave(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/CharacterStatsSave_Struct"
    _GUID: ClassVar[str] = "a99b517b-446f-f5f5-ae13-df8bff0284d3"
    _NAME: ClassVar[str] = "CharacterStatsSave_Struct"


class GVASCharacterSkill(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/Abiotic_CharacterSkill_Struct"
    _GUID: ClassVar[str] = "30a60449-4ede-1014-e008-b1bce1c03ba8"
    _NAME: ClassVar[str] = "Abiotic_CharacterSkill_Struct"


class GVASCoreCompendiumEntryRowHandle(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _GUID: ClassVar[str] = ""
    _NAME: ClassVar[str] = "CompendiumEntryRowHandle"


class GVASCoreCompendiumKillCount(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _GUID: ClassVar[str] = ""
    _NAME: ClassVar[str] = "CompendiumKillCount"


class GVASCoreDataTableRowHandle(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/Engine"
    _GUID: ClassVar[str] = ""
    _NAME: ClassVar[str] = "DataTableRowHandle"


class GVASCoreDynamicProperty(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _GUID: ClassVar[str] = ""
    _NAME: ClassVar[str] = "DynamicProperty"


class GVASCoreDynamicPropertyType(GVASEnumValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "EDynamicProperty"


class GVASInventoryData(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct"
    _GUID: ClassVar[str] = "d775c660-49d1-f198-30bd-428d3199792d"
    _NAME: ClassVar[str] = "Abiotic_InventoryChangeableDataStruct"


class GVASInventorySlot(GVASCustomStructValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/Abiotic_InventoryItemSlotStruct"
    _GUID: ClassVar[str] = "1d38c0c6-4203-e8c2-cbf4-8bb04777befe"
    _NAME: ClassVar[str] = "Abiotic_InventoryItemSlotStruct"


class GVASLiquidType(GVASByteValue):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/E_LiquidType"
    _NAME: ClassVar[str] = "E_LiquidType"
