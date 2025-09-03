import itertools
import os
import re
import sys
from pathlib import Path

from .._saves import ABFPlayerSave, ABFWorldSave
from ._door import unlock_door
from ._player import improve_player
from ._world import (
    deploy_beds,
    deploy_farms,
    deploy_hazard_storages,
    deploy_item_stands,
    deploy_liquid_containers,
    deploy_storages,
    preprocess_objects,
    process_sockets,
    prune_connections,
    write_attributes,
)


entry, profile, name = sys.argv
save_folder = Path(os.environ["LOCALAPPDATA"]) / "AbioticFactor/Saved/SaveGames" / profile / "Worlds" / name
player_save_folder = save_folder / "PlayerData"

output_folder = Path("output") / profile / name
output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)
player_output_folder = output_folder / "PlayerData"
player_output_folder.mkdir(mode=0o755, parents=True, exist_ok=True)

save_regex = re.compile(r"Player_([A-Za-z0-9]+)\.sav")
players: list[str] = []
for index, save_file in enumerate(player_save_folder.glob("Player_*.sav")):
    matches = save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid player save file name {save_file.name}")

    save = ABFPlayerSave.from_binary_file(save_file)
    identifier = save.body["SaveIdentifier"]["value"]
    if identifier != matches[1]:
        raise ValueError(f"Player save file {save_file.name} identifier mismatched")

    improve_player(index, save.body["CharacterSaveData"]["value"])
    save.to_binary_file(player_output_folder / save_file.name)

    players.append(identifier)

save_regex = re.compile(r"WorldSave_(\w+)\.sav")
saves: dict[str, ABFWorldSave] = {}
updated_saves: dict[str, None] = {}
for save_file in save_folder.glob("WorldSave_*.sav"):
    matches = save_regex.match(save_file.name)
    if matches is None:
        raise ValueError(f"Invalid save file name {save_file.name}")

    save = ABFWorldSave.from_binary_file(save_file)
    identifier = save.body["SaveIdentifier"]["value"]
    if identifier != matches[1]:
        raise ValueError(f"World save file {save_file.name} identifier mismatched")
    saves[identifier] = save

    if unlock_door(save.body):
        updated_saves[identifier] = None

    if preprocess_objects(
        identifier,
        save.body,
        {
            "deployed_armor_stand_c",
            "deployed_armor_stand_woodf_c",
            "deployed_armor_stand_woodm_c",
            "deployed_bobblehead_abe_c",
            "deployed_bobblehead_gkheavy_c",
            "deployed_bobblehead_janet_c",
            "deployed_bobblehead_leyak_b_c",
            "deployed_bobblehead_leyak_c",
            "deployed_bobblehead_manse_c",
            "deployed_bobblehead_order_c",
            "deployed_bobblehead_scientist_c",
            "deployed_bobblehead_secguard_c",
            "deployed_bobblehead_smith_c",
            "deployed_bobblehead_sniper_c",
            "deployed_bobblehead_witch_c",
            "deployed_container_armorylocker_c",
            "deployed_container_chest_vintage_c",
            "deployed_container_filingcabinet_small_c",
            "deployed_container_filingcabinet_medium_c",
            "deployed_container_filingcabinet_large_c",
            "deployed_container_filingcabinet_huge_c",
            "deployed_container_magazine_stand_c",
            "deployed_container_medkit_c",
            "deployed_container_parktrashbin_c",
            "deployed_container_toolbox_c",
            "deployed_container_toolbox_plant_c",
            "deployed_container_trashcan_c",
            "deployed_container_trashcan_small_c",
            "deployed_container_wastebucket_c",
            "deployed_craftedchargingstation_c",
            "deployed_crate_hgatekeeper_c",
            "deployed_crate_hmusicbox_c",
            "deployed_crate_hornate_c",
            "deployed_crate_hsecurity_c",
            "deployed_crate_hinquisitor_c",
            "deployed_figurine_composer_c",
            "deployed_figurine_darkwaterbeast_c",
            "deployed_figurine_exor_armored_c",
            "deployed_figurine_exor_c",
            "deployed_figurine_forklift_c",
            "deployed_figurine_gamesprite_c",
            "deployed_figurine_mgt_larva_big_c",
            "deployed_figurine_mgt_larva_big_orange_c",
            "deployed_figurine_mgt_larva_c",
            "deployed_figurine_mgt_larva_orange_c",
            "deployed_figurine_reaper_c",
            "deployed_figurine_security_bot_c",
            "deployed_figurine_train_c",
            "deployed_figurine_watercooler_c",
            "deployed_furniture_craftedbed_c",
            "deployed_furniture_craftedbed_t2_c",
            "deployed_furniture_craftedbed_t3_c",
            "deployed_hazardcrate_c",
            "deployed_is0012_c",
            "deployed_itemstand_parentbp_c",
            "deployed_liquidcontainer_barrel_c",
            "deployed_liquidcontainer_barrel_wood_c",
            "deployed_liquidcontainer_cauldron_tech_c",
            "deployed_painting_desk_c",
            "deployed_poster_c",
            "deployed_ramp_large_c",
            "deployed_ramp_small_c",
            "deployed_rug_arcade_c",
            "deployed_rug_flathill_c",
            "deployed_rug_mat_c",
            "deployed_rug_order_c",
            "deployed_rug_oval_c",
            "deployed_rug_rectangular_c",
            "deployed_rug_square_c",
            "deployed_rug_torii_c",
            "deployed_storagecrate_makeshift_c",
            "deployed_storagecrate_makeshift_t2_c",
            "deployed_storagecrate_makeshift_t3_c",
            "deployed_storagecrate_makeshift_t4_c",
            "deployed_torii_figurine_jizo_c",
            "deployed_wallclock_c",
            "deployed_watercooler_c",
            "deployed_waterfilter_c",
            "deployed_watertank_c",
            "gardenplot_large_c",
            "gardenplot_medium_c",
            "gardenplot_small_c",
            "gardenplot_smallround_c",
        },
    ):
        updated_saves[identifier] = None

