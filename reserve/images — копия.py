import pygame

pygame.init()

expl_img = pygame.image.load("images/explode.png")
expl_img.set_colorkey((255, 255, 255))
a_image = pygame.image.load('images/alien.png')
a_image.set_colorkey((32, 52, 71))
p_image = pygame.image.load('images/Space_ship.png')
p_image.set_colorkey((32, 52, 71))
s_image = pygame.image.load('images/shell.png')
s_image.set_colorkey((32, 52, 71))