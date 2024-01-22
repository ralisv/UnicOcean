from pydantic import BaseModel, validator

from core import OBJECTS_DIRECTORY, CollisionEffect, Direction, Skin
from objects.base import MovingObject, OceanObject

FISHES_DIRECTORY = OBJECTS_DIRECTORY / "fish"
"""The directory where all the fishes are stored"""

FISHES: dict[str, "FishInfo"] = {}
"""A dictionary of all the registered fishes"""


class FishConfiguration(BaseModel):
    min_speed: float = 0.05
    max_speed: float = 1.0
    carnivorous: bool = False
    rarity: int = 1
    colors: dict[str, str] = {}

    @validator("min_speed")
    @classmethod
    def min_speed_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("min_speed must be positive")
        return value


class FishInfo(FishConfiguration):
    name: str
    skin_left: Skin
    skin_right: Skin


class Fish(MovingObject):
    carnivorous: bool
    skin_left: Skin
    skin_right: Skin

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin_left: Skin,
        skin_right: Skin,
        initial_direction: Direction,
        speed: float,
        carnivorous: bool,
        rarity: int,
    ):
        skin = skin_left if initial_direction == Direction.LEFT else skin_right
        super().__init__(anchor_coordinates, skin, initial_direction, speed)
        self.skin_left = skin_left
        self.skin_right = skin_right
        self.carnivorous = carnivorous
        self.rarity = rarity

    def change_direction(self) -> None:
        """Changes the direction of the fish."""
        went_left = self.direction == Direction.LEFT
        self.direction = Direction.RIGHT if went_left else Direction.LEFT
        self.skin = self.skin_right if went_left else self.skin_left

    def _on_collision(self, bumped: OceanObject) -> CollisionEffect:
        if isinstance(bumped, Fish) and self.carnivorous:
            return CollisionEffect.EAT

        return CollisionEffect.NOTHING
