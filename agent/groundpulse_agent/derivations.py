from __future__ import annotations


def orbital_period_minutes(mean_motion: float) -> float:
    """Calculate approximate orbital period from mean motion.

    CelesTrak expresses mean motion as revolutions per day.
    """
    if mean_motion <= 0:
        raise ValueError("MEAN_MOTION must be greater than zero")

    return round(1440.0 / mean_motion, 3)
