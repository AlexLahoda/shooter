import pygame
from audio import s_shell
from images import s_image
from parameters import screen_height
from alien import Alien

pygame.init()


class Shell:
    """Class of shell, contains functions which provides its behaviour """
    shells = []

    def __init__(self, step: float, owner):
        self.step = step
        self.owner = owner
        self.image = s_image
        self.width, self.height = self.image.get_size()
        self.x, self.y = owner.x + owner.width / 2 - self.width / 2, owner.y - self.height
        if isinstance(self.owner, Alien):
            self.image = pygame.transform.rotate(self.image, 180)
            self.y = owner.y
        s_shell.play()
        owner.is_fired = True

    def move(self):
        """Provides shells movements"""
        if isinstance(self.owner, Alien):
            self.y += self.step
        else:
            self.y -= self.step
        if self.y > screen_height or self.y < 0:
            self.rem()

    @staticmethod
    def new(step, owner):
        """Create new shell"""
        Shell.shells.append(Shell(step, owner))

    def rem(self):
        """Remove shell"""
        self.owner.is_fired = False
        Shell.shells.remove(self)
