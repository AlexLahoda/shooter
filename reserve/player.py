import pygame
from images import p_image
from audio import s_crash
from shell import Shell
from parameters import screen_height, screen_width, player_step, shell_step

pygame.init()

class Player:
    def __init__(self, step):
        self.step = step
        self.image = p_image
        self.width, self.height = self.image.get_size()
        self.y, self.x = (screen_height - self.height), (screen_width - self.width) / 2
        self.moves_left, self.moves_right = False, False
        self.lives = 3
        self.is_fired = False
        self.firing = False

    def movements(self):
        fire = False
        if self.moves_left and self.x >= self.step:
            self.x -= self.step
        if self.moves_right and self.x <= screen_width - self.width - self.step:
            self.x += self.step
        if self.firing and not self.is_fired:
            fire = True
        return fire

    def explode(self):
        s_crash.play()
        t = (self.x, self.y)
        self.y, self.x = (screen_height - self.height), (screen_width - self.width) / 2
        self.lives -= 1
        return t
