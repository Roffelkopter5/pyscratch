from pyscratch.sprite import Sprite
from pyscratch.images import BackgroundColor, Triangle

class Figur(Sprite):
    def __init__(self):
        super().__init__("ball.png")
    
    def on_key_up_w(self):
        print("Scaling")
        self.scale(2)