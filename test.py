# CURRENT TEST : Getting queue 
import pyautogui
from PIL import Image
from enum import Enum

Queue_Size = 3

class tetromino(Enum):
    I = (74, 163, 180, 255)
    O = (174, 162, 51, 255)
    T = (112, 39, 135, 255)
    S = (69, 137, 72, 255)
    Z = (128, 42, 37, 255)
    L = (134, 89, 28, 255)
    J = (49, 89, 136, 255)

with Image.open('screenshot.png') as screenshot:
    queue_image = screenshot.crop((550, 77, 591, 263))
    queue_image.save('queue.png')

with Image.open('queue.png') as queue_image:
    x = 20 
    rootname = 'test'
    for i in range(3):
        y = (62*i) + 35
        filename = 'test'  + str(i+1) + ".png"

        thisImage = queue_image.crop((x, y, x+1, y+1))
        thisImage.save(filename)
