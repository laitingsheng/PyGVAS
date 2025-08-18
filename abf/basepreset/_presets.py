PICKUP_TARGETS = {
    "deployed_bobblehead_abe_c": "bobblehead_abe",
    "deployed_bobblehead_gkheavy_c": "bobblehead_jotun",
    "deployed_bobblehead_janet_c": "bobblehead_janet",
    "deployed_bobblehead_leyak_b_c": "bobblehead_leyak_b",
    "deployed_bobblehead_leyak_c": "bobblehead_leyak",
    "deployed_bobblehead_manse_c": "bobblehead_manse",
    "deployed_bobblehead_order_c": "bobblehead_order",
    "deployed_bobblehead_scientist_c": "bobblehead_sci",
    "deployed_bobblehead_secguard_c": "bobblehead_sec",
    "deployed_bobblehead_smith_c": "bobblehead_smith",
    "deployed_bobblehead_sniper_c": "bobblehead_sniper",
    "deployed_bobblehead_witch_c": "bobblehead_witch",
    "deployed_figurine_composer_c": "fig_comp",
    "deployed_figurine_darkwaterbeast_c": "fig_darkwaterbeast",
    "deployed_figurine_exor_armored_c": "fig_exor_armored",
    "deployed_figurine_exor_c": "fig_exor",
    "deployed_figurine_forklift_c": "fig_forklift",
    "deployed_figurine_gamesprite_c": "fig_lamogi",
    "deployed_figurine_mgt_larva_big_c": "fig_larvabig",
    "deployed_figurine_mgt_larva_big_orange_c": "fig_larvabigorange",
    "deployed_figurine_mgt_larva_c": "fig_larva",
    "deployed_figurine_mgt_larva_orange_c": "fig_larvaorange",
    "deployed_figurine_reaper_c": "fig_reaper",
    "deployed_figurine_security_bot_c": "fig_security_bot",
    "deployed_figurine_train_c": "fig_train",
    "deployed_painting_desk_c": "painting_desk",
    "deployed_painting_landscape_c": "painting_landscape",
    "deployed_painting_landscape_fancy_c": "painting_landscape_fancy",
    "deployed_painting_landscape_large_c": "painting_landscape_large",
    "deployed_painting_landscape_large_fancy_c": "painting_landscape_large_fancy",
    "deployed_painting_square_c": "painting_square",
    "deployed_painting_square_fancy_c": "painting_square_fancy",
    "deployed_painting_vertical_c": "painting_vertical",
    "deployed_painting_vertical_fancy_c": "painting_vertical_fancy",
    "deployed_rug_arcade_c": "rug_arcade",
    "deployed_rug_flathill_c": "rug_flathill",
    "deployed_rug_mat_c": "rug_mat_01",
    "deployed_rug_order_c": "rug_order",
    "deployed_rug_oval_c": "rug_oval_01",
    "deployed_rug_rectangular_c": "rug_rectangle_01",
    "deployed_rug_square_c": "rug_square_01",
    "deployed_rug_torii_c": "rug_torii",
    "deployed_torii_figurine_jizo_c": "fig_torii_jizo",
}

REPLACE_TARGETS = {
    "deployed_container_wastebucket_c",
    "deployed_craftedchargingstation_c",
    "deployed_furniture_cabinet_vintage_c",
    "deployed_furniture_craftedbed_c",
    "deployed_furniture_craftedbed_t2_c",
    "deployed_furniture_craftedbed_t3_c",
    "deployed_furniture_desk_executive_01_c",
    "deployed_furniture_desk_lab_01_c",
    "deployed_furniture_desk_lab_02_c",
    "deployed_furniture_desk_office_02_c",
    "deployed_liquidcontainer_barrel_c",
    "deployed_liquidcontainer_barrel_wood_c",
    "deployed_liquidcontainer_cauldron_tech_c",
    "deployed_watercooler_c",
    "deployed_waterfilter_c",
    "deployed_watertank_c",
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
    "deployed_storagecrate_makeshift_c",
    "deployed_storagecrate_makeshift_t2_c",
    "deployed_storagecrate_makeshift_t3_c",
    "deployed_storagecrate_makeshift_t4_c",
    "deployed_armor_stand_c",
    "deployed_armor_stand_woodf_c",
    "deployed_armor_stand_woodm_c",
    "deployed_crate_hgatekeeper_c",
    "deployed_crate_hmusicbox_c",
    "deployed_crate_hornate_c",
    "deployed_crate_hsecurity_c",
    "deployed_crate_hinquisitor_c",
    "gardenplot_large_c",
    "gardenplot_medium_c",
    "gardenplot_small_c",
    "gardenplot_smallround_c",
}

TARGET_IDENTIFIER = "Facility"

DEPLOY_BEDS = [
    (
        {
            "x": -17545.0,
            "y": 11110.0,
            "z": 1571.0,
        },
        "PZ0",
        {
            "y": 140.0,
        },
        {
            0: (0, 0, 0),
            1: (0, 1, 0),
        },
    ),
]

