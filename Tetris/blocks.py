from enum import Enum
from random import shuffle
from define import PIECE_LUT
import pygame

class Piece_Type(Enum):
    PieceI = 0
    PieceT = 1
    PieceO = 2
    PieceS = 3
    PieceZ = 4
    PieceL = 5
    PieceJ = 6


Piece_Color = {
    0 : pygame.Color("turquoise1"),
    1 : pygame.Color("darkorchid"),
    2 : pygame.Color("gold"),
    3 : pygame.Color("chartreuse2"),
    4 : pygame.Color("orangered"),
    5 : pygame.Color("chocolate1"),
    6 : pygame.Color("royalblue"),
}


class Tetris_Piece:
    def __init__(self, screen, board, piece):
        self.screen = screen
        self.board = board
        self.board_grid = board.grid
        self.cell_size = self.board.cell_size
        self.x = 5
        self.y = -2
        self.current_rotation = 0 # initial rotation state

        self.piece = piece
        self.type = Piece_Type(piece)
        self.locked = False
        self.color = Piece_Color[piece]
        self.piece_rotations = PIECE_LUT[piece]

    def draw_current_piece(self, board_x, board_y):
        self.piece_rotation = self.piece_rotations[self.current_rotation]
        for offset in self.piece_rotation:
            off_x, off_y = offset
            real_x = (self.x + off_x - 1) * self.cell_size + board_x
            real_y = (self.y - off_y + 2) * self.cell_size + board_y
            rect = pygame.Rect(real_x + 1, real_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.color, rect)

    def draw_other_piece(self, x, y):
        self.piece_rotation = self.piece_rotations[self.current_rotation]
        for offset in self.piece_rotation:
            off_x, off_y = offset
            real_x = (off_x + 1) * self.cell_size + x
            real_y = (-off_y + 2) * self.cell_size + y
            rect = pygame.Rect(real_x, real_y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.color, rect)

    # movements of the piece
    def move_left(self):
        if self.check_move(self.x-1, self.y, self.current_rotation):
            self.x -= 1
            return True
        else:
            return False
        
    def move_right(self):
        if self.check_move(self.x+1, self.y, self.current_rotation):
            self.x += 1
            return True
        else:
            return False
        
    def move_down(self):
        if self.check_move(self.x, self.y + 1, self.current_rotation):
            self.y += 1
            return True
        else:
            return False
    
    def rotate_cw(self):
        if self.check_move(self.x, self.y, (self.current_rotation + 1) % 4):
            self.current_rotation = (self.current_rotation + 1) % 4
            return True
        return False
    
    def rotate_ccw(self):
        if self.check_move(self.x, self.y, (self.current_rotation - 1) % 4):
            self.current_rotation = (self.current_rotation - 1) % 4
            return True
        return False
    
    def hard_drop(self):
        while self.check_move(self.x, self.y + 1, self.current_rotation):
            self.move_down()
        self.locked = True
    #check if move/rotation is possible
    def check_move(self, x, y, rotation):
        piece_rotation = self.piece_rotations[rotation]
        for offset in piece_rotation:
            off_x, off_y = offset
            try:
                if self.board_grid[y - off_y + 3][x + off_x - 1] != 0 or off_x + x < 1:
                    return False
            except IndexError:
                return False
        return True
    
    #hold piece handling
    def reset(self):
        self.x = 5
        self.y = -2
        self.current_rotation = 0

    '''def __str__(self):
        return(f"Piece Type: {self.type} \nPiece Color: {self.color} \n Piece Rotations : {self.piece_rotations}")'''


def generate_new_bag(screen, board):
    bag = [Tetris_Piece(screen, board, 0),
           Tetris_Piece(screen, board, 1),
           Tetris_Piece(screen, board, 2),
           Tetris_Piece(screen, board, 3),
           Tetris_Piece(screen, board, 4),
           Tetris_Piece(screen, board, 5),
           Tetris_Piece(screen, board, 6)
        ]
    shuffle(bag)
    return bag