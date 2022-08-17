from pyscratch.app import App
from pyscratch.scene import Scene
from pyscratch.sprite import Sprite
from pyscratch.utils import BackgroundColor

class Figur(Sprite):
    def on_key_down_w(self):
        self.rotate_to(0)
        self.move(2)

app = App("Test")
scene = Scene("Scene", bg=BackgroundColor((640, 480), (255, 255, 255)))
figur = Figur(BackgroundColor((30, 30), (255, 0, 0)))
scene.add_figur(figur)
app.set_scene(scene)
app.run()