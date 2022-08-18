from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .locals import Coord

import pygame
from pygame.surface import Surface

class BackgroundColor(Surface):
    def __init__(self, size: Coord, color):
        super().__init__(size)
        self.fill(color)

class Triangle(Surface):
    def __init__(self, size: Coord, color):
        super().__init__(size, pygame.SRCALPHA)
        pygame.draw.polygon(self, color, ((0, 0), (size[0], size[1]//2), (0, size[1])))