import pygame
from pygame import Color, Surface
from blocks import Tetris_Piece, Piece_Color
from define import PIECE_LUT


class Board:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.cell_size = 32
        self.horizontal_lines = 22
        self.vertical_lines = 10
        self.grid_width = self.vertical_lines * self.cell_size
        self.grid_height = self.horizontal_lines * self.cell_size
        self.grid_color = Color((125, 125, 125))
        self.grid = [[0 for _ in range(self.vertical_lines)] for _ in range(self.horizontal_lines + 1)]
        


    def draw(self):
        self.draw_board()
        self.draw_blocks()

    def draw_board(self):
        for vl in range(self.vertical_lines + 1):
            pygame.draw.line(self.screen, self.grid_color, (vl * self.cell_size + self.x, 64 + self.y),
                             (vl * self.cell_size + self.x, self.grid_height + self.y))
        for hl in range(2, self.horizontal_lines + 1):
            pygame.draw.line(self.screen, self.grid_color, (0 + self.x, hl * self.cell_size + self.y),
                             (self.grid_width + self.x, hl * self.cell_size + self.y))

        pygame.draw.line(self.screen, "white", (self.x, self.y+64),
                         (self.x, self.grid_height + self.y), 2)

        pygame.draw.line(self.screen, "white", (self.vertical_lines * self.cell_size + self.x, self.y+64),
                         (self.vertical_lines * self.cell_size + self.x, self.grid_height + self.y), 2)

        pygame.draw.line(self.screen, "white", (0 + self.x, self.horizontal_lines * self.cell_size + self.y),
                         (self.grid_width + self.x, self.horizontal_lines * self.cell_size + self.y), 2)
        
    def draw_piece(self, current_piece):
        self.current_piece = current_piece
        self.current_piece.draw_current_piece(self.x, self.y)

    #handle piece on the board
    def draw_blocks(self):
        for _y in range(len(self.grid)):
            for _x in range(len(self.grid[0])):
                if self.grid[_y][_x] > 0:
                    real_x = _x * self.cell_size + self.x
                    real_y = (_y - 1)* self.cell_size + self.y
                    rect = pygame.Rect(real_x, real_y, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, Piece_Color[self.grid[_y][_x] - 1], rect)

    def add_piece(self, current_piece):
        piece_rotation = current_piece.piece_rotations[current_piece.current_rotation]
        for offset in piece_rotation:
            off_x, off_y = offset
            self.grid[current_piece.y - off_y + 3][current_piece.x + off_x - 1] = current_piece.piece + 1

#line clears
    def clear_lines(self):
        lines_cleared = 0
        for row in range(len(self.grid)-1, -1, -1):
            line = self.grid[row]
            if self.check_full_line(line):
                self.grid.pop(row)
                lines_cleared += 1

        for i in range(lines_cleared):
            self.grid.insert(0, [0 for _ in range(self.vertical_lines)])

    def check_full_line(self, line):
        for i in line:
            if i == 0:
                return False
        return True