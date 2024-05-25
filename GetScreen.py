import pyautogui
from PIL import Image
from enum import Enum

#width and height of the tetris board
WIDTH = 260
HEIGHT = 525

#colors of each tetris piece
class tetromino(Enum):
    I = ()
    O = ()
    T = ()
    S = ()
    Z = ()
    L = ()
    J = (49, 89, 136, 255)

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

def analyze_board(screenshot, WIDTH, HEIGHT):
    cell_width = WIDTH // 10
    cell_height = HEIGHT // 20

    for row in range(20):
        y = (cell_height * row) + cell_height//2
        for col in range(10):
            x = (cell_width * col) + cell_width//2
            colour = screenshot.getpixel((x,y))
            if colour != (0,0,0,255):
                board[row][col] = 1
            else: 
                board[row][col] = 0


#initalise 2D array to hold the tetris board
board = [['' for _ in range(10)] for _ in range(20)]

screenshot = capture_screenshot()

analyze_board(Image.open('board_state.png'), WIDTH, HEIGHT)

for i in range(20):
    for j in range(10):
        if board[i][j] == 0:
            print("  ", end = "")
        else:
            print("[]", end = "")
    print("")