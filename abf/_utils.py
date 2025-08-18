import copy
import math
import secrets
from typing import Any
from uuid import UUID


def create_asset_id() -> UUID:
    candidate = secrets.token_hex(16)
    return UUID(candidate[:8] + "4" + candidate[9:])


def create_facility_object(
    asset_id: UUID,
    blueprint: str,
    name: str,
    actor: str,
    rotation: dict[str, float],
    translation: dict[str, float],
    liquid: int = 0,
    paint: int | None = None,
) -> dict[str, dict[str, Any]]:
    dynamic_attributes: list[dict[str, Any]] = []
    if liquid < 1:
        liquid = 0
    if paint is not None:
        if paint < 0:
            paint = 13
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
    return {
        "Class_77_84FAE6234D772064CD9B659BA5046B1C": {
            "type": {
                "type": "SoftObjectProperty",
            },
            "value": {
                "blueprint": blueprint,
                "reference": name,
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
            "value": {
                "AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB": {
                    "type": {
                        "type": "StrProperty",
                    },
                    "value": asset_id.hex.upper(),
                },
                "CurrentItemDurability_4_24B4D0E64E496B43FB8D3CA2B9D161C8": {
                    "type": {
                        "type": "DoubleProperty",
                    },
                    "value": 1e8,
                },
                "MaxItemDurability_6_F5D5F0D64D4D6050CCCDE4869785012B": {
                    "type": {
                        "type": "DoubleProperty",
                    },
                    "value": 1e5,
                },
                "CurrentStack_9_D443B69044D640B0989FD8A629801A49": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 1,
                },
                "CurrentAmmoInMagazine_12_D68C190F4B2FA78A4B1D57835B95C53D": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 0,
                },
                "LiquidLevel_46_D6414A6E49082BC020AADC89CC29E35A": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 0x7FFFFFFF if liquid else 0,
                },
                "CurrentLiquid_19_3E1652F448223AAE5F405FB510838109": {
                    "type": {
                        "type": "ByteProperty",
                        "blueprint": "/Game/Blueprints/Data/E_LiquidType",
                        "name": "E_LiquidType",
                    },
                    "value": f"NewEnumerator{liquid}",
                },
                "TextureVariantRow_28_1C7CF7A0441335E8AC4EA7B5CA91F636": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/Engine",
                        "name": "DataTableRowHandle",
                    },
                    "value": {
                        "DataTable": {
                            "type": {
                                "type": "ObjectProperty",
                            },
                            "value": "",
                        },
                        "RowName": {
                            "type": {
                                "type": "NameProperty",
                            },
                            "value": "None",
                        },
                    },
                },
                "DynamicState_39_7597AC6549E292B931C61BB13C9E42EB": {
                    "type": {
                        "type": "BoolProperty",
                    },
                    "value": False,
                },
                "PlayerMadeString_42_CC0B72B24DBEAB2CC04454AAFFD4BBE9": {
                    "type": {
                        "type": "StrProperty",
                    },
                    "value": "",
                },
                "GameplayTags_45_1A018E824E25CC7BA608A6B2835209A1": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/GameplayTags",
                        "name": "GameplayTagContainer",
                    },
                    "value": [],
                },
                "DynamicProperties_50_5C138DB145048726E8C0FEAC7C9600F7": {
                    "type": {
                        "type": "ArrayProperty",
                    },
                    "value": {
                        "type": {
                            "type": "StructProperty",
                            "blueprint": "/Script/AbioticFactor",
                            "name": "DynamicProperty",
                        },
                        "values": dynamic_attributes,
                    },
                },
            },
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
                    "value": copy.deepcopy(rotation),
                },
                "Translation": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/CoreUObject",
                        "name": "Vector",
                    },
                    "value": copy.deepcopy(translation),
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
            "value": "",
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


