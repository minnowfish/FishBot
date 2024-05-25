import pyautogui
from PIL import Image

with Image.open('hold.png') as hold_image:
    print(hold_image.getpixel((0,0)))

