import copy
import re
from typing import Any, Iterable
from uuid import UUID

from ._items import extract_proxy_item_asset_id
from ._maths import DIRECTIONS
from ._utils import create_changeable_data


DEPLOYED_BARREL = "Furniture", "Deployed_LiquidContainer_Barrel"
DEPLOYED_BED = "Furniture", "Deployed_Furniture_CraftedBed_T2"
DEPLOYED_CONTAINMENT = "Furniture", "Deployed_LeyakContainment"
DEPLOYED_FARM = "Farming", "GardenPlot_Large"
DEPLOYED_FREEZER = "Furniture", "Deployed_Freezer"
DEPLOYED_HAZARD_FRIDGE = "Furniture", "Deployed_Refrigerator_Hazard"
DEPLOYED_HAZARD_STORAGE = "Furniture", "Deployed_HazardCrate"
DEPLOYED_STORAGE = "Furniture", "Deployed_StorageCrate_Makeshift_T4"


def create_object_inventory(component: int) -> dict[str, dict[str, Any]]:
    return {
        "InventoryContent_3_62DE207642C4C366452A129C54F542F5": {
            "type": {
                "type": "ArrayProperty",
            },
            "value": {
                "type": {
                    "type": "StructProperty",
                    "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryItemSlotStruct",
                    "name": "Abiotic_InventoryItemSlotStruct",
                    "guid": "1d38c0c6-4203-e8c2-cbf4-8bb04777befe",
                },
                "values": [],
            },
        },
        "ComponentID_6_606002AC4D025212386B30ACD626A853": {
            "type": {
                "type": "IntProperty",
            },
            "value": component,
        },
    }


def deploy_facility_object(
    asset_id: UUID,
    blueprint: str,
    reference: str,
    actor: str,
    x: float,
    y: float,
    z: float,
    direction: str,
    liquid: int = 0,
    variant: tuple[str, str] = ("", "None"),
    tags: Iterable[str] = (),
    label: str = "",
    paint: int | None = None,
) -> dict[str, dict[str, Any]]:
    return {
        "Class_77_84FAE6234D772064CD9B659BA5046B1C": {
            "type": {
                "type": "SoftObjectProperty",
            },
            "value": {
                "blueprint": blueprint,
                "reference": reference,
            },
        },
        "ActorPath_164_90AA6DAB481E5DC2E125A3A94475F44D": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/CoreUObject",
                "name": "SoftObjectPath",
            },
            "value": {
                "blueprint": "/Game/Maps/Facility",
                "name": "Facility",
                "value": actor,
            },
        },
        "ChangableData_37_6153F4A94F01A776C108038B7F38E256": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct",
                "name": "Abiotic_InventoryChangeableDataStruct",
                "guid": "d775c660-49d1-f198-30bd-428d3199792d",
            },
            "value": create_changeable_data(
                asset_id=asset_id,
                liquid=liquid,
                variant=variant,
                tags=tags,
                paint=paint,
            ),
        },
        "DeployableDestroyed_56_80BF5DDE46C5F8C6E6CD9EBF6A695E5E": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "BrokeWhenPackaged_63_852033BB4713434A14C0D5B5792BA116": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "HasBeenPackaged_59_9C1C3E4D4D61B7BC4E7D13A1B993E1B0": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "Transform_50_85E8B13D40141C9B1308F4BB943BD753": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/CoreUObject",
                "name": "Transform",
            },
            "value": {
                "Rotation": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/CoreUObject",
                        "name": "Quat",
                    },
                    "value": copy.deepcopy(DIRECTIONS[direction]),
                },
                "Translation": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/CoreUObject",
                        "name": "Vector",
                    },
                    "value": {
                        "x": x,
                        "y": y,
                        "z": z,
                    },
                },
                "Scale3D": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/CoreUObject",
                        "name": "Vector",
                    },
                    "value": {
                        "x": 1.0,
                        "y": 1.0,
                        "z": 1.0,
                    },
                },
            },
        },
        "DeployedByPlayer_71_EA4E6F5C4DBE9C472BC1D1B3ADEE0205": {
            "type": {
                "type": "BoolProperty",
            },
            "value": True,
        },
        "ConstructionMode_82_B226CF9D4E57045A9835B39D8D7AF98D": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "ConstructionLevel_85_460528D64DD6D1712C19198BC316254B": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 9999.0,
        },
        "ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB": {
            "type": {
                "type": "ArrayProperty",
            },
            "value": {
                "type": {
                    "type": "StructProperty",
                    "blueprint": "/Game/Blueprints/Saves/SaveData/SaveData_Inventories_Struct",
                    "name": "SaveData_Inventories_Struct",
                    "guid": "0244edbe-4db8-6a41-c277-93b7ebd71fdf",
                },
                "values": [],
            },
        },
        "ActiveSeats_135_E030A01B4CB15C1F95700EA3945F2A85": {
            "type": {
                "type": "ArrayProperty",
            },
            "value": {
                "type": {
                    "type": "BoolProperty",
                },
                "values": [],
            },
        },
        "ItemProxies_149_E2E145CE4015C4EDFA89E2B0CE3F579A": {
            "type": {
                "type": "ArrayProperty",
            },
            "value": {
                "type": {
                    "type": "StructProperty",
                    "blueprint": "/Game/Blueprints/Saves/SaveData/SaveData_ItemProxy_Struct",
                    "name": "SaveData_ItemProxy_Struct",
                    "guid": "4db48c2d-4b24-823e-1232-2b9b840b0f09",
                },
                "values": [],
            },
        },
        "CustomTextDisplay_152_B59A50C74001B5D2234D9E9B0D7CAB7F": {
            "type": {
                "type": "StrProperty",
            },
            "value": label,
        },
        "FoundByPlayer_154_B3A0D3F6458C7DAD36E130B39DAEDBE3": {
            "type": {
                "type": "BoolProperty",
            },
            "value": True,
        },
        "Supports_158_FE0D33184131D1E1C73782B44057EB5C": {
            "type": {
                "type": "ArrayProperty",
            },
            "value": {
                "type": {
                    "type": "StructProperty",
                    "blueprint": "/Script/CoreUObject",
                    "name": "Vector",
                },
                "values": [],
            },
        },
        "NoResetVignette_161_C76AFFC84B04AA28B73A65836D6BB265": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "CustomSpawnedTime_169_BAD6DE0D42D4F78261A9128279F907FE": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": -1.0,
        },
    }


