import shutil


def clear_terminal() -> None:
    """Clears the terminal."""
    print("\033c", end="")


def get_terminal_dimensions() -> tuple[int, int]:
    """Returns the dimensions of the terminal."""
    return shutil.get_terminal_size()
