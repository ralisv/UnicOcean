from time import sleep

from engine.interface import Ocean
from engine.utils import clear_terminal


def main() -> None:
    clear_terminal()
    print("Hello, world!")
    ocean = Ocean(10)
    while True:
        sleep(1)


if __name__ == "__main__":
    main()
