# CURRENT TEST : Get current piece
import pyautogui
from PIL import Image
from enum import Enum
import math

class tetromino(Enum):
    I = (74, 163, 180, 255)
    O = (174, 162, 51, 255)
    T = (112, 39, 135, 255)
    S = (69, 137, 72, 255)
    Z = (128, 42, 37, 255)
    L = (134, 89, 28, 255)
    J = (49, 89, 136, 255)

def euclidean_distance(color1, color2):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def find_closest_color(target_color, tolerance=75):
    closest_piece = None
    min_distance = float('inf')
    
    for piece in tetromino:
        distance = euclidean_distance(piece.value, target_color)
        if distance < min_distance:
            min_distance = distance
            closest_piece = piece
    
    if min_distance <= tolerance:
        return closest_piece.name
    else:
        return 'Unknown'

board = [['' for _ in range(10)] for _ in range(20)]
hold = ''
queue = []

WIDTH = 260
HEIGHT = 525

cell_width = WIDTH // 10
cell_height = HEIGHT // 20

first = True 

#store board state in an array
with Image.open('board_state.png') as board_state:
    for row in range(20):
        y = (cell_height * row) + cell_height//2
        for col in range(10):
            x = (cell_width * col) + cell_width//2
            colour = board_state.getpixel((x,y))
            if colour != (0,0,0,255):
                board[row][col] = 1
                if first == True:
                    current_piece = find_closest_color(board_state.getpixel((x,y+5)))
                    first = False
            else: 
                board[row][col] = 0

print(current_piece)