# 1 - water
# 2 - feces
# 3 - radioactive
# 4 - molten
# 6 - fuel, not sure where it is used, not available
# 7 - vomit, seems to be a liquid in the character itself only, not available
# 8 - electricity, not meant to be in a barrel
# 9 - blood, seems to be only presented in IS-0013, not available
# 11 - antejuice
# 13 - tainted water, too common in nearly everywhere
# 14 - soup, must be linked to a soup type
# 15 - laser, not meant to be in a barrel
# 16 - ink
DEPLOY_BARRELS = [
    (
        {
            "x": -15472.0,
            "y": 9989.0,
            "z": 1211.0,
        },
        "PZ180",
        {
            "x": -96.0,
            "y": 78.0,
        },
        [
            (11, (0, 0, 0), (1, 4, 1)),
            (16, (0, 4, 0), (1, 1, 1)),
            (1, (1, 0, 0), (1, 5, 1)),
        ],
    ),
    (
        {
            "x": -18690.0,
            "y": 10264.0,
            "z": 1016.0,
        },
        "PZ0",
        {
            "x": 96.0,
            "y": 78.0,
        },
        [
            (1, (0, 0, 0), (1, 4, 1)),
        ],
    ),
    (
        {
            "x": -18246.0,
            "y": 9988.0,
            "z": 1016.0,
        },
        "PZ90",
        {
            "x": -78.0,
        },
        [
            (2, (0, 0, 0), (1, 1, 1)),
            (3, (1, 0, 0), (1, 1, 1)),
            (4, (2, 0, 0), (1, 1, 1)),
            (1, (3, 0, 0), (2, 1, 1)),
        ],
    ),
    (
        {
            "x": -18246.0,
            "y": 10186.0,
            "z": 1016.0,
        },
        "PZ270",
        {
            "x": -78.0,
        },
        [
            (2, (0, 0, 0), (1, 1, 1)),
            (3, (1, 0, 0), (1, 1, 1)),
            (4, (2, 0, 0), (1, 1, 1)),
        ],
    ),
]

IGNORE_LABELS = {
    "Marker",
    "Placeholder",
}

DEPLOY_STORAGES = [
    (
        {
            "x": -16705.0,
            "y": 10324.0,
            "z": 991.0,
        },
        "PZ270",
        {
            "x": -100.0,
            "z": 79.0,
        },
        [
            ("", (0, 0, 0), (7, 1, 3)),
        ],
    ),
    (
        {
            "x": -17044.0,
            "y": 11079.0,
            "z": 1111.0,
        },
        "PZ270",
        {
            "x": 100.0,
            "z": 79.0,
        },
        [
            ("", (0, 0, 0), (7, 1, 5)),
        ],
    ),
    # (
    #     {
    #         "x": -16697.0,
    #         "y": 10762.0,
    #         "z": 991.0,
    #     },
    #     "PZ0",
    #     {
    #         "z": 79.0,
    #     },
    #     [
    #         ("", (0, 0, 0), (1, 1, 4)),
    #     ],
    # ),
    # (
    #     {
    #         "x": -16765.0,
    #         "y": 10762.0,
    #         "z": 991.0,
    #     },
    #     "PZ180",
    #     {
    #         "z": 79.0,
    #     },
    #     [
    #         ("", (0, 0, 0), (1, 1, 4)),
    #     ],
    # ),
    # (
    #     {
    #         "x": -16381.0,
    #         "y": 10444.0,
    #         "z": 1111.0,
    #     },
    #     "PZ180",
    #     {
    #         "y": 100.0,
    #         "z": 79.0,
    #     },
    #     [
    #         ("", (0, 0, 0), (1, 6, 5)),
    #     ],
    # ),
    # {
    #     "start": {
    #         "x": -16385.0,
    #         "y": 10776.0,
    #         "z": 1571.0,
    #     },
    #     "direction": "PZ180",
    #     "spacing": {
    #         "y": 100.0,
    #         "z": 79.0,
    #     },
    #     "labels": [
    #         ("", (0, 0, 0), (1, 4, 4)),
    #     ],
    # },
]

DEPLOY_FARMS = [
    (
        {
            "x": -16542.0,
            "y": 11547.0,
            "z": 1571,
        },
        "PZ270",
        {
            "x": -400.0,
        },
        {
            (0, 0, 0): [
                "Plant_Corn",
                "Plant_Egg",
                "Plant_Greyeb",
                "Plant_Potato",
            ] * 2,
            (1, 0, 0): [
                "Plant_Pumpkin",
                "Plant_Rice",
                "Plant_SpaceLettuce",
                "Plant_Super_Tomato",
            ] * 2,
            (2, 0, 0): [
                "Plant_Tomato",
                "Plant_Wheat",
                "Plant_GlowTulip",
                "Plant_Nyxshade",
            ] * 2,
            (3, 0, 0): [
                "Plant_RopePlant",
                "Plant_VinePlant",
            ] * 4,
        },
    ),
]

# DEPLOY_FREEZERS = [
#     (
#        {
#            "x": -16261.0,
#            "y": 10244.0,
#            "z": 1211.0,
#        },
#        "PZ0",
#        {
#            "z": 100.0,
#        },
#        [
#            ("", (0, 0, 0), (1, 1, 0)),
#        ],
#     ),
# ]
