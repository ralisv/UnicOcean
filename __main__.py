from time import sleep

from engine.ocean import Ocean
from engine.utils import clear_terminal
from objects.fishes import BlueFish


def main() -> None:
    clear_terminal()
    print("Hello, world!")
    ocean = Ocean(10)
    ocean.put_object(BlueFish((1, 0), speed=3))
    ocean.put_object(BlueFish((5, 5), speed=5))
    while True:
        sleep(0.5)
        clear_terminal()
        ocean.update()
        print(ocean)


if __name__ == "__main__":
    main()
