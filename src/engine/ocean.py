import random
import signal
from math import ceil

from core import Direction
from engine.utils import get_terminal_dimensions
from objects.base import MovingObject, OceanObject
from objects.fish import FISHES, Fish


class Ocean:
    SPAWN_RATE = 0.005
    """ Chance of a new fish spawning per frame per row """

    DESPAWN_DISTANCE = 50
    """ Distance from the edge of the terminal at which objects are despawned """

    @property
    def spawn_chance(self) -> float:
        return self.SPAWN_RATE * (self.rows / self.fishes**0.7)

    objects: list[OceanObject] = []
    rows: int
    cols: int

    def __init__(self, fishes: int) -> None:
        self.fishes = fishes
        self.cols, self.rows = get_terminal_dimensions()

        # Generate some fishes
        for _ in range(ceil((self.rows * self.cols) ** 0.25)):
            self.put_object(self.generate_new_fish())

        # Register a signal handler for SIGWINCH
        signal.signal(signal.SIGWINCH, self._on_dimensions_change)

    def _on_dimensions_change(self, signum: int, frame: object) -> None:
        """Called when the terminal dimensions change."""
        self.cols, self.rows = get_terminal_dimensions()

    def __str__(self) -> str:
        grid = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        for obj in self.objects:
            anchor_row, anchor_col = obj.anchor

            for row, l in enumerate(obj.skin):
                for col, char in enumerate(l):
                    new_row, new_col = anchor_row + row, anchor_col + col
                    try:  # Due to signal handling, the terminal dimensions may change asynchronously
                        if self.is_within_bounds((new_row, new_col)) and char != " ":
                            grid[anchor_row + row][anchor_col + col] = char
                    except IndexError:
                        pass

        return "\n".join("".join(row) for row in grid)

    def put_object(self, obj: OceanObject) -> None:
        """Puts an object on the grid."""
        self.objects.append(obj)

    def is_within_bounds(self, coords: tuple[int, int]) -> bool:
        """Returns whether the given anchor is within bounds."""
        row, col = coords
        return 0 <= row < self.rows and 0 <= col < self.cols

    def generate_new_fish(self) -> MovingObject:
        """Generates a new fish object."""
        fish_name = random.choice(list(FISHES.keys()))
        fish_info = FISHES[fish_name]
        speed = random.uniform(fish_info.min_speed, fish_info.max_speed)
        direction = random.choice([Direction.LEFT, Direction.RIGHT])

        fish_length = len(fish_info.skin_left[0])
        fish_height = len(fish_info.skin_left)

        if direction == Direction.LEFT:
            anchor = (random.randint(1, self.rows - fish_height), self.cols)
        else:
            anchor = (random.randint(1, self.rows - fish_height), -fish_length)

        fish = Fish(
            anchor,
            FISHES[fish_name].skin_left,
            FISHES[fish_name].skin_right,
            direction,
            speed,
            FISHES[fish_name].carnivorous,
            FISHES[fish_name].rarity,
        )

        return fish

    def update(self) -> None:
        """Updates the ocean."""
        for obj in self.objects:
            if isinstance(obj, MovingObject):
                obj.move()

        if random.random() < self.spawn_chance:
            self.put_object(self.generate_new_fish())

        self.objects = [obj for obj in self.objects if not self.has_to_despawn(obj)]

    def has_to_despawn(self, obj: OceanObject) -> bool:
        """Returns whether the given object has to be despawned."""
        row, col = obj.anchor
        return (
            row < -self.DESPAWN_DISTANCE
            or row >= self.rows + self.DESPAWN_DISTANCE
            or col < -self.DESPAWN_DISTANCE
            or col >= self.cols + self.DESPAWN_DISTANCE
        )
