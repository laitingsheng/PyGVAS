import secrets
from typing import Any, Iterable
from uuid import UUID


def create_datatable_row_handle(datatable: str, rowname: str) -> dict[str, Any]:
    return {
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
                "value": datatable,
            },
            "RowName": {
                "type": {
                    "type": "NameProperty",
                },
                "value": rowname,
            },
        },
    }


def create_asset_id() -> UUID:
    candidate = bytearray(secrets.token_bytes(16))
    candidate[4] &= 0x4F
    candidate[4] |= 0x40
    return UUID(bytes=bytes(candidate))


def create_changeable_data(
    asset_id: UUID | None = None,
    stack: int = 1,
    ammo: int | None = None,
    liquid: int = 0,
    variant: tuple[str, str] = ("", "None"),
    tags: Iterable[str] = (),
    portions: int = 1,
    paint: int | None = None,
    plant_proxy: bool = False,
) -> dict[str, Any]:
    if portions < 1:
        portions = 1

    dynamic_attributes: list[dict[str, Any]] = [
        {
            "Key": {
                "type": {
                    "type": "EnumProperty",
                    "blueprint": "/Script/AbioticFactor",
                    "name": "EDynamicProperty",
                },
                "value": "Portions",
            },
            "Value": {
                "type": {
                    "type": "IntProperty",
                },
                "value": portions,
            },
        },
    ]

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

    if liquid < 0:
        liquid = 0

    if paint is not None and paint >= 0:
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

    if plant_proxy:
        dynamic_attributes.append(
            {
                "Key": {
                    "type": {
                        "type": "EnumProperty",
                        "blueprint": "/Script/AbioticFactor",
                        "name": "EDynamicProperty",
                    },
                    "value": "GrowthStage",
                },
                "Value": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 4,
                },
            },
        )
        dynamic_attributes.append(
            {
                "Key": {
                    "type": {
                        "type": "EnumProperty",
                        "blueprint": "/Script/AbioticFactor",
                        "name": "EDynamicProperty",
                    },
                    "value": "GrowthProgress",
                },
                "Value": {
                    "type": {
                        "type": "IntProperty",
                    },
                    "value": 0,
                },
            },
        )

    variant_datatable, variant_rowname = variant

    return {
        "AssetID_25_06DB7A12469849D19D5FC3BA6BEDEEAB": {
            "type": {
                "type": "StrProperty",
            },
            "value": "-1" if asset_id is None else asset_id.hex.upper(),
        },
        "CurrentItemDurability_4_24B4D0E64E496B43FB8D3CA2B9D161C8": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0 if asset_id is None else 2e8,
        },
        "MaxItemDurability_6_F5D5F0D64D4D6050CCCDE4869785012B": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0 if asset_id is None else 2e5,
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
            "value": -1 if asset_id is None else (0x7FFFFFFF if liquid else 0),
        },
        "CurrentLiquid_19_3E1652F448223AAE5F405FB510838109": {
            "type": {
                "type": "ByteProperty",
                "blueprint": "/Game/Blueprints/Data/E_LiquidType",
                "name": "E_LiquidType",
            },
            "value": f"NewEnumerator{liquid}",
        },
        "TextureVariantRow_28_1C7CF7A0441335E8AC4EA7B5CA91F636": create_datatable_row_handle(
            datatable=variant_datatable,
            rowname=variant_rowname,
        ),
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
            "value": list(tags),
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
    }


def create_cooking_data() -> dict[str, Any]:
    return {
        "ActorPath_49_9FEEAC6446E69602638F6FB6A601D5B3": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/CoreUObject",
                "name": "SoftObjectPath",
            },
            "value": {
                "blueprint": "None",
                "name": "None",
                "value": "",
            },
        },
        "OriginalItem_5_9765522C42FCC99E6F5D04BB2E72F5E0": create_datatable_row_handle(
            datatable="",
            rowname="None",
        ),
        "CookwareItem_7_0CEA84364B6EFA85C1894C8973D19CEC": create_datatable_row_handle(
            datatable="",
            rowname="None",
        ),
        "TimetoCook_13_957973F1415B52E0EAF193BFCFEF1ED0": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0,
        },
        "TimetoBurn_19_56E61B3D4CD7E80A3468F7B36710A67B": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0,
        },
        "TimetoIgnite_21_E1D2B6EA42120839F22F679D838B0EDC": {
            "type": {
                "type": "DoubleProperty",
            },
            "value": 0.0,
        },
        "ShowPanMesh_24_555B9EA344D3843851B621999A8B46A3": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "ChefID_30_B6FE3723499B8BD398B599803507C8EB": {
            "type": {
                "type": "StrProperty",
            },
            "value": "0",
        },
        "Cookware_33_F0F914814DCB16F2C065D59972EC2242": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "CookingDelayGUID_36_032270FC4B3BB25FF024D2A7EE2A29CD": {
            "type": {
                "type": "StructProperty",
                "blueprint": "/Script/CoreUObject",
                "name": "Guid",
            },
            "value": "00000000-0000-0000-0000-000000000000",
        },
        "CanCookSoup_39_063D45094EF66504F3CE228577A66547": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "StartCookingSoup_41_86C766F8442EE0F41118538989D1C2AF": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "NewIngredientAdded_43_B99A589D4E919808FCA92EB366AD138F": {
            "type": {
                "type": "BoolProperty",
            },
            "value": False,
        },
        "CookState_58_44043C7B47846DF5ADBDF48402C0D6A1": {
            "type": {
                "type": "EnumProperty",
                "blueprint": "/Script/AbioticFactor",
                "name": "ECookingState",
            },
            "value": "Raw",
        },
        "ChefState_59_E6B3445E44EE0E93B0F62AB2A503509F": {
            "type": {
                "type": "EnumProperty",
                "blueprint": "/Script/AbioticFactor",
                "name": "ECookingState",
            },
            "value": "Raw",
        },
    }
