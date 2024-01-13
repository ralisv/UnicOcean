from math import floor

from core import Direction, Skin


class OceanObject:
    skin: Skin
    """ Skin of the object """

    anchor: tuple[int, int]
    """ Coordinates of the top left corner of the object """

    depth: int
    """ Z-index of the object, the higher the less overshadowed """

    height: int
    """ Height of the object """
    length: int
    """ Length of the object """

    def __init__(self, anchor_coordinates: tuple[int, int], depth: int, skin: Skin):
        self.anchor = anchor_coordinates
        self.depth = depth
        self.skin = skin
        self.height = len(skin)
        self.length = len(skin[0])


class MovingObject(OceanObject):
    MAX_SPEED = 1.0
    MIN_SPEED = 0.1
    direction: Direction
    speed: float
    move_index = 0

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin: Skin,
        direction: Direction,
        speed: float,
        depth: int = 0,
    ):
        super().__init__(anchor_coordinates, depth, skin)
        self.direction = direction
        self.speed = min(self.MAX_SPEED, speed)
        self.speed = max(self.MIN_SPEED, speed)

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


class Fish(MovingObject):
    skin_left: Skin
    """ Skin for the fish swimming in the left direction """
    skin_right: Skin
    """ Skin for the fish swimming in the right direction """
    carnivorous: bool

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin: Skin,
        direction: Direction,
        speed: int,
        skin_left: Skin,
        skin_right: Skin,
        carnivorous: bool,
    ):
        super().__init__(anchor_coordinates, skin, direction, speed)
        self.skin_left = skin_left
        self.skin_right = skin_right
        self.skin = skin_left if direction == Direction.LEFT else skin_right
        self.carnivorous = carnivorous

    def change_direction(self) -> None:
        """Changes the direction of the fish."""
        went_left = self.direction == Direction.LEFT
        self.direction = Direction.RIGHT if went_left else Direction.LEFT
        self.skin = self.skin_right if went_left else self.skin_left


class StaticObject(OceanObject):
    def __init__(self, anchor_coordinates: tuple[int, int], skin: Skin):
        super().__init__(anchor_coordinates, 0, skin)
        self.skin = skin