def form_deployed_object_identifier(object_type: str, name: str, hashtag: int) -> tuple[str, str, str]:
    return (
        f"/Game/Blueprints/DeployedObjects/{object_type}/{name}",
        f"{name}_C",
        f"PersistentLevel.{name}_C_{hashtag}",
    )


def get_object_asset_id(obj: dict[str, dict[str, Any]]) -> UUID | None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    asset_id = data["AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB"]["value"]
    return None if asset_id in ("", "-1") or asset_id.startswith("/Game/") else UUID(asset_id)


def object_extract_inventories(obj: dict[str, dict[str, Any]]) -> list[dict[str, dict[str, Any]]]:
    inventories = obj["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"]
    obj["ContainerInventories_110_3A680B7244ACB095D963B786D9BB6ECB"]["value"]["values"] = []
    return [
        item
        for inventory in inventories
        for item in inventory["InventoryContent_3_62DE207642C4C366452A129C54F542F5"]["value"]["values"]
        if item["ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B"]["value"]["RowName"]["value"].lower()
        not in ("", "empty", "none")
    ]


def object_extract_proxied_item_ids(obj: dict[str, dict[str, Any]]) -> list[UUID]:
    proxied_items = obj["ItemProxies_149_E2E145CE4015C4EDFA89E2B0CE3F579A"]["value"]["values"]
    obj["ItemProxies_149_E2E145CE4015C4EDFA89E2B0CE3F579A"]["value"]["values"] = []
    return [extract_proxy_item_asset_id(item) for item in proxied_items]


def object_fill(obj: dict[str, dict[str, Any]], liquid: int) -> None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    if liquid < 1:
        liquid = 0
    data["LiquidLevel_46_D6414A6E49082BC020AADC89CC29E35A"]["value"] = 0x7FFFFFFF if liquid else 0
    data["CurrentLiquid_19_3E1652F448223AAE5F405FB510838109"]["value"] = f"NewEnumerator{liquid}"


def object_label(obj: dict[str, dict[str, Any]], label: str) -> None:
    obj["CustomTextDisplay_152_B59A50C74001B5D2234D9E9B0D7CAB7F"]["value"] = label


