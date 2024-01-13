from objects.base import MovingObject


class BlueFish(MovingObject):
    def __init__(self, anchor_coordinates: tuple[int, int], speed: int = 1):
        skin = [["d", "d", "o"], ["d", "d", "d"]]
        super().__init__(anchor_coordinates, skin, speed=speed)
