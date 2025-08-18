from typing import Any, Iterable
from uuid import UUID

from ._utils import create_changeable_data, create_cooking_data, create_datatable_row_handle


def create_empty_item() -> dict[str, dict[str, Any]]:
    return {
        "ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B": create_datatable_row_handle(
            datatable="/Game/Blueprints/Items/ItemTable_Pickups.ItemTable_Pickups",
            rowname="Empty",
        ),
        "ChangeableData_12_2B90E1F74F648135579D39A49F5A2313": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct",
                "name": "Abiotic_InventoryChangeableDataStruct",
                "guid": "d775c660-49d1-f198-30bd-428d3199792d",
            },
            "value": create_changeable_data(stack=0),
        },
    }


def create_global_item(
    asset_id: UUID,
    name: str,
    stack: int = 1,
    ammo: int | None = None,
    liquid: int = 0,
    variant: tuple[str, str] = ("", "None"),
    tags: Iterable[str] = (),
    portions: int = 1,
) -> dict[str, dict[str, Any]]:
    return {
        "ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B": create_datatable_row_handle(
            datatable="/Game/Blueprints/Items/ItemTable_Global.ItemTable_Global",
            rowname=name,
        ),
        "ChangeableData_12_2B90E1F74F648135579D39A49F5A2313": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct",
                "name": "Abiotic_InventoryChangeableDataStruct",
                "guid": "d775c660-49d1-f198-30bd-428d3199792d",
            },
            "value": create_changeable_data(
                asset_id=asset_id,
                stack=stack,
                ammo=ammo,
                liquid=liquid,
                variant=variant,
                tags=tags,
                portions=portions,
            ),
        },
    }


def create_plant_proxy(
    index: int,
    asset_id: UUID,
    plant_name: str,
) -> dict[str, dict[str, Any]]:
    return {
        "SpotIndex_75_9396897F4B2435CCF9B5909D8FFDF3B2": {
            "type": {
                "type": "IntProperty",
            },
            "value": index,
        },
        "ChangeableData_72_4C9675D849FC210B33DB648A3249A0E0": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct",
                "name": "Abiotic_InventoryChangeableDataStruct",
                "guid": "d775c660-49d1-f198-30bd-428d3199792d",
            },
            "value": create_changeable_data(asset_id=asset_id, plant_proxy=True),
        },
        "ItemRow_81_75819F45465D9DA0D3BF64B9C00E1D92": create_datatable_row_handle(
            datatable="/Game/Blueprints/Items/ItemTable_Plants.ItemTable_Plants",
            rowname=plant_name,
        ),
        "CookingData_60_6DEA84C54D2A902875B23580EAEA39BA": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Saves/SaveData/SaveData_Cooking_Struct",
                "name": "SaveData_Cooking_Struct",
                "guid": "406f5941-46da-6c91-1066-549ac23e760c",
            },
            "value": create_cooking_data(),
        },
        "TimerData_66_6D089E0745B138F4F3ED42BD7C99CC2F": {
            "type": {
                "type": "ArrayProperty",
            },
            "value": {
                "type": {
                    "type": "DoubleProperty",
                },
                "values": [],
            },
        },
    }


def extract_proxy_item_asset_id(item: dict[str, dict[str, Any]]) -> UUID:
    data = item.pop("ChangeableData_72_4C9675D849FC210B33DB648A3249A0E0").pop("value")
    asset_id = data.pop("AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB").pop("value")
    return UUID(asset_id)


def get_item_asset_id(item: dict[str, dict[str, Any]]) -> UUID | None:
    data = item["ChangeableData_12_2B90E1F74F648135579D39A49F5A2313"]["value"]
    asset_id = data["AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB"]["value"]
    return None if asset_id == "-1" else UUID(asset_id)
