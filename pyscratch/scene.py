from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App
    from .sprite import Sprite
    from .locals import Coord
    from .events import PyScratchEvent

from . import _get_logger

from pygame.sprite import LayeredDirty
from pygame.surface import Surface
import threading

_log = _get_logger(__name__)

class Scene(Surface):
    def __init__(self, name: str, size: Coord = None, bg: Surface = None):
        self._name = name

        if size:
            super().__init__(size)
        else:
            super().__init__((640, 480))

        self._figures = LayeredDirty()
        self._bg = bg
        self._app = None

    def set_bg(self, img: str | Surface):
        pass

    def add_figur(self, sprite: Sprite):
        _log.info(f"Adding sprite '{sprite._name}' to scene '{self._name}'")
        if not sprite._scene:
            self._figures.add(sprite)
            sprite._scene = self
        else:
            _log.error(f"Each sprite can only be in on scene")
    
    def update(self):
        pass

    def dispatch(self, event: PyScratchEvent):
        for sprite in self._figures:
            if f := getattr(sprite, event._name, None):
                _log.info(f"Dispatching event '{event._name}' with {event._kwargs} to '{sprite._name}'")
                threading.Thread(target=f, args=(event,), daemon=True).start()

    def render(self):
        _log.debug(f"Rendering scene '{self._name}'")
        if self._bg:
            self._figures.draw(self, self._bg)
        else:
            self._figures.draw(self)
    
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