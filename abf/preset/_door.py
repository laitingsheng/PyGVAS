from typing import Any


def unlock_door(world: dict[str, dict[str, Any]]) -> bool:
    updated = False

    doormap = world.get("SimpleDoorMap")
    if doormap is not None:
        for _, door in doormap["value"]["values"]:
            for key, value in (
                ("DoorState_16_FC20B6E3483FF18E4FBDF19E39E880E9", "NewEnumerator0"),
                ("DoorRotationRootYaw_17_FEB24A4F4081A0EFDC1475AB811846D1", 0.0),
                ("OneWayDoor_HasBeenUnlocked_9_128506D0489955F65729EEA611C542AC", True),
            ):
                if door[key]["value"] != value:
                    door[key]["value"] = value
                    updated = True

    doormap = world.get("SecurityDoorMap")
    if doormap is not None:
        for _, door in doormap["value"]["values"]:
            for key, value in (
                ("IsDoorOpen_27_128506D0489955F65729EEA611C542AC", True),
            ):
                if door[key]["value"] != value:
                    door[key]["value"] = value
                    updated = True

    return updated
