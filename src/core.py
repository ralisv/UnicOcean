from enum import Enum
from pathlib import Path

from pydantic import BaseModel

Skin = list[list[str]]

OBJECTS_DIRECTORY = Path(__file__).parent.parent / "assets" / "objects"


MIRRORING_CHARACTERS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
    "/": "\\",
}


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


class AnsiColorCode(BaseModel):
    """
    A class representing an ANSI color code
    """

    rgb_red: int
    rgb_green: int
    rgb_blue: int
    bg: bool = False

    def __str__(self) -> str:
        return f"\033[{48 if self.bg else 38};2;{self.rgb_red};{self.rgb_green};{self.rgb_blue}m"

    @property
    def background(self) -> "AnsiColorCode":
        return AnsiColorCode(
            rgb_red=self.rgb_red,
            rgb_green=self.rgb_green,
            rgb_blue=self.rgb_blue,
            bg=True,
        )

    def wrap(self, string: str) -> str:
        return f"{self}{string}\033[0m"


def parse_colors(colors: dict[str, str]) -> dict[str, AnsiColorCode]:
    """
    Parses the colors from the given dictionary
    """
    color_mapping: dict[str, AnsiColorCode] = {}
    for chars, color in colors.items():
        r, g, b = color.split(";")
        color_code = AnsiColorCode(rgb_red=int(r), rgb_green=int(g), rgb_blue=int(b))
        for char in chars:
            color_mapping[char] = color_code

    return color_mapping
