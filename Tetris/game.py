import pygame
from math import floor
from pygame.event import Event
from define import Controls
from board import Board
from blocks import generate_new_bag


class Game:
    def __init__(self, app, screen):
        self.screen = screen
        self.gravity = 0.02
        self.drop_timer = 0
        self.app = app
        self.DAS = 4
        
        #screen
        self.board = Board(self.screen, x=140, y=20)

        #generate queue and current piece 
        self.bag = generate_new_bag(self.screen, self.board)
        self.queue = [self.get_queue() for _ in range(4)]
        self.current_piece = self.get_next()

        #DAS and Key press
        self.last_movement = pygame.time.get_ticks()

        self.left_pressed = False
        self.left_pressed_tick = 0

        self.right_pressed = False
        self.right_pressed_tick = 0

        self.soft_drop = False

    def draw(self):
        self.board.draw()
        self.board.draw_piece(self.current_piece)

    def update(self, events):
        for event in events:
            # TODO : define the functions for each event 
            if event.type == pygame.KEYDOWN:
                if event.key == Controls.hold:
                    pass
                elif event.key == Controls.rotate_cw:
                    self.rotate_cw()
                elif event.key == Controls.rotate_ccw:
                    self.rotate_ccw()
                elif event.key == Controls.hard_drop:
                    self.current_piece.hard_drop()
                elif event.key == Controls.soft_drop:
                    self.soft_drop = True
                elif event.key == Controls.move_left:
                    self.left_pressed_tick = 0
                    self.left_pressed = True
                elif event.key == Controls.move_right:
                    self.right_pressed_tick = 0
                    self.right_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == Controls.move_left:
                    self.left_pressed = False
                elif event.key == Controls.move_right:
                    self.right_pressed = False
                elif event.key == Controls.soft_drop:
                    self.soft_drop = False

        if self.left_pressed:
            if self.left_pressed_tick > self.DAS:
                while self.current_piece.move_left():
                     self.last_movement = pygame.time.get_ticks()
            elif self.left_pressed_tick == 0:
                if self.current_piece.move_left():
                    self.last_movement = pygame.time.get_ticks()
            self.left_pressed_tick += 1

        if self.right_pressed:
            if self.right_pressed_tick > self.DAS:
                while self.current_piece.move_right():
                     self.last_movement = pygame.time.get_ticks()
            elif self.right_pressed_tick == 0:
                if self.current_piece.move_right():
                    self.last_movement = pygame.time.get_ticks()
            self.right_pressed_tick += 1

        if self.soft_drop:
            self.drop_timer += self.gravity * 40
        else:
            self.drop_timer += self.gravity

        #locking
        if self.current_piece.locked:
            self.board.add_piece(self.current_piece)
            self.current_piece = self.get_next()
            self.board.clear_lines()
            self.last_movement = pygame.time.get_ticks()


        #gravity
        if self.drop_timer >= 1:
            gravity_floor = floor(self.drop_timer)
            self.drop_timer -= gravity_floor
            for i in range(gravity_floor):
                if self.current_piece.move_down():
                    self.last_movement = pygame.time.get_ticks()
                    
    def rotate_cw(self):
        if self.current_piece.rotate_cw():
            self.last_movement = pygame.time.get_ticks
    
    def rotate_ccw(self):
        if self.current_piece.rotate_ccw():
            self.last_movement = pygame.time.get_ticks

    def get_queue(self):
        next = self.bag.pop(0)
        if len(self.bag) == 0:
            self.bag = generate_new_bag(self.screen, self.board)
        return next
    
    def get_next(self):
        self.queue.append(self.get_queue())
        return self.queue.pop(0)



