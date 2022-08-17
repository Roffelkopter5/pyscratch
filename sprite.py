from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
import os
import datetime
from random import randint
from typing import Sequence
from pygame.math import Vector2
from pygame.sprite import DirtySprite, LayeredDirty
from pygame.surface import Surface
from pygame.rect import Rect
from pygame import transform
from math import sin, cos, radians, acos, degrees
import time
import threading
import pygame
from utils import load_image, vec2_lerp, convert_to_pg, convert_to_ps
from locals import Image, Coord

pygame.init()


log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')

my_handler = RotatingFileHandler(f"logs/PyScratchLog.log", mode='a', maxBytes=5*1024*1024, 
                                 backupCount=5, encoding=None, delay=False)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

_log = logging.getLogger('root')
_log.setLevel(logging.INFO)

_log.addHandler(my_handler)

class BackgroundColor(Surface):
    def __init__(self, size: Coord, color):
        super().__init__(size)
        self.fill(color)

class Triangle(Surface):
    def __init__(self, size: Coord, color):
        super().__init__(size, pygame.SRCALPHA)
        pygame.draw.polygon(self, color, ((0, 0), (size[0], size[1]//2), (0, size[1])))

class PyScratchEvent:
    def __init__(self, name: str, **kwargs):
        self._name = name
        self._kwargs = kwargs
        for k, v in kwargs.items():
            self.__setattr__(k, v)

class Sprite(DirtySprite):
    def __init__(self, image: Image):
        super().__init__()

        self._pos = Vector2()
        self._dim = Vector2()
        self._rot = 0.0
        self._alive = True
        self._app: App = None
        self._scene: Scene = None
        self._name = self.__class__.__name__

        self.set_image(image)
        self._dirty = 1
        self._visible = True
        self._layer = 0


    ### Motion ###
    # TODO: bounce on edge
    # TODO: Move vector conversion to utils

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
        elif not isinstance(target, Vector2):
            self._pos = Vector2(target)
        self._dirty = 1
    
    def go_to_random(self):
        self.go_to(self._scene.random_pos())

    def glide_to(self, target: Coord | Sprite, duration: float):
        if isinstance(target, __class__):
            target = target._pos
        t1 = time.time()
        pos = self._pos.copy()
        while (elapsed := time.time() - t1) <= duration:
            self.move_to(vec2_lerp(pos, target, elapsed/duration))
            self._wait_frame()
        self.move_to(target)
    
    def glide_to_random(self, duration: float):
        self.glide_to(self._scene.random_pos(), duration)

    def turn(self, amount: float):
        self.point_in(self._rot + amount)
    
    def turn_left(self, amount: float):
        self.point_in(self._rot + amount)
    
    def turn_right(self, amount: float):
        self.point_in(self._rot - amount)

    def point_to(self, target: Coord | Sprite):
        if isinstance(target, self.__class__):
            target = target._pos
        else:
            target = Vector2(target)
        v = target - self._pos
        angle = degrees(acos(v.x/v.length()))
        if target.y < self._pos.y:
            angle = 360 - angle
        self.point_in(angle)

    def point_in(self, angle: float):
        self._rot = angle % 360
        self._image = transform.rotate(self._org_image, self._rot)
        self._dim = Vector2(self.rect.width, self.rect.height)
        self._dirty = 1

    def on_edge_bounce(self):
        pass

    


    ### Looks ###
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
    
    ### Events ###

    def on_key_down(self, event: PyScratchEvent):
        if f := getattr(self, event._name + "_" + pygame.key.name(event.key), False):
            f()

    def on_key_up(self, event: PyScratchEvent):
        if f := getattr(self, event._name + "_" + pygame.key.name(event.key), False):
            f()

    def broadcast(self, message: str):
        pass

    def broadcast_wait(self, message: str):
        pass

    def clone(self) -> Sprite:
        pass


    ### Control ###

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

    ### Properties ###

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
            return self._image.get_rect(center=convert_to_pg(self._pos))
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


    ### Private ###

    def update(self, *args, **kwargs):
        pass

    def _wait_frame(self):
        time.sleep(1/self.app.fps)


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


class App:
    def __init__(self, name: str, scene: Scene = None):
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
                self._scene.dispatch(PyScratchEvent("on_key_down", key=event.key))
                self._pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self._scene.dispatch(PyScratchEvent("on_key_up", key=event.key))
                self._pressed.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._scene.dispatch(PyScratchEvent("on_mouse_down", button=event.button))
            elif event.type == pygame.MOUSEBUTTONUP:
                self._scene.dispatch(PyScratchEvent("on_mouse_up", button=event.button))

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


class Figur(Sprite):
    def __init__(self):
        super().__init__(Triangle((40, 40), (255, 0, 0)))

app = App("PlanetX")
scene = Scene("First Scene", bg=BackgroundColor((640, 480), (255, 255, 255)))
figur = Figur()
scene.add_figur(figur)
app.set_scene(scene)
app.run()