from pathlib import Path

from core import Direction
from objects.base import MovingObject


def parse_skin(name: str) -> list[list[str]]:
    """Parses a skin from the given path."""
    return [
        list(line) for line in open(SKINS_DIRECTORY / f"{name}.txt").read().split("\n")
    ]


SKINS_DIRECTORY = Path(__file__).parent / "fish-skins"
FISHES: dict[str, dict[Direction, list[list[str]]]] = {
    "blue": {
        Direction.LEFT: parse_skin("blue-left"),
        Direction.RIGHT: parse_skin("blue-right"),
    },
    "tuna": {
        Direction.RIGHT: parse_skin("tuna-right"),
        Direction.LEFT: parse_skin("tuna-left"),
    },
}


def new_fish(
    name: str, speed: int, anchor_coords: tuple[int, int], direction: Direction
) -> MovingObject:
    """Returns a new fish object with the given name and speed."""
    skin = FISHES[name][direction]
    return MovingObject(anchor_coords, skin, direction, speed=speed)
