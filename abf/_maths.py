import math


DIRECTIONS: dict[str, dict[str, float]] = {
    "PZ0": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "w": 1.0,
    },
    "PZ90": {
        "x": 0.0,
        "y": 0.0,
        "z": math.sqrt(2) / 2,
        "w": math.sqrt(2) / 2,
    },
    "PZ180": {
        "x": 0.0,
        "y": 0.0,
        "z": 1.0,
        "w": 0.0,
    },
    "PZ270": {
        "x": 0.0,
        "y": 0.0,
        "z": -math.sqrt(2) / 2,
        "w": math.sqrt(2) / 2,
    },
}


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
