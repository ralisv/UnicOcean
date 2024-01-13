import json
from pathlib import Path
from typing import Any

from core import Direction
from objects.base import MovingObject

Skin = list[list[str]]


FISHES_DIRECTORY = Path(__file__).parent.parent.parent / "assets" / "fishes"
FISH_TYPES: dict[str, dict[str, Any]] = {}


def reverse_skin(skin: str) -> str:
    """Reverses the direction where the fish is looking in the given skin."""

    for switch in ("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"), ("/", "\\"):
        fst, snd = switch
        skin = skin.replace(fst, "TEMP").replace(snd, fst).replace("TEMP", snd)

    lines = skin.splitlines()
    lines = [line[::-1] for line in lines]
    return "\n".join(lines)


def parse_skin(raw_skin: str) -> Skin:
    """Parses the skin from the given string."""
    return [list(line) for line in raw_skin.splitlines()]


def get_skin(name: str) -> tuple[Skin, Skin]:
    """Parses a skin from the given path, returns a tuple of left and right skins."""
    raw_skin = (FISHES_DIRECTORY / name / "skin.txt").read_text()
    return parse_skin(raw_skin), parse_skin(reverse_skin(raw_skin))


def parse_colors(name: str) -> dict[str, str]:
    """Parses the colors from the given path."""
    return json.loads((FISHES_DIRECTORY / name / "colors.json").read_text())


def dye_skin(skin: Skin, colors: dict[str, str]) -> Skin:
    """Dyes the skin with the given colors."""
    for row, line in enumerate(skin):
        for col, char in enumerate(line):
            if char in colors:
                skin[row][col] = f"\033[38;2;{colors[char]}m{char}\033[0m"
    return skin


# Parse all fishes
for fish_dir in FISHES_DIRECTORY.iterdir():
    # TODO if not dir log error (invalid structure)
    if fish_dir.is_dir():
        fish_name = fish_dir.name
        fish_colors: dict[str, str] = {}
        fish_skin_left: Skin = []
        fish_skin_right: Skin = []

        # Parse the skin
        try:
            fish_skin_left, fish_skin_right = get_skin(fish_name)
        except FileNotFoundError:
            # TODO log error
            continue

        except PermissionError:
            # TODO log error
            pass

        # Parse the colors
        try:
            fish_colors = parse_colors(fish_name)
        except FileNotFoundError:
            pass
        except PermissionError:
            # TODO log error
            pass

        # Dye the skin
        fish_skin_right = dye_skin(fish_skin_right, fish_colors)
        fish_skin_left = dye_skin(fish_skin_left, fish_colors)

        # Add the fish to the list
        FISH_TYPES[fish_name] = {
            "name": fish_name,
            "skin_left": fish_skin_left,
            "skin_right": fish_skin_right,
        }


def new_fish(
    name: str, speed: float, anchor_coords: tuple[int, int], direction: Direction
) -> MovingObject:
    """Returns a new fish object with the given name and speed."""
    if name not in FISH_TYPES:
        raise ValueError(f"Unknown fish type: {name}")

    skin = FISH_TYPES[name][f"skin_{direction.name.lower()}"]

    return MovingObject(anchor_coords, skin, direction, speed=speed)
