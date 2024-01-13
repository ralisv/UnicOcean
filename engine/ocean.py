import random
import signal
from math import ceil

from core import Direction
from engine.utils import get_terminal_dimensions
from objects.base import MovingObject, OceanObject
from objects.fishes import FISHES, new_fish


class Ocean:
    DESPAWN_DISTANCE = 20
    """ Distance from the edge of the terminal at which objects are despawned """

    objects: list[OceanObject] = []
    rows: int
    cols: int

    def __init__(self, fishes: int) -> None:
        self.fishes = fishes
        self.cols, self.rows = get_terminal_dimensions()

        for _ in range(ceil((self.rows * self.cols) ** 0.25)):
            self.put_object(self.generate_new_fish())

        # Register a signal handler for SIGWINCH
        signal.signal(signal.SIGWINCH, self._on_dimensions_change)

    def _on_dimensions_change(self, signum: int, frame: object) -> None:
        """Called when the terminal dimensions change."""
        self.cols, self.rows = get_terminal_dimensions()

    def __str__(self) -> str:
        grid = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        for obj in sorted(self.objects, key=lambda key: key.depth):
            anchor_row, anchor_col = obj.anchor

            for row, l in enumerate(obj.skin):
                for col, char in enumerate(l):
                    new_row, new_col = anchor_row + row, anchor_col + col

                    if self.is_within_bounds((new_row, new_col)):
                        grid[anchor_row + row][anchor_col + col] = char

        return "\n".join("".join(row) for row in grid)

    def put_object(self, obj: OceanObject) -> None:
        """Puts an object on the grid."""
        self.objects.append(obj)

    def is_within_bounds(self, coords: tuple[int, int]) -> bool:
        """Returns whether the given anchor is within bounds."""
        row, col = coords
        return 0 <= row < self.rows and 0 <= col < self.cols

    def generate_new_fish(self) -> MovingObject:
        fish_name = random.choice(list(FISHES.keys()))
        speed = random.randint(1, MovingObject.MAX_SPEED)
        direction = random.choice([Direction.LEFT, Direction.RIGHT])

        if direction == Direction.LEFT:
            anchor = (random.randint(0, self.rows - 2), self.cols)
        else:
            anchor = (random.randint(0, self.rows - 2), -10)

        return new_fish(fish_name, speed, anchor, direction)

    def update(self) -> None:
        """Updates the state of the ocean."""
        for obj in self.objects:
            if isinstance(obj, MovingObject):
                obj.move()

        if len(self.objects) < (self.rows * self.cols) ** 0.5 and random.random() < 0.1:
            self.put_object(self.generate_new_fish())

        self.objects = [obj for obj in self.objects if not self.has_to_despawn(obj)]

    def has_to_despawn(self, obj: OceanObject) -> bool:
        """Returns whether the given object has an anchor out of bounds."""
        row, col = obj.anchor
        return (
            row < -self.DESPAWN_DISTANCE
            or row >= self.rows + self.DESPAWN_DISTANCE
            or col < -self.DESPAWN_DISTANCE
            or col >= self.cols + self.DESPAWN_DISTANCE
        )
