import pygame

pygame.init()
game_font = pygame.font.Font(None, 50)
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
back_img = pygame.image.load("images/back.jpg")
pygame.display.set_caption("First Game")
player_step = 1
alien_step = 0.5
shell_step = 1
score = 0
lives = 3
