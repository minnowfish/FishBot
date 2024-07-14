import pygame
from math import floor
from pygame.event import Event
from Tetris.define import Controls
from Tetris.board import Board
from Tetris.blocks import generate_new_bag


class Game:
    def __init__(self, app, screen):
        self.screen = screen
        self.gravity = 0.02
        self.drop_timer = 0
        self.app = app
        self.DAS = 4
        self.gameover = False
        
        #screen
        self.board = Board(self.screen, x=140, y=20)

        #generate queue and current piece 
        self.bag = generate_new_bag(self.screen, self.board)
        self.queue = [self.get_queue() for _ in range(4)]
        self.current_piece = self.get_next()
        self.hold_piece = None

        #DAS and Key press
        self.last_movement = pygame.time.get_ticks()

        self.left_pressed = False
        self.left_pressed_tick = 0

        self.right_pressed = False
        self.right_pressed_tick = 0

        self.soft_drop = False
        self.piece_held = False

    def draw(self):
        self.board.draw()
        self.board.draw_piece(self.current_piece)
        self.board.draw_hold(self.hold_piece)
        self.board.draw_queue(self.queue)

    def update(self, events):
        if self.gameover == True:
            return False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == Controls.hold:
                    self.hold()
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

                #locking
        if self.current_piece.locked:
            if not self.board.add_piece(self.current_piece, self.queue[0]):
                self.gameover = True
                return
            self.current_piece = self.get_next()
            self.board.clear_lines()
            self.last_movement = pygame.time.get_ticks()
            self.piece_held = False

        if self.left_pressed:
            self.right_pressed_tick = 0
            if self.left_pressed_tick > self.DAS:
                while self.current_piece.move_left():
                     self.last_movement = pygame.time.get_ticks()
            elif self.left_pressed_tick == 0:
                if self.current_piece.move_left():
                    self.last_movement = pygame.time.get_ticks()
            self.left_pressed_tick += 1

        if self.right_pressed:
            self.left_pressed_tick = 0
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
    
    def hold(self):
        if self.piece_held == False:
            if self.hold_piece == None:
                self.hold_piece = self.current_piece
                self.current_piece = self.get_next()
            else:
                self.current_piece, self.hold_piece = self.hold_piece, self.current_piece
            self.hold_piece.reset()
            self.piece_held = True