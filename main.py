import pyautogui
from PIL import Image

hold = Image.open('hold.png')
print(hold.getpixel((0,0)))

