from typing import ClassVar

from gvas.properties import (
    GVASArrayProperty,
    GVASBlueprintStructProperty,
    GVASByteProperty,
    GVASEnumProperty,
    GVASIntProperty,
    GVASNameProperty,
    GVASStructAttributes,
    GVASUniqueStructProperty,
)


def dummy() -> None:
    pass


class ABFByteDoorStates(GVASByteProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/E_DoorStates"
    _NAME: ClassVar[str] = "E_DoorStates"


class ABFByteLiquidType(GVASByteProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/E_LiquidType"
    _NAME: ClassVar[str] = "E_LiquidType"


class ABFByteNarrativeNPCStates(GVASByteProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/E_NarrativeNPCStates"
    _NAME: ClassVar[str] = "E_NarrativeNPCStates"


class ABFBytePowerTimerModes(GVASByteProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/E_PowerTimerModes"
    _NAME: ClassVar[str] = "E_PowerTimerModes"


class ABFEnumCookingState(GVASEnumProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "ECookingState"


class ABFEnumDynamicProperty(GVASEnumProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "EDynamicProperty"


class ABFEnumEBodyLimbs(GVASEnumProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "EBodyLimbs"


class ABFStructBodyLimbHealth(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/BodyLimbHealth_Struct"
    _GUID: ClassVar[str] = "8bc2938b-4cb1-33c4-160e-01b73a0c5f43"
    _NAME: ClassVar[str] = "BodyLimbHealth_Struct"


class ABFStructButton(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_ButtonStruct"
    _NAME: ClassVar[str] = "SaveData_ButtonStruct"
    _GUID: ClassVar[str] = "fd82a89b-4c35-6f9a-996a-c782ff846e7f"


class ABFStructCharacterSave(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_CharacterSave_Struct"
    _GUID: ClassVar[str] = "b646f4d9-4fe4-eb1e-053d-3e95b840a395"
    _NAME: ClassVar[str] = "SaveData_CharacterSave_Struct"


class ABFStructCharacterSkill(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/Abiotic_CharacterSkill_Struct"
    _GUID: ClassVar[str] = "30a60449-4ede-1014-e008-b1bce1c03ba8"
    _NAME: ClassVar[str] = "Abiotic_CharacterSkill_Struct"


class ABFStructCharacterStatsSave(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/CharacterStatsSave_Struct"
    _GUID: ClassVar[str] = "a99b517b-446f-f5f5-ae13-df8bff0284d3"
    _NAME: ClassVar[str] = "CharacterStatsSave_Struct"


class ABFStructCompendiumEntryRowHandle(
    GVASUniqueStructProperty, metaclass=GVASStructAttributes, row_name=("RowName", GVASNameProperty)
):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "CompendiumEntryRowHandle"


class ABFStructCompendiumKillCount(
    GVASUniqueStructProperty,
    metaclass=GVASStructAttributes,
    compendium_row=("CompendiumRow", ABFStructCompendiumEntryRowHandle),
    count=("Count", GVASIntProperty),
):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "CompendiumKillCount"


class ABFStructCooking(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Cooking_Struct"
    _NAME: ClassVar[str] = "SaveData_Cooking_Struct"
    _GUID: ClassVar[str] = "406f5941-46da-6c91-1066-549ac23e760c"


class ABFStructCorpseSave(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/CorpseSave_Struct"
    _NAME: ClassVar[str] = "CorpseSave_Struct"
    _GUID: ClassVar[str] = "ceede9f1-41fb-3f54-d8ce-d68e1d8bcc8c"


class ABFStructDeployable(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Deployable_Struct"
    _NAME: ClassVar[str] = "SaveData_Deployable_Struct"
    _GUID: ClassVar[str] = "8bd9d1f7-433e-82ec-cb4f-8a89f434945a"


class ABFStructDestructible(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Destructible_Struct"
    _NAME: ClassVar[str] = "SaveData_Destructible_Struct"
    _GUID: ClassVar[str] = "a4ce3ca6-447d-7197-9729-2e9ccfd05d1c"


class ABFStructDoorSave(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Door_Struct"
    _GUID: ClassVar[str] = "241768a8-4397-bb04-35ac-27afef98cf21"
    _NAME: ClassVar[str] = "SaveData_Door_Struct"


class ABFStructDroppedItem(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_DroppedItem_Struct"
    _NAME: ClassVar[str] = "SaveData_DroppedItem_Struct"
    _GUID: ClassVar[str] = "7f8b86de-4a89-6b63-555c-74815b42e3da"


class ABFStructDynamicProperty(
    GVASUniqueStructProperty,
    metaclass=GVASStructAttributes,
    key=("Key", ABFEnumDynamicProperty),
    value=("Value", GVASIntProperty),
):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "DynamicProperty"


class ABFStructElevator(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Elevator_Struct"
    _NAME: ClassVar[str] = "SaveData_Elevator_Struct"
    _GUID: ClassVar[str] = "69a1301f-4c43-7c95-e35c-888c24395505"


class ABFStructGlobalUnlocks(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_GlobalUnlocks_Struct"
    _NAME: ClassVar[str] = "SaveData_GlobalUnlocks_Struct"
    _GUID: ClassVar[str] = "541be988-4535-b43a-f0e1-a795de7ae3c7"


class ABFStructInventoryData(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct"
    _GUID: ClassVar[str] = "d775c660-49d1-f198-30bd-428d3199792d"
    _NAME: ClassVar[str] = "Abiotic_InventoryChangeableDataStruct"


class ABFStructInventorySlot(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/Abiotic_InventoryItemSlotStruct"
    _GUID: ClassVar[str] = "1d38c0c6-4203-e8c2-cbf4-8bb04777befe"
    _NAME: ClassVar[str] = "Abiotic_InventoryItemSlotStruct"


class ABFStructInventories(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Inventories_Struct"
    _NAME: ClassVar[str] = "SaveData_Inventories_Struct"
    _GUID: ClassVar[str] = "0244edbe-4db8-6a41-c277-93b7ebd71fdf"


class ABFStructItemProxy(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_ItemProxy_Struct"
    _NAME: ClassVar[str] = "SaveData_ItemProxy_Struct"
    _GUID: ClassVar[str] = "4db48c2d-4b24-823e-1232-2b9b840b0f09"


class ABFStructNPCState(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_NPCState_Struct"
    _NAME: ClassVar[str] = "SaveData_NPCState_Struct"
    _GUID: ClassVar[str] = "0d1386b5-4e88-51da-8ca6-60aebfea1e04"


class ABFStructPortal(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_PortalStruct"
    _NAME: ClassVar[str] = "SaveData_PortalStruct"
    _GUID: ClassVar[str] = "78627d38-4c23-49c2-1e71-f5ba7e49fff1"


class ABFStructPowerSockets(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_PowerSockets"
    _NAME: ClassVar[str] = "SaveData_PowerSockets"
    _GUID: ClassVar[str] = "5ff25b82-4753-4d5c-627d-408f513014fd"


class ABFStructResource(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Resource_Struct"
    _NAME: ClassVar[str] = "SaveData_Resource_Struct"
    _GUID: ClassVar[str] = "bb6bdbe0-4c26-60f1-babf-81b023ec9c7e"


class ABFStructSecurityDoor(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_SecurityDoor_Struct"
    _NAME: ClassVar[str] = "SaveData_SecurityDoor_Struct"
    _GUID: ClassVar[str] = "e2790163-4c08-ed0b-0549-538156c4ddbf"


class ABFStructTimeOfDay(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Data/TimeOfDay_Struct"
    _NAME: ClassVar[str] = "TimeOfDay_Struct"
    _GUID: ClassVar[str] = "464930cb-42f5-5750-717e-6eb8ecf0200b"


class ABFStructTram(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Tram"
    _NAME: ClassVar[str] = "SaveData_Tram"
    _GUID: ClassVar[str] = "303bbea0-4b7a-28bc-ddea-cdbceeb8c435"


class ABFStructTrigger(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Trigger_Struct"
    _NAME: ClassVar[str] = "SaveData_Trigger_Struct"
    _GUID: ClassVar[str] = "c8521d99-4885-6f39-607e-4086d2b96594"


class ABFStructUserEntitlements(
    GVASUniqueStructProperty, metaclass=GVASStructAttributes, entitlements=("Entitlements", GVASArrayProperty)
):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Script/AbioticFactor"
    _NAME: ClassVar[str] = "UserEntitlements"


class ABFStructVehicle(GVASBlueprintStructProperty):
    __slots__ = ()

    _BLUEPRINT: ClassVar[str] = "/Game/Blueprints/Saves/SaveData/SaveData_Vehicle_Struct"
    _NAME: ClassVar[str] = "SaveData_Vehicle_Struct"
    _GUID: ClassVar[str] = "b622a80e-4690-5416-4dcb-6cac86ce6d10"