def object_move(obj: dict[str, dict[str, Any]], x: float, y: float, z: float, direction: str) -> None:
    transformation = obj["Transform_50_85E8B13D40141C9B1308F4BB943BD753"]["value"]
    transformation["Rotation"]["value"] = copy.deepcopy(DIRECTIONS[direction])
    transformation["Translation"]["value"] = {
        "x": x,
        "y": y,
        "z": z,
    }


def object_paint(obj: dict[str, dict[str, Any]], paint: int | None) -> None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    dynamic_attributes = data["DynamicProperties_50_5C138DB145048726E8C0FEAC7C9600F7"]["value"]["values"]
    indices: list[int] = []
    for i, dynamic_attribute in enumerate(dynamic_attributes):
        if dynamic_attribute["Key"]["value"] == "PaintColor":
            indices.append(i)
    if paint is not None:
        if indices:
            dynamic_attributes[indices.pop()]["Value"]["value"] = paint
        else:
            dynamic_attributes.append(
                {
                    "Key": {
                        "type": {
                            "type": "EnumProperty",
                            "blueprint": "/Script/AbioticFactor",
                            "name": "EDynamicProperty",
                        },
                        "value": "PaintColor",
                    },
                    "Value": {
                        "type": {
                            "type": "IntProperty",
                        },
                        "value": paint,
                    },
                },
            )
    for index in reversed(indices):
        dynamic_attributes.pop(index)


_ACTOR_REGEX = re.compile(r"^PersistentLevel\.\w+?_(\d+)$")


def object_rename(obj: dict[str, dict[str, Any]], object_type: str, name: str) -> None:
    descriptor = obj["Class_77_84FAE6234D772064CD9B659BA5046B1C"]["value"]
    descriptor["blueprint"] = f"/Game/Blueprints/DeployedObjects/{object_type}/{name}"
    descriptor["reference"] = f"{name}_C"
    actor_path = obj["ActorPath_164_90AA6DAB481E5DC2E125A3A94475F44D"]["value"]
    matches = _ACTOR_REGEX.match(actor_path["value"])
    hashtag = 0x7FFFFF00 if matches is None else int(matches[1])
    actor_path["value"] = f"PersistentLevel.{name}_C_{hashtag}"


def object_repair(obj: dict[str, dict[str, Any]]) -> None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    data["CurrentItemDurability_4_24B4D0E64E496B43FB8D3CA2B9D161C8"]["value"] = 2e8
    data["MaxItemDurability_6_F5D5F0D64D4D6050CCCDE4869785012B"]["value"] = 2e5
    obj["DeployableDestroyed_56_80BF5DDE46C5F8C6E6CD9EBF6A695E5E"]["value"] = False
    obj["BrokeWhenPackaged_63_852033BB4713434A14C0D5B5792BA116"]["value"] = False
    obj["BrokeWhenPackaged_63_852033BB4713434A14C0D5B5792BA116"]["value"] = False
    obj["DeployedByPlayer_71_EA4E6F5C4DBE9C472BC1D1B3ADEE0205"]["value"] = True
    obj["ConstructionMode_82_B226CF9D4E57045A9835B39D8D7AF98D"]["value"] = False
    obj["ConstructionLevel_85_460528D64DD6D1712C19198BC316254B"]["value"] = 9999.0
    obj["FoundByPlayer_154_B3A0D3F6458C7DAD36E130B39DAEDBE3"]["value"] = True
    obj["Supports_158_FE0D33184131D1E1C73782B44057EB5C"]["value"]["values"] = []
    obj["NoResetVignette_161_C76AFFC84B04AA28B73A65836D6BB265"]["value"] = False
    obj["CustomSpawnedTime_169_BAD6DE0D42D4F78261A9128279F907FE"]["value"] = -1.0


def object_set_tags(obj: dict[str, dict[str, Any]], tags: Iterable[str]) -> None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    data["GameplayTags_45_1A018E824E25CC7BA608A6B2835209A1"]["value"] = list(tags)


def object_set_variant(obj: dict[str, dict[str, Any]], datatable: str, rowname: str) -> None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    variant = data["TextureVariantRow_28_1C7CF7A0441335E8AC4EA7B5CA91F636"]["value"]
    variant["DataTable"]["value"] = datatable
    variant["RowName"]["value"] = rowname