def create_empty_item() -> dict[str, dict[str, Any]]:
    return {
        "ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/Engine",
                "name": "DataTableRowHandle",
            },
            "value": {
                "DataTable": {
                    "type": {
                        "type": "ObjectProperty",
                    },
                    "value": "/Game/Blueprints/Items/ItemTable_Pickups.ItemTable_Pickups",
                },
                "RowName": {
                    "type": {
                        "type": "NameProperty",
                    },
                    "value": "Empty",
                },
            },
        },
        "ChangeableData_12_2B90E1F74F648135579D39A49F5A2313": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct",
                "name": "Abiotic_InventoryChangeableDataStruct",
                "guid": "d775c660-49d1-f198-30bd-428d3199792d",
            },
            "value": {
                "AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB": {
                    "type": {
                        "type": "StrProperty",
                    },
                    "value": "-1",
                },
                "CurrentItemDurability_4_24B4D0E64E496B43FB8D3CA2B9D161C8": {
                    "type": {
                        "type": "DoubleProperty",
                    },
                    "value": 0.0,
                },
                "MaxItemDurability_6_F5D5F0D64D4D6050CCCDE4869785012B": {
                    "type": {
                        "type": "DoubleProperty",
                    },
                    "value": 0.0,
                },
                "CurrentStack_9_D443B69044D640B0989FD8A629801A49": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 0,
                },
                "CurrentAmmoInMagazine_12_D68C190F4B2FA78A4B1D57835B95C53D": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 0,
                },
                "LiquidLevel_46_D6414A6E49082BC020AADC89CC29E35A": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": -1,
                },
                "CurrentLiquid_19_3E1652F448223AAE5F405FB510838109": {
                    "type": {
                        "type": "ByteProperty",
                        "blueprint": "/Game/Blueprints/Data/E_LiquidType",
                        "name": "E_LiquidType",
                    },
                    "value": "NewEnumerator0",
                },
                "TextureVariantRow_28_1C7CF7A0441335E8AC4EA7B5CA91F636": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/Engine",
                        "name": "DataTableRowHandle",
                    },
                    "value": {
                        "DataTable": {
                            "type": {"type": "ObjectProperty"},
                            "value": "/Game/Blueprints/DataTables/Customization/DT_TextureVariants.DT_TextureVariants",
                        },
                        "RowName": {
                            "type": {
                                "type": "NameProperty",
                            },
                            "value": "None",
                        },
                    },
                },
                "DynamicState_39_7597AC6549E292B931C61BB13C9E42EB": {
                    "type": {
                        "type": "BoolProperty",
                    },
                    "value": False,
                },
                "PlayerMadeString_42_CC0B72B24DBEAB2CC04454AAFFD4BBE9": {
                    "type": {
                        "type": "StrProperty",
                    },
                    "value": "",
                },
                "GameplayTags_45_1A018E824E25CC7BA608A6B2835209A1": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/GameplayTags",
                        "name": "GameplayTagContainer",
                    },
                    "value": [],
                },
                "DynamicProperties_50_5C138DB145048726E8C0FEAC7C9600F7": {
                    "type": {
                        "type": "ArrayProperty",
                    },
                    "value": {
                        "type": {
                            "type": "StructProperty",
                            "blueprint": "/Script/AbioticFactor",
                            "name": "DynamicProperty",
                        },
                        "values": [],
                    },
                },
            },
        },
    }


