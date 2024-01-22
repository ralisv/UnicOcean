"""Module containing the configuration classes for all objects

To ensure valid data, the configuration classes are subclasses of :class:`pydantic.BaseModel`.
"""
from pydantic import BaseModel, PositiveFloat, root_validator


class OceanObjectConfig(BaseModel):
    colors: dict[str, str] = {}


class MovingObjectConfig(OceanObjectConfig):
    min_speed: PositiveFloat = 0.05
    max_speed: PositiveFloat = 1.0

    @root_validator
    def validate_speeds(cls, values: dict[str, float]) -> dict[str, float]:
        if values["min_speed"] > values["max_speed"]:
            raise ValueError("min_speed cannot be greater than max_speed")

        return values


class FishConfig(MovingObjectConfig):
    carnivorous: bool = False
    rarity: int = 1
    colors: dict[str, str] = {}
