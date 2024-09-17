import pygame
import time
from pygame.locals import *
from data.scripts.image_functions import import_image, scale_image_size
from data.scripts.game_board import GameBoard
from data.scripts.score_board import ScoreBoard
from data.scripts.text import font

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.screen_size = [700, 600]
        self.screen = pygame.display.set_mode(self.screen_size)
        self.score_screen = pygame.Surface([self.screen_size[0] - self.screen_size[1], self.screen_size[1]])

        pygame.display.set_caption("Minesweeper")
        icon = import_image('icon.png', (255, 255, 255))
        pygame.display.set_icon(icon)

        # Importing Images---------------------------#
        self.game_over_image = scale_image_size(import_image("game_over.png"), self.screen_size)
        self.win = import_image('win.png', (255, 255, 255))
        self.lose = import_image('lose.png', (255, 255, 255))
        self.home_bg = import_image('home_back.png')
        self.button_back = import_image('button_back.png')

        self.home_buttons = {
            "play": [import_image('play_button.png'), import_image('play_button_hover.png')],
            "exit": [import_image('exit_button.png'), import_image('exit_button_hover.png')],
        }

        self.mode_buttons = {
            "easy": [import_image('easy.png'), import_image('easy_hover.png')],
            "medium": [import_image('medium.png'), import_image('medium_hover.png')],
            "hard": [import_image('hard.png'), import_image('hard_hover.png')]
        }

        self.text = font('small_font.png', (10, 0, 0), 5)

        # Importing sounds---------------------------------#
        pygame.mixer.music.load('data/sounds/background.mp3')
        pygame.mixer.music.play(loops=-1)

        self.mine_sound = pygame.mixer.Sound('data/sounds/mine.mp3')
        self.flag_sound = pygame.mixer.Sound('data/sounds/flag.mp3')

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.fps = 30

        self.game_board = GameBoard(self.screen_size)
        self.level = 'easy'
        self.game_board.set_game(self.level)

        self.score_board = ScoreBoard(self.score_screen)

        self.gaming_mode = False

        self.victory = False
        self.run = True

    def home_screen(self):
        while self.run:
            self.screen.blit(self.home_bg, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            pos = [(self.screen_size[0] - self.button_back.get_width()) // 2,
                   (self.screen_size[1] - self.button_back.get_height()) // 2]

            if self.gaming_mode:
                offset = 0
                for button in self.mode_buttons:
                    button_rect = pygame.Rect(pos[0], pos[1] + offset - 100, self.mode_buttons[button][0].get_width(),
                                              self.mode_buttons[button][0].get_height())
                    if button_rect.collidepoint(mouse_pos):
                        self.screen.blit(self.mode_buttons[button][1], button_rect.topleft)
                        if pygame.mouse.get_pressed()[0]:
                            self.mine_sound.play()
                            self.game_board.set_game(button)
                            self.main_loop()
                    else:
                        self.screen.blit(self.mode_buttons[button][0], button_rect.topleft)

                    offset += 100
            else:
                offset = 0
                for button in self.home_buttons:
                    button_rect = pygame.Rect(pos[0], pos[1] + offset, self.home_buttons[button][0].get_width(),
                                              self.home_buttons[button][0].get_height())
                    if button_rect.collidepoint(mouse_pos):
                        self.screen.blit(self.home_buttons[button][1], button_rect.topleft)
                        if pygame.mouse.get_pressed()[0]:
                            self.mine_sound.play()
                            if button == "play":
                                self.gaming_mode = True
                                time.sleep(0.5)
                            elif button == "exit":
                                pygame.quit()
                                return
                    else:
                        self.screen.blit(self.home_buttons[button][0], button_rect.topleft)

                    offset += 100

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False

                if event.type == MOUSEBUTTONDOWN:
                    pass

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()

    def main_loop(self):
        last_mine_discovered_time = 0
        uncover_interval = 200
        self.start_time = pygame.time.get_ticks()

        while self.run:
            mouse_pos = pygame.mouse.get_pos()
            elapsed_time = pygame.time.get_ticks() - self.start_time
            self.screen.fill((185, 122, 87))
            self.score_screen.fill((0, 0, 0))
            pygame.draw.line(self.score_screen, (255, 255, 255), (0, 0), (0, self.screen_size[1]), 2)

            self.game_board.display_board(self.screen)
            self.score_board.display_flags(self.game_board.flags)
            self.score_board.display_time(elapsed_time)

            if self.game_board.game_over and self.game_board.mines_to_discover:
                current_time = pygame.time.get_ticks()
                if current_time - last_mine_discovered_time >= uncover_interval:
                    i, j = self.game_board.mines_to_discover.pop(0)
                    self.game_board.board[i][j].discover_tile()
                    last_mine_discovered_time = current_time
            elif self.game_board.game_over and not self.game_board.mines_to_discover:
                time.sleep(2)
                self.game_over()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False

                if event.type == MOUSEBUTTONDOWN:
                    pos = [int(mouse_pos[1] // self.game_board.tile_size),
                           int(mouse_pos[0] // self.game_board.tile_size)]
                    if event.button == 1:
                        self.game_board.uncover_tile(*pos)
                        self.mine_sound.play()
                    if event.button == 3:
                        self.game_board.place_flag(*pos)
                        self.flag_sound.play()
                        if self.game_board.check_victory():
                            self.victory = True
                            time.sleep(2)
                            self.game_over()

            self.screen.blit(self.score_screen, [self.screen_size[1], 0])

            pygame.display.update()
            self.clock.tick(self.fps)

    def game_over(self):
        while self.run:
            self.screen.blit(self.game_over_image, (0, 0))
            self.screen.blit(self.win if self.victory else self.lose, (
                (self.screen_size[0] - self.win.get_width()) // 2,
                (self.screen_size[1] - self.win.get_height()) // 2 + 150))

            self.text.display_fonts(self.screen, "Press r to continue...", [170, 570])

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.victory = False
                        self.gaming_mode = False
                        self.game_board.game_over = False
                        self.game_board.mines_to_discover = None
                        self.home_screen()

                if event.type == MOUSEBUTTONDOWN:
                    pass

            pygame.display.update()
            self.clock.tick(self.fps)


game = Game()
game.home_screen()
