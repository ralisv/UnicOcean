#!/usr/bin/env python3

import argparse
import signal
from time import sleep

from engine.ocean import Ocean
from engine.utils import clear_terminal

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

    clear_terminal()
    ocean = Ocean(10)
    ocean_string = str(ocean)

    while True:
        print(ocean_string)
        ocean.update()
        ocean_string = str(ocean)
        sleep(1 / fps)
        clear_terminal()


if __name__ == "__main__":
    main()
