#!/usr/bin/env python3

import argparse
import signal
from time import sleep

from engine.ocean import Ocean
from engine.utils import clear_terminal
from load import load_mirror, load_objects

DEFAULT_FPS = 5


def sigint_handler(signum: int, frame: object) -> None:
    """Called when SIGINT is received"""
    clear_terminal()
    print("Hope you enjoyed the ocean")
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)


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

    # mirror must be loaded BEFORE objects
    load_mirror()
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
