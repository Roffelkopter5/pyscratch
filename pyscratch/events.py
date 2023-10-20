from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene


class EventHandler:
    def __init__(self):
        self._listener = {
            "on_key_down": {},
            "on_key_up": {},
            "on_mouse_down": {},
            "on_mouse_up": {},
        }

    def load_listeners(self, scene: Scene):
        for figur in scene._figures:
            for name in figur.__dict__:
                print(name)


class PyScratchEvent:
    def __init__(self, name: str, general: str = "", **kwargs):
        self._name = name
        self._kwargs = kwargs
        self._general = general
        for k, v in kwargs.items():
            self.__setattr__(k, v)
