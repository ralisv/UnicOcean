#!/usr/bin/env python3

import argparse
import signal
from time import sleep

from engine.ocean import Ocean
from engine.utils import clear_terminal

DEFAULT_FPS = 2


def sigint_handler(signum: int, frame: object) -> None:
    """Called when SIGINT is received."""
    clear_terminal()
    print("Hope you enjoyed the ocean")
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main() -> int:
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some files.")

    # Add the optional argument for the output file with metavar
    parser.add_argument(
        "-f",
        "--fps",
        dest="fps",
        type=int,
        metavar="OUTPUT_FILE",
        help="output file where the result will be saved",
    )

    # Parse the arguments
    args = parser.parse_args()
    fps = args.fps or DEFAULT_FPS

    clear_terminal()
    ocean = Ocean(10)

    while True:
        sleep(1 / fps)
        clear_terminal()
        ocean.update()
        print(ocean)


if __name__ == "__main__":
    main()
