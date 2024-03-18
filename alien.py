import math
import random
import pygame
from audio import s_hit
from images import a_image
from parameters import screen_width, screen_height

pygame.init()


class Alien:
    """Contains list of aliens and methods which provide their behaviour"""
    aliens = []

    def __init__(self, step: float):
        self.image = a_image
        self.width, self.height = self.image.get_size()
        self.x, self.y = random.randint(0, screen_width - self.width), 0
        self.step = step
        self.change = 0
        self.is_fired = False
        self.round = False
        self.center = (400, 300)
        self.head = 1

    @staticmethod
    def new(step):
        """Create new alien"""
        Alien.aliens.append(Alien(step))

    def movements(self, dest_x: int, dest_width: int):
        """logic of alien flight"""
        fire = False
        dst = dest_x + dest_width / 2
        if (dst - self.step < self.x + self.width / 2 < dst) and not self.is_fired:
            fire = True
        if 200 < self.y < 200 + self.step / 2 and not self.round:
            self.round = True
            if (self.x - dest_x) / abs(self.x - abs(dest_x)) <= 0:
                self.center = (self.x - 100, self.y)
                self.change = 90
            else:
                self.center = (self.x + 100, self.y)
                self.change = 270
                self.head = -1
        if not self.round:
            self.y += self.step
            self.x += self.change
        else:
            self.change += self.step * self.head
            self.x = self.center[0] + 100 * math.sin(self.change * 3.14 / 180)
            self.y = self.center[1] + 100 * math.cos(self.change * 3.14 / 180)
            if self.change > 275 or self.change < 85:
                self.round = False
                self.side(dest_x)
        if 0 < self.y <= self.step:
            self.side(dest_x)
        if self.y > screen_height:
            self.y -= screen_height
            if self.x >= screen_width:
                self.x = random.randint(0, 100)
            if self.x <= 0:
                self.x = random.randint(700, screen_width)
        return fire

    def side(self, dest):
        """Calculate to which side alien will move"""
        change = abs(self.x - dest) / ((self.y - screen_height) / self.step)
        if dest > self.x:
            self.change = -change
        if dest < self.x:
            self.change = change

    def rem(self):
        """Delete alien from list"""
        s_hit.play()
        t = (self.x, self.y)
        Alien.aliens.remove(self)
        return t  # send position to set explosion