for identifier, save in saves.items():
    if process_sockets(identifier, save.body):
        updated_saves[identifier] = None

identifier = "Facility"
deploy_beds(
    identifier,
    13,
    players,
    (
        (
            (-17545.0, 11110.0, 1571.0),
            (0.0, 140.0),
            "PZ0",
            {
                0: (0, 0),
                1: (0, 1),
            },
        ),
    ),
)
deploy_farms(
    identifier,
    13,
    (
        (
            (-16528.0, 11539.0, 1571.0),
            (-330.0, 0.0),
            "PZ270",
            {
                (0, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_Corn",
                                "Plant_Egg",
                                "Plant_Greyeb",
                                "Plant_Potato",
                            ),
                            2,
                        ),
                    ),
                ),
                (1, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_Pumpkin",
                                "Plant_Rice",
                                "Plant_SpaceLettuce",
                                "Plant_Super_Tomato",
                            ),
                            2,
                        ),
                    ),
                ),
                (2, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_Tomato",
                                "Plant_Wheat",
                                "Plant_GlowTulip",
                                "Plant_Nyxshade",
                            ),
                            2,
                        ),
                    ),
                ),
                (3, 0): tuple(
                    itertools.chain.from_iterable(
                        itertools.repeat(
                            (
                                "Plant_RopePlant",
                                "Plant_VinePlant",
                            ),
                            4,
                        ),
                    ),
                ),
            },
        ),
    ),
)
deploy_liquid_containers(
    identifier,
    13,
    (
        (
            (-18003.0, 9786.0, 991.0),
            (96.0, -78.0),
            "PZ0",
            (2, 6),
            tuple(
                itertools.chain(
                    itertools.repeat(11, 5),
                    itertools.repeat(16, 1),
                    itertools.repeat(1, 6),
                ),
            ),
        ),
        (
            (-18690.0, 10264.0, 1016.0),
            (0.0, 78.0),
            "PZ0",
            (1, 4),
            tuple(itertools.repeat(1, 4)),
        ),
        (
            (-18246.0, 9988.0, 1016.0),
            (-78.0, 0.0),
            "PZ90",
            (5, 1),
            tuple(itertools.chain(range(2, 5), itertools.repeat(1, 2))),
        ),
        (
            (-18246.0, 10186.0, 1016.0),
            (-78.0, 0.0),
            "PZ270",
            (3, 1),
            tuple(range(2, 5)),
        ),
    ),
)
texture_variants_datatable = "/Game/Blueprints/DataTables/Customization/DT_TextureVariants.DT_TextureVariants"
deploy_storages(
    identifier,
    13,
    (
        (
            (-16705.0, 10324.0, 991.0),
            (-100.0, 0.0, 79.0),
            "PZ270",
            (4, 1, 3),
            (),
        ),
        (
            (-16698.0, 10762.0, 991.0),
            (0.0, 0.0, 79.0),
            "PZ0",
            (1, 1, 5),
            (
                (
                    "Pickup",
                    tuple(
                        {
                            "name": name,
                            "stack": 100,
                        }
                        for name in (
                            "anvil",
                            "batterycharger",
                            "briefcase",
                            "cable_fibre",
                            "cafeteriatray",
                            "cementbag",
                            "core_fragment",
                            "crackedlight",
                            "deployable_gaseousnest",
                            "emptymug",
                            "fishbones",
                            "geigercounter",
                            "glowshard",
                            "glowstick",
                            "gravitycube",
                            "grease",
                            "headlamp_nvg_t2_broken",
                            "keyboard",
                            "reapersigil",
                            "shieldgen_broken",
                            "silverchain",
                            "windchime_exor",
                        )
                    ),
                ),
                (
                    "Material",
                    tuple(
                        {
                            "name": name,
                            "stack": 8000,
                        }
                        for name in (
                            "cpu",
                            "cpu_gold",
                            "cpu_purple",
                            "cpu_red",
                            "growth",
                            "hose",
                            "magalloy",
                            "motor",
                            "neutrinomapper",
                            "petn",
                            "scrap_arcane",
                            "scrap_bio",
                            "scrap_cloth",
                            "scrap_composer",
                            "scrap_glass",
                            "scrap_gunk",
                            "scrap_kevlar",
                            "scrap_leather",
                            "scrap_metal",
                            "scrap_military",
                            "scrap_order",
                            "scrap_paper",
                            "scrap_plastic",
                            "scrap_silver",
                            "scrap_tech",
                            "stapler",
                            "steelcable",
                        )
                    ),
                ),
                (
                    "Material",
                    tuple(
                        {
                            "name": name,
                            "stack": 8000,
                        }
                        for name in (
                            "blood_plutonic",
                            "book",
                            "capacitor",
                            "carapace",
                            "carapace_plutonic",
                            "casefan",
                            "censer",
                            "coal",
                            "chains",
                            "coil",
                            "coil_v2",
                            "enethiol",
                            "essence_reaper",
                            "fishglue",
                            "gel",
                            "gem",
                            "gigaglue",
                            "hexwood",
                            "ichor",
                            "lens",
                            "liquidcrystal",
                            "magazines",
                            "mage_eye",
                            "organ_partial",
                            "rebar",
                            "receptor",
                            "refinedcarbon",
                            "solder",
                            "woodplank",
                        )
                    ),
                ),
                (
                    "Material",
                    tuple(
                        {
                            "name": name,
                            "stack": 8000,
                        }
                        for name in (
                            "acid",
                            "aircanister",
                            "cog",
                            "detcord",
                            "digital_ore",
                            "diode",
                            "eel_fat",
                            "oil",
                            "oil_black",
                            "oil_fish",
                            "oil_robot",
                            "parchment",
                            "pens",
                            "phone",
                            "pipe_hydro",
                            "pipe_metal",
                            "powderedcrystal",
                            "powersupply",
                            "pressuregauge",
                            "rotary_pump",
                            "rubberbands",
                            "sensor",
                            "transcendium",
                            "transformer_bushing",
                            "transformer_round",
                            "yetifur",
                        )
                    ),
                ),
                (
                    "Compound",
                    tuple(
                        {
                            "name": name,
                            "stack": 1000,
                        }
                        for name in (
                            "aircompressor",
                            "bleach",
                            "brick_cpu",
                            "brick_memory",
                            "brick_power",
                            "burner",
                            "carbonplating",
                            "circuitboard",
                            "controller",
                            "digital_gold",
                            "ducttape",
                            "grimoire",
                            "hose_reinforced",
                            "infrared_emitter",
                            "lcd_screen",
                            "lodestone",
                            "motionmod",
                            "organ",
                            "projectionmatrix",
                            "quantumglass",
                            "screws",
                            "storagechip",
                            "woodplank_reinforced",
                        )
                    ),
                ),
            ),
        ),
        (
            (-16764.0, 10762.0, 991.0),
            (0.0, 0.0, 79.0),
            "PZ180",
            (1, 1, 5),
            (
                (
                    "Container",
                    tuple(
                        {
                            "name": name,
                            "stack": 10,
                        }
                        for name in (
                            "bucket_metal",
                            "canteen",
                            "cauldron",
                            "chest_vintage",
                            "crate_hgatekeeper",
                            "crate_hinquisitor",
                            "crate_hmusicbox",
                            "crate_hornate",
                            "crate_hsecurity",
                            "deployable_armorylocker",
                            "deployable_barrel",
                            "deployable_filingcabinet_huge",
                            "deployable_filingcabinet_large",
                            "deployable_filingcabinet_medium",
                            "deployable_filingcabinet_small",
                            "deployable_fridge",
                            "deployable_magazine_stand",
                            "freezer",
                            "fridge_hazard",
                            "leyak_containment",
                            "storage_hazardcrate",
                            "storagecrate_makeshift",
                            "storagecrate_makeshift_t2",
                            "storagecrate_makeshift_t3",
                            "storagecrate_t4",
                            "storagecrate_void",
                            "warmingdrawer",
                        )
                    ),
                ),
                (
                    "Armour",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": f"armor_{part}_{name}",
                                    "stack": 10,
                                }
                                for part in ("chest", "arms", "legs")
                                for name in (
                                    "breacher",
                                    "captain",
                                    "groupe",
                                    "grunt",
                                    "medic",
                                    "sniper",
                                )
                            ),
                            (
                                {
                                    "name": f"armor_{part}_{name}",
                                    "stack": 10,
                                }
                                for part in ("helmet", "chest", "arms", "legs")
                                for name in (
                                    "exor",
                                    "hex",
                                    "interf",
                                    "mage",
                                    "reactor",
                                    "security",
                                )
                            ),
                        ),
                    ),
                ),
                (
                    "Armour",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": f"armor_{part}_{name}_u{level}",
                                    "stack": 10,
                                }
                                for part in ("helmet", "chest", "arms", "legs")
                                for name, level in (
                                    ("composer", 2),
                                    ("crystal", 1),
                                    ("forge", 2),
                                    ("labs", 2),
                                    ("makeshift", 3),
                                    ("tech", 1),
                                )
                            ),
                            (
                                {
                                    "name": f"armor_{part}_{name}",
                                    "stack": 10,
                                }
                                for part, name in (
                                    ("hat", "floppy"),
                                    ("chest", "puffycoat"),
                                    ("arms", "snowgloves"),
                                    ("legs", "snowpants"),
                                )
                            ),
                            (
                                {
                                    "name": f"armor_{part}_{name}",
                                    "stack": 10,
                                }
                                for part, name in (
                                    ("hat", "baseball"),
                                    ("hat", "beanie"),
                                    ("hat", "commander"),
                                    ("hat", "cowboy"),
                                    ("hat", "golfcap"),
                                    ("helmet", "beret"),
                                    ("helmet", "breacher"),
                                    ("helmet", "cqc"),
                                    ("helmet", "gkheavy"),
                                    ("helmet", "medmask"),
                                    ("helmet", "military"),
                                    ("helmet", "mountaineer"),
                                    ("helmet", "rook"),
                                    ("helmet", "santahat"),
                                )
                            ),
                        ),
                    ),
                ),
            ),
        ),
        (
            (-17044.0, 11079.0, 1111.0),
            (100.0, 0.0, 79.0),
            "PZ270",
            (7, 1, 5),
            (
                (
                    "Statue",
                    tuple(
                        {
                            "name": name,
                            "stack": 10,
                        }
                        for name in (
                            "bell",
                            "bobblehead_abe",
                            "bobblehead_janet",
                            "bobblehead_jotun",
                            "bobblehead_leyak",
                            "bobblehead_leyak_b",
                            "bobblehead_manse",
                            "bobblehead_order",
                            "bobblehead_sci",
                            "bobblehead_sec",
                            "bobblehead_smith",
                            "bobblehead_sniper",
                            "bobblehead_witch",
                            "fig_comp",
                            "fig_darkwaterbeast",
                            "fig_exor",
                            "fig_exor_armored",
                            "fig_forklift",
                            "fig_lamogi",
                            "fig_larva",
                            "fig_larvabig",
                            "fig_larvabigorange",
                            "fig_larvaorange",
                            "fig_reaper",
                            "fig_security_bot",
                            "fig_torii_jizo",
                            "fig_train",
                            "figurine_watercooler",
                            "rug_arcade",
                            "rug_flathill",
                            "rug_mat_01",
                            "rug_order",
                            "rug_oval_01",
                            "rug_rectangle_01",
                            "rug_square_01",
                            "rug_torii",
                        )
                    ),
                ),
                (
                    "Tool",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": name,
                                    "stack": 100,
                                }
                                for name in (
                                    "bait_antefish",
                                    "bait_crab_gem",
                                    "bait_dw",
                                    "bait_eel",
                                    "bait_ice",
                                    "bait_is98",
                                    "bait_moonfish",
                                    "bait_portal",
                                    "bait_radfish",
                                    "bait_silk",
                                    "bait_umbra",
                                    "lantern_torii",
                                    "lodestone_fragment",
                                    "sconce",
                                    "tinygears",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 100,
                                    "liquid": liquid,
                                }
                                for name, liquid in (
                                    ("battery_quantum", 8),
                                    ("flashlight_basic", 8),
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 10,
                                }
                                for name in (
                                    "book_journal",
                                    "cookbook",
                                    "salem_book_01",
                                    "salem_book_02",
                                    "salem_book_03",
                                    "salem_book_04",
                                    "salem_book_05",
                                    "sg_book_01",
                                    "sg_book_02",
                                    "sg_book_03",
                                    "sydyk_book_01",
                                    "sydyk_book_02",
                                    "sydyk_book_03",
                                )
                            ),
                        ),
                    ),
                ),
                (
                    "Tool",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": name,
                                    "stack": 1000,
                                }
                                for name in (
                                    "bandage",
                                    "bandage_t2",
                                    "gastromeds",
                                    "iodinetablets",
                                    "splint",
                                    "syringe",
                                    "syringe_acid",
                                    "thermite_molotov",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 10,
                                }
                                for name in (
                                    "alienthermite",
                                    "composer_tablet",
                                    "cookingpot",
                                    "fireextinguisher",
                                    "fishingrod_insulated",
                                    "fryingpan",
                                    "hammer",
                                    "headlamp_goggles_swim",
                                    "neutrino_emitter",
                                    "pocketwatch",
                                    "screwdriver",
                                    "soupbowl",
                                    "tramkey",
                                    "wall_clock",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 1,
                                }
                                for name in (
                                    "paint_black",
                                    "paint_blue",
                                    "paint_brown",
                                    "paint_cyan",
                                    "paint_glitch",
                                    "paint_green",
                                    "paint_lime",
                                    "paint_orange",
                                    "paint_pink",
                                    "paint_purple",
                                    "paint_red",
                                    "paint_white",
                                    "paint_yellow",
                                )
                            ),
                        ),
                    ),
                ),
                (
                    "Farming",
                    tuple(
                        {
                            "name": name,
                            "stack": 100,
                        }
                        for name in (
                            "plant_dead",
                            "plantfood_t1",
                            "plantfood_t2",
                            "plantfood_t3",
                            "seed_antelight",
                            "seed_antelight_blue",
                            "seed_antelight_grn",
                            "seed_antelight_orange",
                            "seed_antelight_pink",
                            "seed_antelight_red",
                            "seed_antelight_rgb",
                            "seed_antelight_space",
                            "seed_corn",
                            "seed_eggplant",
                            "seed_glowtulip",
                            "seed_greyeb",
                            "seed_lettuce",
                            "seed_nyxshade",
                            "seed_pumpkin",
                            "seed_rice",
                            "seed_ropeplant",
                            "seed_supertomato",
                            "seed_tomato",
                            "seed_vine",
                            "seed_wheat",
                            "soilbag",
                        )
                    ),
                ),
                (
                    "Decoration",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": name,
                                    "stack": 100,
                                }
                                for name in (
                                    "christmaslights_01",
                                    "holly_01",
                                    "royal_coin",
                                    "royal_crown",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 10,
                                }
                                for name in (
                                    "banner_gatekeeper",
                                    "banner_order",
                                    "deployable_antelight",
                                    "deployable_antelight_blue",
                                    "deployable_antelight_grn",
                                    "deployable_antelight_orange",
                                    "deployable_antelight_pink",
                                    "deployable_antelight_red",
                                    "deployable_antelight_rgb",
                                    "deployable_antelight_space",
                                    "deployable_pottedplant_01",
                                    "deployable_pottedplant_02",
                                    "deployable_pottedplant_03",
                                    "deployable_pottedplant_04",
                                    "deployable_pottedplant_06",
                                    "tapestry_order",
                                    "xmastree",
                                )
                            ),
                        ),
                    ),
                ),
                (
                    "Biological",
                    tuple(
                        {
                            "name": name,
                            "stack": 100,
                        }
                        for name in (
                            "feces",
                            "feces_donotspawn",
                            "feces_skink",
                            "gib_chieftain_skull",
                            "gib_exor_skull",
                            "gib_exor_skull_volatile",
                            "gib_gkheavy_skull",
                            "gib_human_arm_mil",
                            "gib_human_skull",
                            "gib_mage_skull",
                            "gib_skull_behemoth",
                            "gib_sniper_skull",
                            "gib_symph_skull",
                            "gib_tarasque_skull",
                            "gib_witch_skull",
                            "gib_yeti_skull",
                            "goo_exor",
                            "pet_skink",
                        )
                    ),
                ),
                (
                    "Gear",
                    tuple(
                        {
                            "name": name,
                            "stack": 10,
                        }
                        for name in (
                            "suit_beekeeper",
                            "suit_fire",
                            "suit_hazmat",
                            "suit_highinquisitor",
                            "suit_mgt_larva",
                            "suit_powerc",
                            "suit_ratsuit",
                            "suit_rebreather",
                            "suit_sappersuit",
                            "trinket_biofusion",
                            "trinket_carbuncle",
                            "trinket_censer",
                            "trinket_core",
                            "trinket_cornhuskdoll",
                            "trinket_foglantern",
                            "trinket_friendfinder",
                            "trinket_geigercounter",
                            "trinket_gravitycube",
                            "trinket_kylie",
                            "trinket_kylie_shieldgenerator",
                            "trinket_light_orange",
                            "trinket_light_purple",
                            "trinket_light_red",
                            "trinket_light_white",
                            "trinket_light_yellow",
                            "trinket_neutrinolantern",
                            "trinket_nightpass",
                            "trinket_ogredoll",
                            "trinket_order",
                            "trinket_petrock",
                            "trinket_shieldgenerator",
                            "trinket_shieldgenerator_u1",
                            "trinket_spuddy",
                        )
                    ),
                ),
                (
                    "Gear",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": name,
                                    "stack": 100,
                                }
                                for name in (
                                    "clothrope",
                                    "key_gatekeeper",
                                    "key_inq",
                                    "key_ornate",
                                    "key_porcelain",
                                    "key_security",
                                    "gatekey",
                                    "gunrepairkit_t1",
                                    "gunrepairkit_t2",
                                    "hotwirekit_securitycart",
                                    "hotwirekit_suv",
                                    "jumppad",
                                    "plantrope",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 10,
                                }
                                for name in (
                                    "backpack_chieftain",
                                    "backpack_heavy",
                                    "backpack_medium",
                                    "backpack_security",
                                    "backpack_small",
                                    "backpack_snow",
                                    "backpack_radio",
                                    "backpack_rat",
                                )
                            ),
                        ),
                    ),
                ),
                (
                    "Firearm",
                    tuple(
                        itertools.chain(
                            (
                                {
                                    "name": name,
                                    "stack": 2000,
                                }
                                for name in (
                                    "ammo_12g",
                                    "ammo_308",
                                    "ammo_556",
                                    "ammo_9mm",
                                    "ammo_magnum",
                                    "ammo_rocket",
                                    "ammo_rocket_cluster",
                                    "ammo_rocket_penetrator",
                                    "blackholegrenade",
                                    "frag",
                                    "keresphere",
                                    "net",
                                    "nullgrenade",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 20,
                                }
                                for name in (
                                    "biocannon",
                                    "heavy_laser",
                                    "magnum_military",
                                    "net_launcher",
                                    "pistol_gk",
                                    "pistol_security",
                                    "rifle_assault",
                                    "rifle_groupe",
                                    "rifle_sniper",
                                    "rocketlauncher",
                                    "shotgun_doublebarrel",
                                    "shotgun_military",
                                    "smg_military",
                                )
                            ),
                            (
                                {
                                    "name": name,
                                    "stack": 20,
                                    "liquid": liquid,
                                }
                                for name, liquid in (
                                    ("flamethrower", 15),
                                    ("megalight_t2", 8),
                                    ("offhand_mageglove", 15),
                                    ("vacuum_u2", 8),
                                )
                            ),
                        ),
                    ),
                ),
                (
                    "Weapon",
                    tuple(
                        {
                            "name": name,
                            "stack": 20,
                        }
                        for name in (
                            "baton",
                            "canesword",
                            "crowbar",
                            "kiteshield",
                            "knife",
                            "knife_groupe",
                            "knife_ornate",
                            "knife_ornate_dual",
                            "knife_super",
                            "oar",
                            "offhand_ornate_knife",
                            "pickaxe",
                            "pipewrench",
                            "pitchfork",
                            "ratscanner",
                            "riotshield",
                            "sledgehammer",
                            "sword",
                            "umbrella",
                            "weapon_deskleg",
                            "woodaxe",
                        )
                    ),
                ),
                (
                    "Food",
                    tuple(
                        {
                            "name": name,
                            "stack": 400,
                        }
                        for name in (
                            "alienwheat",
                            "aloe",
                            "food_candy",
                            "food_candycane",
                            "food_cannedpeas",
                            "food_cookie",
                            "food_donut",
                            "food_mre",
                            "food_nachos",
                            "food_sugar",
                            "gloweye",
                            "glowtulip",
                            "honey",
                            "icecream_melted",
                            "salt",
                            "saltrock",
                            "slushie",
                            "soda_a",
                            "soda_b",
                            "soda_c",
                            "soda_d",
                            "soda_e",
                            "soda_energy",
                            "sugarcrystal",
                            "wax",
                        )
                    ),
                ),
            ),
        ),
    ),
)
deploy_hazard_storages(
    identifier,
    13,
    (
        (
            (-16731.0, 10762.0, 1386.0),
            (0.0, 0.0, 0.0),
            "PZ270",
            (1, 1, 1),
            (
                tuple(
                    itertools.chain(
                        (
                            {
                                "name": name,
                                "stack": 8000,
                            }
                            for name in (
                                "essence_frozen",
                                "essence_leyak",
                                "powercell",
                            )
                        ),
                        (
                            {
                                "name": name,
                                "stack": 1000,
                            }
                            for name in (
                                "238",
                                "thermocell",
                            )
                        ),
                        (
                            {
                                "name": name,
                                "stack": 400,
                            }
                            for name in (
                                "soda_anom",
                                "soda_bad",
                            )
                        ),
                        (
                            {
                                "name": name,
                                "stack": 10,
                            }
                            for name in (
                                "gib_peccary_skull",
                                "gib_peccary_skull_red",
                                "gib_pecmushroom_skull",
                                "gib_sow_skull",
                                "trinket_light_green",
                            )
                        ),
                    ),
                ),
            ),
        ),
    ),
)
deploy_item_stands(
    identifier,
    13,
    (
        (
            (-15449.0, 9964.0, 1211.0),
            (-42.0, 42.0),
            "PZ180",
            (4, 20),
            tuple(
                itertools.chain(
                    (
                        {
                            "name": f"armor_{part}_{name}",
                            "stack": 10,
                        }
                        for part, name in (
                            ("hat", "bonnet"),
                            ("hat", "buckethat"),
                            ("hat", "securitycap"),
                            ("helmet", "gasmask"),
                            ("helmet", "hydrohat"),
                            ("helmet", "karate"),
                        )
                    ),
                    (
                        {
                            "name": name,
                            "stack": 10,
                            "variant": (
                                texture_variants_datatable,
                                variant,
                            ),
                        }
                        for name, variant in (
                            ("armor_hat_bonnet", "bonnet_black"),
                            ("armor_hat_floppy", "hat_floppy_orange"),
                            ("armor_hat_securitycap", "securitycap_blue"),
                        )
                    ),
                    (
                        {
                            "name": name,
                            "stack": 10,
                            "variant": (
                                texture_variants_datatable,
                                f"{prefix}_{variant}",
                            ),
                        }
                        for name, prefix, variants in (
                            (
                                "armor_hat_buckethat",
                                "buckethat",
                                (
                                    "green",
                                    "navy",
                                    "red",
                                ),
                            ),
                            (
                                "armor_helmet_gasmask",
                                "labmask_shiny",
                                (
                                    "blue",
                                    "dark",
                                    "gold",
                                    "green",
                                    "orange",
                                    "pink",
                                    "purple",
                                    "red",
                                ),
                            ),
                            (
                                "armor_helmet_hardhat",
                                "gear_hardhat",
                                (
                                    "blue",
                                    "brown",
                                    "gray",
                                    "green",
                                    "red",
                                    "white",
                                    "yellow",
                                ),
                            ),
                            (
                                "armor_helmet_hydrohat",
                                "hydrohat",
                                (
                                    "green",
                                    "orange",
                                    "red",
                                    "yellow",
                                ),
                            ),
                            (
                                "armor_helmet_karate",
                                "gear_armor_karatehelmet",
                                (
                                    "black",
                                    "red",
                                    "white",
                                ),
                            ),
                            (
                                "deployable_fridge",
                                "fridge_office",
                                (
                                    "blue",
                                    "gray",
                                    "red",
                                ),
                            ),
                            (
                                "painting_desk",
                                "photoframe",
                                (
                                    "acahn",
                                    "alexander",
                                    "clock",
                                    "cozycat",
                                    "digby",
                                    "ela",
                                    "hopia",
                                    "jacat",
                                    "jim",
                                    "jimmy",
                                    "jordog",
                                    "kingsley",
                                    "km",
                                    "rowan",
                                    "zig",
                                    "zig2",
                                    "zig3",
                                ),
                            ),
                        )
                        for variant in variants
                    ),
                    (
                        {
                            "name": name,
                            "stack": 10,
                            "variant": (
                                texture_variants_datatable,
                                f"{name}_{variant}",
                            ),
                        }
                        for name, variants in (
                            (
                                "arcademachine",
                                (
                                    "detour",
                                    "tdl",
                                    "usm",
                                ),
                            ),
                            (
                                "backpack_small",
                                (
                                    "gray",
                                    "green",
                                    "purple",
                                    "red",
                                    "white",
                                    "yellow",
                                ),
                            ),
                            (
                                "poster",
                                (
                                    "0091",
                                    "detour",
                                    "tdl",
                                    "usm",
                                ),
                            ),
                            (
                                "tv",
                                (
                                    "channel5",
                                    "standby",
                                    "tips_cafeteria",
                                    "tips_designations",
                                    "tips_exploration",
                                    "tips_gk",
                                    "tips_resting",
                                    "tips_static",
                                    "tips_trams",
                                    "tips_vehicles",
                                    "tips_wayseeker",
                                ),
                            ),
                        )
                        for variant in variants
                    ),
                ),
            ),
        ),
    ),
)
updated_saves[identifier] = None
updated_saves["MetaData"] = None

updated_saves.update(prune_connections())

for identifier in updated_saves:
    save = saves[identifier]
    write_attributes(identifier, save.body)
    save.to_binary_file(output_folder / f"WorldSave_{identifier}.sav")
