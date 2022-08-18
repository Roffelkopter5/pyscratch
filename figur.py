from pyscratch.sprite import Sprite
from pyscratch.images import BackgroundColor

class Figur(Sprite):
    def on_key_down_w(self):
        self.rotate_to(0)
        while self.is_pressed("w"):
            self.move(2)
    
    def on_mouse_down_right(self):
        self.go_to_random()