import pygame

pygame.init()
game_font = pygame.font.Font(None, 50)
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
back_img = pygame.image.load("images/back.jpg")
pygame.display.set_caption("First Game")
