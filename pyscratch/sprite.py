from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App
    from .scene import Scene
    from .events import PyScratchEvent

from .utils import _to_vec2, load_image, _vec2_lerp, _convert_to_pg, _key_name, _button_name
from .locals import Image, Coord
from . import _get_logger

import pygame
from pygame import transform
from pygame.math import Vector2
from pygame.sprite import DirtySprite
from pygame.surface import Surface
from pygame.rect import Rect

from math import sin, cos, radians, acos, degrees
import time

_log = _get_logger(__name__)

class Sprite(DirtySprite):
    def __init__(self, image: Image = None):
        super().__init__()

        self._pos = Vector2()
        self._dim = Vector2()
        self._rot = 0.0
        self._alive = True
        self._app: App = None
        self._scene: Scene = None
        self._name = self.__class__.__name__

        if image:
            self.set_image(image)
        else:
            self.set_image(Surface((20, 20)))
        self._dirty = 1
        self._visible = True
        self._layer = 0

    # region MOTION
    # TODO: bounce on edge

    def change_pos(
        self,
        *,
        x: float = None,
        y: float = None,
        dx: float = 0,
        dy: float = 0,
    ):
        if x:
            self._pos.x = x + dx
        else:
            self._pos.x += dx
        
        if y:
            self._pos.y = y + dy
        else:
            self._pos.y += dy
        
        self._dirty = 1
        
    def move(self, steplength: float):
        direction = Vector2(cos(radians(self._rot)), sin(radians(self._rot)))
        self._pos += direction * steplength
        self._dirty = 1

    def go_to(self, target: Coord | Sprite):
        if isinstance(target, self.__class__):
            self._pos = target._pos
        else:
            self._pos = _to_vec2(target)
        self._dirty = 1
    
    def go_to_random(self):
        self.go_to(self._scene.random_pos())

    def glide_to(self, target: Coord | Sprite, duration: float):
        if isinstance(target, __class__):
            target = target._pos
        t1 = time.time()
        pos = self._pos.copy()
        while (elapsed := time.time() - t1) <= duration:
            self.move_to(_vec2_lerp(pos, target, elapsed/duration))
            self._wait_frame()
        self.move_to(target)
    
    def glide_to_random(self, duration: float):
        self.glide_to(self._scene.random_pos(), duration)

    def turn(self, amount: float):
        self.rotate_to(self._rot + amount)
    
    def turn_left(self, amount: float):
        self.rotate_to(self._rot + amount)
    
    def turn_right(self, amount: float):
        self.rotate_to(self._rot - amount)

    def point_to(self, target: Coord | Sprite):
        if isinstance(target, self.__class__):
            target = target._pos
        else:
            target = _to_vec2(target)
        v = target - self._pos
        angle = degrees(acos(v.x/v.length()))
        if target.y < self._pos.y:
            angle = 360 - angle
        self.rotate_to(angle)

    def rotate_to(self, angle: float):
        if self._rot != angle % 360:
            self._rot = angle % 360
            self._image = transform.rotate(self._org_image, self._rot)
            self._dim = Vector2(self.rect.width, self.rect.height)
            self._dirty = 1

    def bounce_on_edge(self):
        if (d := self._scene.rect.left - self.rect.left) > 0:
            self.rotate_to(180 - self._rot)
            self._pos.x += d
        elif (d := self._scene.rect.right - self.rect.right) < 0:
            self.rotate_to(180 - self._rot)
            self._pos.x += d
        
        if (d := self._scene.rect.top - self.rect.top) > 0:
            self.rotate_to(-self._rot)
            self._pos.y -= d
        elif (d := self._scene.rect.bottom - self.rect.bottom) < 0:
            self.rotate_to(-self._rot)
            self._pos.y -= d
    #endregion

    # region LOOKS
    # TODO: scaling and resizing
    # TODO: implement costumes
    # TODO: layer system
    # TODO: broadcasting system
    # TODO: saying and thinking
    # TODO: image effects

    def say(self, text: str):
        pass

    def say_for(self, text: str, duration: float = 2):
        pass

    def think(self, text: str):
        pass

    def think_for(self, text: str, duration: float = 2):
        pass

    def set_image(self, img: Image, keep_dim: bool = False):
        if keep_dim:
            self._image = transform.scale(
                load_image(img), self._dim)
        else:
            self._image = load_image(img)
        self._org_image = self._image.copy()
        self._dirty = 1

    def scale(
        self,
        factor: float,
    ):
        pass

    def resize(
        self,
        width: int = 0,
        height: int = 0,
        *,
        dw: int = 0,
        dh: int = 0,
        dim: Coord = None
    ):
        pass

    def go_to_front(self):
        pass

    def change_layer(self, offset: int):
        pass

    def set_layer(self, layer: int):
        pass
    
    def hide(self):
        if self._visible:
            self._visible = False
            self._dirty = 1

    def show(self):
        if not self._visible:
            self._visible = True
            self._dirty = 1
    #endregion

    # region EVENTS

    def on_key(self, event: PyScratchEvent):
        if f := getattr(self, event._name + "_" + _key_name(event.key), False):
            f()
    
    def on_mouse(self, event: PyScratchEvent):
        if f := getattr(self, event._name + "_" + _button_name(event.button), False):
            f()

    def broadcast(self, message: str):
        pass

    def broadcast_wait(self, message: str):
        pass

    def clone(self) -> Sprite:
        pass
    # endregion

    # region CONTROLS

    def wait(self, duration: float | int):
        time.sleep(duration)

    def repeat(self, times: int):
        pass

    def endless(self) -> bool:
        self._wait_frame()
        return self._alive
    
    def is_pressed(self, key: str) -> bool:
        self._wait_frame()
        return pygame.key.key_code(key) in self._app._pressed

    def wait_until(self, event):
        pass

    def repeat_until(self, event):
        pass
    # endregion

    # region PROPERTIES

    @property
    def image(self) -> Surface:
        return self._image

    @property
    def dirty(self) -> int:
        return self._dirty
    
    @dirty.setter
    def dirty(self, v: int):
        self._dirty = v

    @property
    def rect(self) -> Rect:
        if self.image:
            return self._image.get_rect(center=_convert_to_pg(self._pos))
        else:
            return Rect(0, 0, 0, 0)

    @property
    def pos(self) -> Vector2:
        return self._pos
    
    @property
    def x(self) -> float:
        return self._pos.x
    
    @property
    def y(self) -> float:
        return self._pos.y

    @property
    def dim(self) -> Vector2:
        return self._dim

    @property
    def width(self) -> float:
        return self._dim.x
    
    @property
    def height(self) -> float:
        return self._dim.y

    @property
    def visible(self) -> bool:
        return self._visible

    @property
    def layer(self) -> int:
        return self._layer
    
    @property
    def app(self) -> App:
        return self._app
    
    @property
    def scene(self) -> Scene:
        return self._scene
    
    @property
    def name(self) -> str:
        return self._name
    # endregion

    def update(self, *args, **kwargs):
        pass

    def _wait_frame(self):
        time.sleep(1/self.app.fps)


