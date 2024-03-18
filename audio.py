import pygame

pygame.init()
pygame.mixer.music.load("audio/back_sound.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)
s_hit = pygame.mixer.Sound("audio/hit.ogg")
s_crash = pygame.mixer.Sound("audio/ships_crash.ogg")
s_shell = pygame.mixer.Sound("audio/shell.ogg")
s_hit.set_volume(0.1)
s_crash.set_volume(0.1)
s_shell.set_volume(0.1)