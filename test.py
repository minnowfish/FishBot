# CURRENT TEST : Getting queue 
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

#(550, 74, 591, 263)
with Image.open('screenshot.png') as screenshot:
    queue1 = screenshot.crop((575, 74, 576, 137))
    queue1.save('Image/queue1.png')
    queue2 = screenshot.crop((575, 137, 576, 200))
    queue2.save('Image/queue2.png')
    queue3 = screenshot.crop((575, 200, 576, 263))
    queue3.save('Image/queue3.png')

def test(ImgPath):
    with Image.open(ImgPath) as Img:
        for y in range(63):
            if Img.getpixel((0,y)) != (36,36,36,255):
                colour = Img.getpixel((0, y + 10))
                return(find_closest_color(colour))
                break

queue = []
queue.append(test('Image/queue1.png'))
queue.append(test('Image/queue2.png'))
queue.append(test('Image/queue3.png'))

print(queue)




