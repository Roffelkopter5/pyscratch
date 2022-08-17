from pygame import image, Vector2, Surface
from pyscratch.config import Config
import os
from locals import Coord, Image

def load_image(name: Image) -> Surface:
    if isinstance(name, Surface):
        return name
    if os.path.isfile(name):
        return image.load(name).convert_alpha()
    elif file := Config.IMAGES.get(name, False):
        return load_image(file)
    else:
        raise FileNotFoundError(f"Image: {name} not found!")


def vec2_lerp(v1: Coord, v2: Coord, h: float):
    return (v2 - v1) * h + v1


def convert_to_pg(v: Vector2) -> Vector2:
    return Vector2(v.x + 320, -1 * v.y + 240)

def convert_to_ps(v: Vector2) -> Vector2:
    return Vector2(v.x - 320, -1 * v.y + 240)

def to_vec2(v: Coord) -> Vector2:
    if isinstance(v, Vector2):
        return v
    else:
        return Vector2(v)

class BackgroundColor(Surface):
    def __init__(self, size: Coord, color):
        super().__init__(size)
        self.fill(color)

class Triangle(Surface):
    def __init__(self, size: Coord, color):
        super().__init__(size, pygame.SRCALPHA)
        pygame.draw.polygon(self, color, ((0, 0), (size[0], size[1]//2), (0, size[1])))