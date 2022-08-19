from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App
    from .sprite import Sprite
    from .locals import Coord
    from .events import PyScratchEvent

from . import _get_logger
from .utils import _to_vec2

from pygame.sprite import LayeredDirty
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.rect import Rect
import threading
from random import randint
import os.path
import importlib

_log = _get_logger(__name__)

class Scene(Surface):
    def __init__(self, name: str, size: Coord = None, bg: Surface = None):
        self._name = name

        if size:
            self._size = _to_vec2(size)
            super().__init__(size)
        else:
            self._size = Vector2(640, 480)
            super().__init__((640, 480))

        self._figures = LayeredDirty()
        self._bg = bg
        self._app = None

    def set_bg(self, img: str | Surface):
        pass

    def add_sprite(self, sprite: Sprite):
        _log.info(f"Adding sprite '{sprite._name}' to scene '{self._name}'")
        if not sprite._scene:
            self._figures.add(sprite)
            sprite._scene = self
        else:
            _log.error(f"Each sprite can only be in on scene")
    
    def load_sprites(self, sprite_path, count: int = 0):
        if os.path.isfile(sprite_path) and (parts := os.path.splitext(os.path.split(sprite_path)[1]))[1] == ".py":
            name = parts[0]
            sprite = getattr(importlib.import_module(name), name.capitalize())
            for _ in range(count):
                self.add_sprite(sprite())


    def update(self):
        pass

    def dispatch(self, event: PyScratchEvent):
        for sprite in self._figures:
            if event._general:
                _log.info(f"Dispatching event '{event._name}' with {event._kwargs} to '{sprite._name}' as general")
                threading.Thread(target=getattr(sprite, event._general), args=(event,), daemon=True).start()
            if f := getattr(sprite, event._name, None):
                _log.info(f"Dispatching event '{event._name}' with {event._kwargs} to '{sprite._name}'")
                threading.Thread(target=f, args=(event,), daemon=True).start()

    def render(self):
        _log.debug(f"Rendering scene '{self._name}'")
        if self._bg:
            self._figures.draw(self, self._bg)
        else:
            self._figures.draw(self)
    
    def random_pos(self) -> Vector2:
        w_h, h_h = self._size.x // 2, self._size.y // 2
        return Vector2(randint(-w_h, w_h), randint(-h_h, h_h))

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def app(self) -> App:
        return self._app
    
    @app.setter
    def app(self, app):
        self._app = app
        for sprite in self._figures:
            sprite._app = app
    
    @property
    def rect(self) -> Rect:
        return self.get_rect()