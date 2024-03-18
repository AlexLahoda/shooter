import math
import random
import sys
import pygame
from parameters import *
import button
from audio import *
from images import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


def save():
    pass

def start():
    game_started = True
    shells = []
    tmp = []
    aliens = []

    class Alien:
        def __init__(self, step):
            self.image = a_image
            self.width, self.height = self.image.get_size()
            self.x, self.y = random.randint(0, screen_width - self.width), 0
            self.step = step
            self.change = 0
            self.is_fired = False
            self.round = False
            self.center = (400, 300)
            self.head = 1

        def movements(self, dest_x, dest_width):
            dst = dest_x + dest_width / 2
            if (dst - self.step < self.x + self.width / 2 < dst) and not self.is_fired:
                shells.append(Shell(shell_step / 4, self))

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

        def side(self, dest):
            change = abs(self.x - dest) / ((self.y - screen_height) / self.step)
            if dest > self.x:
                self.change = -change
            if dest < self.x:
                self.change = change
            print(self.change)

        def rem(self):
            s_hit.play()
            t = (alien.x, alien.y)
            aliens.remove(self)
            return t

    class Player:
        def __init__(self):
            self.image = p_image
            self.width, self.height = self.image.get_size()
            self.y, self.x = (screen_height - self.height), (screen_width - self.width) / 2
            self.moves_left, self.moves_right = False, False
            self.lives = 3
            self.is_fired = False
            self.firing = False

        def movements(self):
            if self.moves_left and self.x >= player_step:
                self.x -= player_step
            if self.moves_right and self.x <= screen_width - self.width - player_step:
                self.x += player_step
            if self.firing and not self.is_fired:
                shells.append(Shell(shell_step, player))

        def explode(self):
            s_crash.play()
            t = (self.x, self.y)
            self.y, self.x = (screen_height - self.height), (screen_width - self.width) / 2
            player.lives -= 1
            return t

    class Shell:
        def __init__(self, step, owner):
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
            if isinstance(self.owner, Alien):
                self.y += 1
            else:
                self.y -= 1
            if self.y > screen_height or self.y < 0:
                self.rem()

        def rem(self):
            self.owner.is_fired = False
            shells.remove(self)


    player = Player()


    score = 0
    player_step = 0.5
    shell_step = 0.5
    alien_step = 0.2
    timer = pygame.time.get_ticks()

    while player.lives:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.moves_left = True
                if event.key == pygame.K_RIGHT:
                    player.moves_right = True
                if event.key == pygame.K_SPACE:
                    player.firing = True
                if event.key == pygame.K_ESCAPE:
                    player.moves_left, player.moves_right, player.is_fired = menu(game_started)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.moves_left = False
                if event.key == pygame.K_RIGHT:
                    player.moves_right = False
                if event.key == pygame.K_SPACE:
                    player.firing = False
        player.movements()

        if pygame.time.get_ticks() - timer > 4000:
            alien_step *= 1.01
            player_step *= 1.01
            shell_step *= 1.01
            print(alien_step)
            aliens.append(Alien(alien_step))
            timer = pygame.time.get_ticks()

        screen.blit(back_img, (0, 0))

        for shell in shells:
            shell.move()
            if isinstance(shell.owner, Player):
                for alien in aliens:
                    if (alien.x < shell.x < (alien.x + alien.width - shell.width) and
                            alien.y < shell.y < alien.y + alien.height - shell.height):
                        tmp.append((alien.rem(), pygame.time.get_ticks()))
                        shell.rem()
                        score += alien_step * 5
            else:
                if (shell.y > player.y and
                    player.x - shell.width + 1 < shell.x <
                        player.x + player.width - 1):
                    tmp.append((player.explode(), pygame.time.get_ticks()))
                    shell.rem()
            screen.blit(shell.image, (shell.x, shell.y))

        for alien in aliens:
            alien.movements(player.x, player.width)
            screen.blit(alien.image, (alien.x, alien.y))
            if (alien.y > player.y and
                    player.x - alien.width + 1 < alien.x <
                    player.x + player.width - 1):
                tmp.append((player.explode(), pygame.time.get_ticks()))
                tmp.append((alien.rem(), pygame.time.get_ticks()))

        for i in tmp:
            """show explode on the place of destroyed object"""
            screen.blit(expl_img, i[0])
            if pygame.time.get_ticks() - i[1] > 200:
                tmp.remove(i)
        screen.blit(player.image, (player.x, player.y))

        button.print_txt(f"Your score: {int(score)}","white", (20, 20))
        button.print_txt(f"Lives: {int(player.lives)}", "white", (650, 20))
        pygame.display.update()

    game_over_text = game_font.render(f"Game over", True, 'red')
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (screen_width/2, screen_height/2)
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()
    pygame.time.wait(5000)
    menu()


def menu(game_running=False):
    menu_show = True
    back_menu = pygame.image.load("images/back_menu.jpg")
    start_btn = button.Button(200, 50, "Start game")
    save_btn = button.Button(200, 50, "Save game")
    exit_btn = button.Button(200, 50, "Exit game")
    while menu_show:
        screen.blit(back_menu, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if game_running:
                button.print_txt("Pause. Press Esc to continue!", "white", (160, 100))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False, False, False
        start_btn.draw((285, 150), start, menu_show)
        save_btn.draw((285, 250))
        exit_btn.draw((285, 360), sys.exit)
        pygame.display.update()


menu()

