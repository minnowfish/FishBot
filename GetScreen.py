import pyautogui
from PIL import Image
from enum import Enum
import math

#width and height of the tetris board
WIDTH = 260
HEIGHT = 525

#colors of each tetris piece
class tetromino(Enum):
    I = (74, 163, 180, 255)
    O = (174, 162, 51, 255)
    T = (112, 39, 135, 255)
    S = (69, 137, 72, 255)
    Z = (128, 42, 37, 255)
    L = (134, 89, 28, 255)
    J = (49, 89, 136, 255)

#initalise variables/arrays
board = [['' for _ in range(10)] for _ in range(20)]
hold = ''
queue = []
first = True
current_piece = ''

def capture_screenshot():
    #get the screenshot of the current state of the game
    screenshot = pyautogui.screenshot(region=(425, 190, 630, HEIGHT))
    screenshot.save('Image/screenshot.png')

    #get tetris board
    board_state = screenshot.crop((180, 0, 440, 525))
    board_state.save('Image/board_state.png')

    #get queue and hold piece
    hold_image = screenshot.crop((60, 104, 61, 105))
    hold_image.save('Image/hold.png')

    queue1 = screenshot.crop((575, 74, 576, 137))
    queue1.save('Image/queue1.png')
    queue2 = screenshot.crop((575, 137, 576, 200))
    queue2.save('Image/queue2.png')
    queue3 = screenshot.crop((575, 200, 576, 263))
    queue3.save('Image/queue3.png')


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
    
def get_queue_piece(ImgPath):
    with Image.open(ImgPath) as Img:
        for y in range(63):
            if Img.getpixel((0,y)) != (36,36,36,255):
                colour = Img.getpixel((0, y + 10))
                return(find_closest_color(colour))
                break

def analyze_board(WIDTH, HEIGHT, first, hold, current_piece):
    global queue
    cell_width = WIDTH // 10
    cell_height = HEIGHT // 20
    new_queue = []

    #identify hold piece and store in a variable
    with Image.open('Image/hold.png') as hold_image:
        colour = hold_image.getpixel((0,0))
        new_hold = find_closest_color(colour)

    #identify pieces in the queue
    new_queue.append(get_queue_piece('Image/queue1.png'))
    new_queue.append(get_queue_piece('Image/queue2.png'))
    new_queue.append(get_queue_piece('Image/queue3.png'))

    if first == False:
        if new_queue != queue:
            current_piece = queue[0]
        elif new_hold != hold and hold != "Unknown":
            current_piece = hold
        else:
            current_piece = current_piece
    
    queue = new_queue

    #store board state in an array and get current piece
    with Image.open('Image/board_state.png') as board_state:
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

    return new_hold, current_piece, first

while True:
    screenshot = capture_screenshot()

    hold , current_piece, first= analyze_board(WIDTH, HEIGHT, first, hold, current_piece)

    #to be removed
    for i in range(20):
        for j in range(10):
            if board[i][j] == 0:
                print("  ", end = "")
            else:
                print("[]", end = "")
        print("")

    print(f"\nhold piece : {hold}")
    print(f"queue : {queue}")
    print(f"current piece : {current_piece}")