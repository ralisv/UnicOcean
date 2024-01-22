"""The module which contains the base classes for all the objects in the ocean."""

from math import floor

from core import Direction, Skin


class OceanObject:
    anchor: tuple[int, int]
    """ Coordinates of the top left corner of the object """

    skin: Skin
    """ Skin of the object """

    height: int
    """ Height of the object """
    length: int
    """ Length of the object """

    def __init__(self, anchor_coordinates: tuple[int, int], skin: Skin):
        self.anchor = anchor_coordinates
        self.skin = skin
        self.height = len(skin)
        self.length = len(skin[0])

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.skin)


class MovingObject(OceanObject):
    direction: Direction
    speed: float
    move_index = 0

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin: Skin,
        direction: Direction,
        speed: float,
    ):
        super().__init__(anchor_coordinates, skin)
        self.direction = direction
        self.speed = speed

    def move(self) -> None:
        """Moves the object in the given direction."""
        row_delta, col_delta = self.direction.value
        row, col = self.anchor
        self.move_index += 1 * self.speed

        self.anchor = (
            row + row_delta * floor(self.move_index),
            col + col_delta * floor(self.move_index),
        )

        self.move_index -= floor(self.move_index)


class StaticObject(OceanObject):
    def __init__(self, anchor_coordinates: tuple[int, int], skin: Skin):
        super().__init__(anchor_coordinates, skin)
        self.skin = skin
