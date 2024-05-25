import pyautogui
from PIL import Image
from enum import Enum

#width and height of the tetris board
WIDTH = 260
HEIGHT = 525

#colors of each tetris piece
class tetromino(Enum):
    I = (74, 163, 180, 255)
    O = (138, 131, 53, 255)
    T = (112, 39, 135, 255)
    S = (69, 137, 72, 255)
    Z = (128, 42, 37, 255)
    L = (134, 106, 47, 255)
    J = (49, 89, 136, 255)

#initalise variables/arrays
board = [['' for _ in range(10)] for _ in range(20)]
hold = ''
queue = []

def capture_screenshot():
    #get the screenshot of the current state of the game
    screenshot = pyautogui.screenshot(region=(425, 190, 630, HEIGHT))
    screenshot.save('screenshot.png')

    #get tetris board
    board_state = screenshot.crop((180, 0, 440, 525))
    board_state.save('board_state.png')

    #get queue and hold piece
    hold_image = screenshot.crop((60, 104, 61, 105))
    hold_image.save('hold.png')

def analyze_board(WIDTH, HEIGHT):
    cell_width = WIDTH // 10
    cell_height = HEIGHT // 20

    #store board state in an array
    with Image.open('board_state.png') as board_state:
        for row in range(20):
            y = (cell_height * row) + cell_height//2
            for col in range(10):
                x = (cell_width * col) + cell_width//2
                colour = board_state.getpixel((x,y))
                if colour != (0,0,0,255):
                    board[row][col] = 1
                else: 
                    board[row][col] = 0
    
    #identify hold piece and store in a variable
    with Image.open('hold.png') as hold_image:
        colour = hold_image.getpixel((0,0))
        hold = tetromino(colour).name
    return hold

#screenshot = capture_screenshot()

hold = analyze_board(WIDTH, HEIGHT)

#to be removed
for i in range(20):
    for j in range(10):
        if board[i][j] == 0:
            print("  ", end = "")
        else:
            print("[]", end = "")
    print("")

print(f"\nhold piece : {hold}")