import signal
from time import sleep

from engine.ocean import Ocean
from engine.utils import clear_terminal


def sigint_handler(signum: int, frame: object) -> None:
    """Called when SIGINT is received."""
    clear_terminal()
    print("Hope you enjoyed the ocean")
    exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def main() -> None:
    clear_terminal()
    ocean = Ocean(10)

    while True:
        sleep(0.1)
        clear_terminal()
        ocean.update()
        print(ocean)


if __name__ == "__main__":
    main()
