import random
from data.scripts.extract_images import extract_images
from data.scripts.tile import Tile


class GameBoard:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.game_modes = {
            'easy': [10, 10],
            'medium': [15, 40],
            'hard': [20, 80]
        }
        self.mode = 'easy'
        self.tile_size = None
        self.tile_grid = None
        self.mine_number = None
        self.min_positions = []
        self.mines_to_discover = None
        self.ratio = 1
        self.images = None
        self.board = []
        self.flags = None
        self.game_over = False

    def set_game(self, mode):
        self.mode = mode
        self.tile_grid = self.game_modes[self.mode][0]
        self.mine_number = self.game_modes[self.mode][1]
        self.flags = self.mine_number
        self.tile_size = self.screen_size[1] / self.tile_grid
        self.ratio = self.tile_size / 16
        self.images = extract_images(self.ratio)
        self.place_mines()

    def place_mines(self):
        self.board = [[0 for _ in range(self.tile_grid)] for _ in range(self.tile_grid)]
        mines = self.mine_number
        while mines > 0:
            position = [random.randint(0, self.tile_grid - 1), random.randint(0, self.tile_grid - 1)]
            if self.board[position[0]][position[1]] != 'mine':
                self.min_positions.append(position)
                self.board[position[0]][position[1]] = 'mine'
                mines -= 1
        self.place_numbers()

    def place_numbers(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for i in range(self.tile_grid):
            for j in range(self.tile_grid):
                if self.board[i][j] == 'mine':
                    continue

                number = 0
                for direction in directions:
                    ni, nj = i + direction[0], j + direction[1]

                    if 0 <= ni < self.tile_grid and 0 <= nj < self.tile_grid:
                        if self.board[ni][nj] == 'mine':
                            number += 1

                self.board[i][j] = number
        self.tile_generation()

    def tile_generation(self):
        for i in range(self.tile_grid):
            for j in range(self.tile_grid):
                tile_value = self.board[i][j]
                if tile_value != 'mine':
                    self.board[i][j] = Tile(i, j, self.images[str(tile_value)])
                else:
                    self.board[i][j] = Tile(i, j, self.images['mine'])

    def display_board(self, screen):
        for i in range(self.tile_grid):
            for j in range(self.tile_grid):
                x, y = self.tile_size * j, self.tile_size * i
                if self.board[i][j].discovered:
                    screen.blit(self.board[i][j].type, (x, y))
                else:
                    screen.blit(self.images['hiding_tile'], (x, y))

                if self.board[i][j].flagged:
                    screen.blit(self.images['flag'], (x, y))

    def uncover_tile(self, i, j):
        if 0 <= i < self.tile_grid and 0 <= j < self.tile_grid:
            if not self.board[i][j].flagged:
                self.board[i][j].discover_tile()

                if self.board[i][j].type == self.images['mine']:
                    self.game_over = True
                    self.discover_all_mines()

                elif self.board[i][j].type == self.images['0']:
                    self.uncover_adjacent_tiles(i, j)

    def uncover_adjacent_tiles(self, i, j):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for direction in directions:
            ni, nj = i + direction[0], j + direction[1]
            if 0 <= ni < self.tile_grid and 0 <= nj < self.tile_grid:
                if not self.board[ni][nj].discovered and not self.board[ni][nj].flagged:
                    self.board[ni][nj].discover_tile()

                    if self.board[ni][nj].type == self.images['0']:
                        self.uncover_adjacent_tiles(ni, nj)

    def discover_all_mines(self):
        self.mines_to_discover = []
        for i in range(self.tile_grid):
            for j in range(self.tile_grid):
                if self.board[i][j].type == self.images['mine']:
                    self.mines_to_discover.append((i, j))

    def place_flag(self, i, j):
        if 0 <= i < self.tile_grid and 0 <= j < self.tile_grid and not self.board[i][j].discovered:
            if self.board[i][j].flagged:
                self.board[i][j].switch_flagged()
                self.flags += 1
            elif self.flags > 0:
                self.board[i][j].switch_flagged()
                if self.board[i][j].flagged:
                    self.flags -= 1

    def check_victory(self):
        if self.flags == 0:
            for i in range(self.tile_grid):
                for j in range(self.tile_grid):
                    if self.board[i][j].type == self.images['mine'] and not self.board[i][j].flagged:
                        return False
            return True
