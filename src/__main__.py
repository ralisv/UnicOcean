#!/usr/bin/env python3

import argparse
import signal
from time import sleep

from engine.ocean import Ocean
from engine.utils import clear_terminal
from objects.fish import FISHES, FISHES_DIRECTORY, FishConfiguration, FishInfo
from objects.skin import load_skin

DEFAULT_FPS = 5


def sigint_handler(signum: int, frame: object) -> None:
    """Called when SIGINT is received"""
    clear_terminal()
    print("Hope you enjoyed the ocean")
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def load_objects() -> None:
    """Loads all objects from the objects directory, should be called before Ocean is instantiated"""

    # Load fishes
    for fish_dir in FISHES_DIRECTORY.iterdir():
        if not fish_dir.is_dir():
            continue

        config_file = fish_dir / "config.json"
        if not config_file.exists():
            continue

        config = FishConfiguration.parse_file(config_file)
        left, right = load_skin(fish_dir / "skin.txt", config.colors)

        FISHES[fish_dir.name] = FishInfo(
            name=fish_dir.name,
            skin_left=left,
            skin_right=right,
            min_speed=config.min_speed,
            max_speed=config.max_speed,
            carnivorous=config.carnivorous,
            rarity=config.rarity,
            colors=config.colors,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument(
        "-f",
        "--fps",
        dest="fps",
        type=int,
        metavar="FPS",
        help="How many frames per second to render",
    )
    args = parser.parse_args()

    fps = args.fps or DEFAULT_FPS

    load_objects()

    ocean = Ocean(10)

    clear_terminal()
    print(ocean)

    while True:
        ocean.update()
        ocean_string = str(ocean)
        sleep(1 / fps)
        clear_terminal()
        print(ocean_string)


if __name__ == "__main__":
    main()
