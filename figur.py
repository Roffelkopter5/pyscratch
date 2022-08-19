from pyscratch.sprite import Sprite
from pyscratch.images import BackgroundColor, Triangle

class Figur(Sprite):
    def __init__(self):
        super().__init__(Triangle((20, 20), (255, 0, 0)))

    def on_mouse_down_right(self):
        self.go_to_random()
        self.point_to(self._scene.random_pos())
        while self.endless():
            self.move(2)
            self.bounce_on_edge()