from pyscratch.app import App
from pyscratch.scene import Scene
from pyscratch.images import BackgroundColor

app = App("Test")
scene = Scene("Scene", bg=BackgroundColor((640, 480), (255, 255, 255)))
scene.load_sprites("figur.py", 20)
app.set_scene(scene)
app.run()