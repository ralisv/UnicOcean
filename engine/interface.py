import signal


class Ocean:
    fishes: int

    def __init__(self, fishes: int) -> None:
        self.fishes = fishes

        # Register a signal handler for SIGWINCH
        signal.signal(signal.SIGWINCH, self._on_dimensions_change)

    def _on_dimensions_change(self, signum: int, frame: object) -> None:
        """Called when the terminal dimensions change."""
        print("The terminal dimensions changed!")
