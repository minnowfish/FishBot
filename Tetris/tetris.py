import sys
import pygame as pygame
from Tetris.game import Game

class Tetris:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 900
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width , self.screen_height))
        self.running = True
        self.start_game()

    def run(self):
        while True: 
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.running != False:
                self.running = self.game.update(events)

            self.screen.fill("black")
            self.game.draw()
            pygame.display.flip()

            self.clock.tick(120)

    def start_game(self):
        self.game =  Game(self, self.screen)

if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()