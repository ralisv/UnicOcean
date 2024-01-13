from core import Direction


class OceanObject:
    skin: list[list[str]]
    anchor: tuple[int, int]
    depth: int
    """ Z-index of the object, the higher the less overshadowed """

    def __init__(self, anchor_coordinates: tuple[int, int], depth: int = 0):
        self.anchor = anchor_coordinates
        self.depth = depth


class MovingObject(OceanObject):
    DEFAULT_MOVE_INDEX = 10
    MAX_SPEED = 10
    direction: Direction
    speed: int
    move_index = DEFAULT_MOVE_INDEX

    def __init__(
        self,
        anchor_coordinates: tuple[int, int],
        skin: list[list[str]],
        direction: Direction = Direction.RIGHT,
        speed: int = 1,
    ):
        super().__init__(anchor_coordinates)
        self.skin = skin
        self.direction = direction
        self.speed = min(self.MAX_SPEED, speed)

    def move(self) -> None:
        """Moves the object in the given direction."""
        self.move_index -= self.speed
        if self.move_index > 0:
            return

        else:
            self.move_index += self.DEFAULT_MOVE_INDEX

        row, col = self.direction.value
        self.anchor = (self.anchor[0] + row, self.anchor[1] + col)


class StaticObject(OceanObject):
    def __init__(self, anchor_coordinates: tuple[int, int], skin: list[list[str]]):
        super().__init__(anchor_coordinates)
        self.skin = skin
