import sys
from parameters import *
import button
from images import *
from alien import *
from player import *
from parameters import alien_step, player_step, shell_step, score

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


class Game:
    def __init__(self, p_step, a_step, s_step, sc):
        self.p_step = p_step
        self.a_step = a_step
        self.s_step = s_step
        self.sc = sc

    def save(self):
        pass

    def start(self):
        game_started = True
        tmp = []
        player = Player(self.p_step)
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
                        player.moves_left, player.moves_right, player.is_fired = self.menu(game_started)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.moves_left = False
                    if event.key == pygame.K_RIGHT:
                        player.moves_right = False
                    if event.key == pygame.K_SPACE:
                        player.firing = False
            if player.movements():
                Shell.new(self.s_step, player)

            if pygame.time.get_ticks() - timer > 4000:
                self.a_step *= 1.05
                self.p_step *= 1.05
                self.s_step *= 1.05
                Alien.new(self.a_step)
                timer = pygame.time.get_ticks()

            screen.blit(back_img, (0, 0))
            for shell in Shell.shells:
                shell.move()
                if isinstance(shell.owner, Player):
                    for alien in Alien.aliens:
                        if (alien.x < shell.x < (alien.x + alien.width - shell.width) and
                                alien.y < shell.y < alien.y + alien.height - shell.height):
                            tmp.append((alien.rem(), pygame.time.get_ticks()))
                            shell.rem()
                            self.sc += alien_step * 5
                else:
                    if (shell.y > player.y and
                        player.x - shell.width + 1 < shell.x <
                            player.x + player.width - 1):
                        tmp.append((player.explode(), pygame.time.get_ticks()))
                        shell.rem()
                screen.blit(shell.image, (shell.x, shell.y))

            for alien in Alien.aliens:
                if alien.movements(player.x, player.width):
                    Shell.new(self.s_step, alien)
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

            button.print_txt(f"Your score: {int(self.sc)}", "white", (20, 20))
            button.print_txt(f"Lives: {int(player.lives)}", "white", (650, 20))
            pygame.display.update()

        game_over_text = game_font.render(f"Game over", True, 'red')
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (screen_width/2, screen_height/2)
        screen.blit(game_over_text, game_over_rect)
        pygame.display.update()
        pygame.time.wait(5000)
        self.menu()

    def menu(self, game_running=False):
        menu_show = True
        back_menu = pygame.image.load("images/back_menu.jpg")
        start_btn = button.Button(200, 50, "Start game")
        save_btn = button.Button(200, 50, "Save game")
        exit_btn = button.Button(200, 50, "Exit game")
        while menu_show:
            screen.blit(back_menu, (0, 0))
            if game_running:
                button.print_txt("Pause. Press Esc to continue!", "white", (160, 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if game_running and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False, False, False
            start_btn.draw((285, 150), self.start, menu_show)
            save_btn.draw((285, 250))
            exit_btn.draw((285, 360), sys.exit)
            pygame.display.update()


game = Game(player_step, alien_step, shell_step, score)
game.menu()
