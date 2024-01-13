import signal

from engine.utils import get_terminal_dimensions
from objects.base import MovingObject, OceanObject


class Ocean:
    objects: list[OceanObject] = []
    rows: int
    cols: int

    def __init__(self, fishes: int) -> None:
        self.fishes = fishes
        self.cols, self.rows = get_terminal_dimensions()

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
                    grid[anchor_row + row][anchor_col + col] = char
        return "\n".join("".join(row) for row in grid)

    def put_object(self, obj: OceanObject) -> None:
        """Puts an object on the grid."""
        if not self.is_within_bounds(obj.anchor):
            raise ValueError("Anchor is out of bounds")

        self.objects.append(obj)

    def is_within_bounds(self, coords: tuple[int, int]) -> bool:
        """Returns whether the given anchor is within bounds."""
        row, col = coords
        return 0 <= row < self.rows and 0 <= col < self.cols

    def update(self) -> None:
        """Updates the state of the ocean."""
        for obj in self.objects:
            if isinstance(obj, MovingObject):
                obj.move()

        self.objects = [
            obj for obj in self.objects if self.is_within_bounds(obj.anchor)
        ]