def create_global_item(
    asset_id: UUID,
    name: str,
    stack: int = 1,
    ammo: int | None = None,
    liquid: int = 0,
) -> dict[str, dict[str, Any]]:
    dynamic_attributes: list[dict[str, Any]] = []
    if ammo is None:
        ammo_size = 0
    elif ammo < 0:
        ammo_size = 0x7FFFFFFF
    else:
        dynamic_attributes.append(
            {
                "Key": {
                    "type": {
                        "type": "EnumProperty",
                        "blueprint": "/Script/AbioticFactor",
                        "name": "EDynamicProperty",
                    },
                    "value": "AmmoType",
                },
                "Value": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": ammo,
                },
            },
        )
        ammo_size = 0x7FFFFFFF
    if liquid < 1:
        liquid = 0
    return {
        "ItemDataTable_18_BF1052F141F66A976F4844AB2B13062B": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/Engine",
                "name": "DataTableRowHandle",
            },
            "value": {
                "DataTable": {
                    "type": {
                        "type": "ObjectProperty",
                    },
                    "value": "/Game/Blueprints/Items/ItemTable_Global.ItemTable_Global",
                },
                "RowName": {
                    "type": {
                        "type": "NameProperty",
                    },
                    "value": name,
                },
            },
        },
        "ChangeableData_12_2B90E1F74F648135579D39A49F5A2313": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Game/Blueprints/Data/Abiotic_InventoryChangeableDataStruct",
                "name": "Abiotic_InventoryChangeableDataStruct",
                "guid": "d775c660-49d1-f198-30bd-428d3199792d",
            },
            "value": {
                "AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB": {
                    "type": {
                        "type": "StrProperty",
                    },
                    "value": asset_id.hex.upper(),
                },
                "CurrentItemDurability_4_24B4D0E64E496B43FB8D3CA2B9D161C8": {
                    "type": {
                        "type": "DoubleProperty",
                    },
                    "value": 1e8,
                },
                "MaxItemDurability_6_F5D5F0D64D4D6050CCCDE4869785012B": {
                    "type": {
                        "type": "DoubleProperty",
                    },
                    "value": 1e5,
                },
                "CurrentStack_9_D443B69044D640B0989FD8A629801A49": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": stack,
                },
                "CurrentAmmoInMagazine_12_D68C190F4B2FA78A4B1D57835B95C53D": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": ammo_size,
                },
                "LiquidLevel_46_D6414A6E49082BC020AADC89CC29E35A": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 0x7FFFFFFF if liquid else 0,
                },
                "CurrentLiquid_19_3E1652F448223AAE5F405FB510838109": {
                    "type": {
                        "type": "ByteProperty",
                        "blueprint": "/Game/Blueprints/Data/E_LiquidType",
                        "name": "E_LiquidType",
                    },
                    "value": f"NewEnumerator{liquid}",
                },
                "TextureVariantRow_28_1C7CF7A0441335E8AC4EA7B5CA91F636": {
                    "type": {"type": "StructProperty", "blueprint": "/Script/Engine", "name": "DataTableRowHandle"},
                    "value": {
                        "DataTable": {
                            "type": {
                                "type": "ObjectProperty",
                            },
                            "value": "",
                        },
                        "RowName": {
                            "type": {
                                "type": "NameProperty",
                            },
                            "value": "None",
                        },
                    },
                },
                "DynamicState_39_7597AC6549E292B931C61BB13C9E42EB": {
                    "type": {
                        "type": "BoolProperty",
                    },
                    "value": False,
                },
                "PlayerMadeString_42_CC0B72B24DBEAB2CC04454AAFFD4BBE9": {
                    "type": {
                        "type": "StrProperty",
                    },
                    "value": "",
                },
                "GameplayTags_45_1A018E824E25CC7BA608A6B2835209A1": {
                    "type": {
                        "type": "StructProperty",
                        "blueprint": "/Script/GameplayTags",
                        "name": "GameplayTagContainer",
                    },
                    "value": [],
                },
                "DynamicProperties_50_5C138DB145048726E8C0FEAC7C9600F7": {
                    "type": {
                        "type": "ArrayProperty",
                    },
                    "value": {
                        "type": {
                            "type": "StructProperty",
                            "blueprint": "/Script/AbioticFactor",
                            "name": "DynamicProperty",
                        },
                        "values": dynamic_attributes,
                    },
                },
            },
        },
    }


def create_object_inventory() -> dict[str, dict[str, Any]]:
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
            "value": 0,
        },
    }


def extract_item_asset_id(item: dict[str, dict[str, Any]]) -> UUID | None:
    data = item["ChangeableData_12_2B90E1F74F648135579D39A49F5A2313"]["value"]
    asset_id = data["AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB"]["value"]
    return None if asset_id == "-1" else UUID(asset_id)


def extract_object_asset_id(obj: dict[str, dict[str, Any]]) -> UUID | None:
    data = obj["ChangableData_37_6153F4A94F01A776C108038B7F38E256"]["value"]
    asset_id = data["AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB"]["value"]
    return None if asset_id == "-1" or asset_id.startswith("/Game/Maps") else UUID(asset_id)


def euler(w: float, x: float, y: float, z: float) -> tuple[float, float, float]:
    return (
        math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)),
        2 * math.atan2(math.sqrt(1 + 2 * (w * y - x * z)), math.sqrt(1 - 2 * (w * y - x * z))) - math.pi / 2,
        math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)),
    )


def quaternion(psi: float, theta: float, phi: float) -> tuple[float, float, float, float]:
    cos_psi = math.cos(psi / 2)
    sin_psi = math.sin(psi / 2)
    cos_theta = math.cos(theta / 2)
    sin_theta = math.sin(theta / 2)
    cos_phi = math.cos(phi / 2)
    sin_phi = math.sin(phi / 2)
    return (
        cos_phi * cos_theta * cos_psi + sin_phi * sin_theta * sin_psi,
        sin_phi * cos_theta * cos_psi - cos_phi * sin_theta * sin_psi,
        cos_phi * sin_theta * cos_psi + sin_phi * cos_theta * sin_psi,
        cos_phi * cos_theta * sin_psi - sin_phi * sin_theta * cos_psi,
    )
