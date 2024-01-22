from enum import Enum
from pathlib import Path

Skin = list[list[str]]

OBJECTS_DIRECTORY = Path(__file__).parent.parent / "assets" / "objects"


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class CollisionEffect(Enum):
    NOTHING = 0
    EAT = 1
    EXPLODE = 2


class NoFishSkinException(Exception):
    pass
