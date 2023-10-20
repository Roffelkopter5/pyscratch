from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .scene import Scene

from .events import PyScratchEvent
from . import _get_logger

import pygame

_log = _get_logger(__name__)


class App:
    def __init__(self, name: str, scene: Optional[Scene] = None):
        _log.info(f"Starting app '{name}'")
        self._name = name

        if scene:
            self.set_scene(scene)
        else:
            self._scene = None

        _log.debug("Creating mainwindow")
        self._window = pygame.display.set_mode((640, 480))

        self._running = True
        self._pressed = set()
        self._clock = pygame.time.Clock()
        self._fps = 60

    def handle_events(self):
        _log.debug("Checking for unhandled pygame events")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                self._scene.dispatch(PyScratchEvent("on_game_end"))
            elif event.type == pygame.KEYDOWN:
                self._scene.dispatch(
                    PyScratchEvent("on_key_down", key=event.key, general="on_key")
                )
                self._pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self._scene.dispatch(
                    PyScratchEvent("on_key_up", key=event.key, general="on_key")
                )
                self._pressed.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._scene.dispatch(
                    PyScratchEvent(
                        "on_mouse_down", button=event.button, general="on_mouse"
                    )
                )
            elif event.type == pygame.MOUSEBUTTONUP:
                self._scene.dispatch(
                    PyScratchEvent(
                        "on_mouse_up", button=event.button, general="on_mouse"
                    )
                )

    def set_scene(self, scene: Scene):
        _log.info(f"Setting scene to '{scene._name}'")
        self._scene = scene
        scene.app = self

    def run(self):
        if self._scene:
            _log.info("Starting mainloop")
            while self._running:
                self.handle_events()
                self._scene.update()
                self._scene.render()
                self._window.blit(self._scene, (0, 0))
                pygame.display.update(self._scene.get_rect())
                self._clock.tick(self._fps)
                pygame.display.set_caption(str(self._clock.get_fps()))
        else:
            _log.error("No scene set")
        self.quit()

    def quit(self):
        _log.info(f"Stopping app '{self._name}'")
        _log.debug("Quitting pygame")
        pygame.quit()

    @property
    def fps(self) -> int:
        return self._fps

    @property
    def pressed(self) -> set[int]:
        return self._pressed
