from pygame import Vector2, Surface
import pygame.key
import pygame.image
import pygame.mouse
from pyscratch.config import Config
import os
from .locals import Coord, Image

def load_image(name: Image) -> Surface:
    if isinstance(name, Surface):
        return name
    if os.path.isfile(name):
        return pygame.image.load(name).convert_alpha()
    elif file := Config.IMAGES.get(name, False):
        return load_image(file)
    else:
        raise FileNotFoundError(f"Image: {name} not found!")

def _vec2_lerp(v1: Coord, v2: Coord, h: float):
    return (v2 - v1) * h + v1

def _convert_to_pg(v: Vector2) -> Vector2:
    return Vector2(v.x + 320, -1 * v.y + 240)

def _convert_to_ps(v: Vector2) -> Vector2:
    return Vector2(v.x - 320, -1 * v.y + 240)

def _to_vec2(v: Coord) -> Vector2:
    if isinstance(v, Vector2):
        return v
    else:
        return Vector2(v)

def _key_name(key: int) -> str:
    return pygame.key.name(key)

def _button_name(button: int) -> str:
    return ["left", "middle", "right"][button-1]