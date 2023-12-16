import time

import pygame
import sys
from pygame.math import Vector2
import random


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('resources/head_up_30.png').convert_alpha()
        self.head_down = pygame.image.load('resources/head_down_30.png').convert_alpha()
        self.head_right = pygame.image.load('resources/head_right_30.png').convert_alpha()
        self.head_left = pygame.image.load('resources/head_left_30.png').convert_alpha()

        self.tail_up = pygame.image.load('resources/tail_up_30.png').convert_alpha()
        self.tail_down = pygame.image.load('resources/tail_down_30.png').convert_alpha()
        self.tail_right = pygame.image.load('resources/tail_right_30.png').convert_alpha()
        self.tail_left = pygame.image.load('resources/tail_left_30.png').convert_alpha()

        self.body_vertical = pygame.image.load('resources/body_vertical_30.png').convert_alpha()
        self.body_horizontal = pygame.image.load('resources/body_horizontal_30.png').convert_alpha()

        self.body_tr = pygame.image.load('resources/body_topright_30.png').convert_alpha()
        self.body_tl = pygame.image.load('resources/body_topleft_30.png').convert_alpha()
        self.body_br = pygame.image.load('resources/body_bottomright_30.png').convert_alpha()
        self.body_bl = pygame.image.load('resources/body_bottomleft_30.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for idx, block in enumerate(self.body):
            x_pos = int(block.x) * cell_size
            y_pos = int(block.y) * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if idx == 0:
                screen.blit(self.head, block_rect)
            elif idx == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[idx + 1] - block
                next_block = self.body[idx - 1] - block
                if previous_block.x == next_block.x:
                    # vertical block
                    screen.blit(self.body_vertical, block_rect)
                if previous_block.y == next_block.y:
                    # horizontal block
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    if (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    if (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    if (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        if head_relation == Vector2(-1, 0):
            self.head = self.head_right
        if head_relation == Vector2(0, 1):
            self.head = self.head_up
        if head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        if tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        if tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        if tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
class Fruit:
    def __init__(self, snake_body):
        self.randomize(snake_body)
        self.apple = pygame.image.load('resources/apple_30.png').convert_alpha()
    def draw_fruit(self):
        x_pos = int(self.pos.x) * cell_size
        y_pos = int(self.pos.y) * cell_size
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        screen.blit(self.apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self, snake_body):
        occupied = False
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            for block in snake_body:
                if x == block.x and y == block.y:
                    occupied = True
                    break

            self.x = x
            self.y = y

            if occupied is not True:
                break

        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.Snake = Snake()
        self.Fruit = Fruit(self.Snake.body)

    def update(self):
        self.Snake.move_snake()
        self.check_collision()
        self.check_fail()
    def draw_elements(self):
        self.draw_grass()
        self.Snake.draw_snake()
        self.Fruit.draw_fruit()

    def check_collision(self):
        if self.Fruit.pos == self.Snake.body[0]:
            self.Fruit.randomize(self.Snake.body)
            self.Snake.add_block()

    def check_fail(self):
        if (not 0 <= self.Snake.body[0].x < cell_number) or (not 0 <= self.Snake.body[0].y < cell_number):
            self.game_over()

        for block in self.Snake.body[1:]:
            if block == self.Snake.body[0]:
                self.game_over()
    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)


if __name__ == "__main__":
    pygame.init()

    # Creates a "fake" grid
    cell_size = 30
    cell_number = 20
    screen_x_y = cell_size * cell_number
    screen = pygame.display.set_mode((screen_x_y, screen_x_y))

    clock = pygame.time.Clock() # Object that control FPS

    Main_game = Main()

    # Creating an userevent and setting it's timing
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    moved_from_last_press = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                Main_game.update()
                moved_from_last_press = True
            if event.type == pygame.KEYDOWN:
                if moved_from_last_press:
                    if event.key == pygame.K_UP:
                        if Main_game.Snake.direction.y != 1:
                            Main_game.Snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if Main_game.Snake.direction.y != -1:
                            Main_game.Snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_RIGHT:
                        if Main_game.Snake.direction.x != -1:
                            Main_game.Snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_LEFT:
                        if Main_game.Snake.direction.x != 1:
                            Main_game.Snake.direction = Vector2(-1, 0)
                    moved_from_last_press = False



        screen.fill((175, 215, 70))
        Main_game.draw_elements()
        pygame.display.update()
        # clock.tick(60)