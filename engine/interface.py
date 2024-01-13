import signal

from engine.utils import get_terminal_dimensions


class Ocean:
    fishes: int
    rows: int
    cols: int
    grid: list[list[str]]

    def __init__(self, fishes: int) -> None:
        self.fishes = fishes
        self.cols, self.rows = get_terminal_dimensions()
        self.grid = [["a" for _ in range(self.cols)] for _ in range(self.rows)]

        # Register a signal handler for SIGWINCH
        signal.signal(signal.SIGWINCH, self._on_dimensions_change)

    def _on_dimensions_change(self, signum: int, frame: object) -> None:
        """Called when the terminal dimensions change."""
        self.cols, self.rows = get_terminal_dimensions()
        self.grid = [["a" for _ in range(self.cols)] for _ in range(self.rows)]

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid)
