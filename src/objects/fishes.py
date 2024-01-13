from pathlib import Path

from core import Direction
from objects.base import MovingObject


def reverse_skin(input_file: Path) -> str:
    """Reverses the direction where the fish is looking in the given skin."""

    text = input_file.read_text()
    for switch in ("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"), ("/", "\\"):
        fst, snd = switch
        text = text.replace(fst, "TEMP").replace(snd, fst).replace("TEMP", snd)

    lines = text.splitlines()
    lines = [line[::-1] for line in lines]
    return "\n".join(lines)


def parse_skin(name: str) -> list[list[str]]:
    """Parses a skin from the given path."""
    return [
        list(line) for line in open(SKINS_DIRECTORY / f"{name}.txt").read().split("\n")
    ]


SKINS_DIRECTORY = Path(__file__).parent / "fishes"
for file 


def new_fish(
    name: str, speed: int, anchor_coords: tuple[int, int], direction: Direction
) -> MovingObject:
    """Returns a new fish object with the given name and speed."""
    skin = FISHES[name][direction]
    return MovingObject(anchor_coords, skin, direction, speed=speed)
