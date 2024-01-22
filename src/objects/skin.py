from pathlib import Path

from core import Skin

MIRRORING_CHARACTERS = [
    ("(", ")"),
    ("[", "]"),
    ("{", "}"),
    ("<", ">"),
    ("/", "\\"),
]


def load_skin(path: Path, colors: dict[str, str]) -> tuple[Skin, Skin]:
    """Parses a skin from the given path, returns a tuple of left and right skins."""
    raw_skin = path.read_text()

    # Make sure all lines are the same length
    lines = [line.rstrip() for line in raw_skin.splitlines()]
    max_length = max(len(line) for line in lines)
    lines = [line.ljust(max_length) for line in lines]
    raw_skin = "\n".join(lines)

    return (
        dye_skin(parse_skin(raw_skin), colors),
        dye_skin(parse_skin(reverse_skin(raw_skin)), colors),
    )


def dye_skin(skin: Skin, colors: dict[str, str]) -> Skin:
    """Dyes the skin with the given colors."""
    for row, line in enumerate(skin):
        for col, char in enumerate(line):
            if char in colors:
                skin[row][col] = f"\033[38;2;{colors[char]}m{char}\033[0m"

    return skin


def reverse_skin(skin: str) -> str:
    """Reverses the direction where the fish is looking in the given skin."""

    for fst, snd in MIRRORING_CHARACTERS:
        skin = skin.replace(fst, "TEMP").replace(snd, fst).replace("TEMP", snd)

    lines = [line[::-1] for line in skin.splitlines()]
    return "\n".join(lines)


def parse_skin(raw_skin: str) -> Skin:
    """Parses the skin from the given string."""
    return [list(line) for line in raw_skin.splitlines()]