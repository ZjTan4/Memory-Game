
import os
from uagame import Window
import pygame
from pygame import QUIT
from pygame import image, MOUSEBUTTONDOWN
import random
import time
from time import clock


def main():
    window = Window('Memory', 500, 400)
    
    game = Game(window)
    game.play()

    window.close()


class Game:
# An object in this class represents a complete game.

    def __init__(self, window, rows = 4, columns = 4):
    # Initialize a Game.
    # - self is the Game to initialize
    # - window is the uagame window object
      
        self.window = window
        self.pause_time = 0.04 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
      
        self.grid_size = (rows, columns)
        self.images = self.get_images()
        self.grid = self.create_grid()

    def get_images(self):
        images = []
        prefix = 'image'
        suffix = '.bmp'
        path = os.path.dirname(__file__) + '\\images\\'
        image_num = (self.grid_size[0]*self.grid_size[1])//2
        for index in range(1, image_num + 1):
            filename = path + prefix + str(index) + suffix
            img = image.load(filename)
            images.append(img)
            images.append(img)
        random.shuffle(images)
        return images

    def create_grid(self):
        Tile.set_window(self.window)
        grid = []
        for row_index in range(self.grid_size[0]):
            row = self.create_row(row_index)
            grid.append(row)
        return grid
    
    def create_row(self, row_index):
        row = []
        for column_index in range(self.grid_size[1]):
            img_index = row_index*self.grid_size[1] + column_index
            image = self.images[img_index]
            height = image.get_height()
            width = image.get_width()
            x = width*column_index
            y = height*row_index

            tile = Tile(x, y, image)
            
            row.append(tile)
        return row

    
    def play(self):
    # Play the game until the player presses the close box.
    # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
        # play frame
            self.handle_event()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time) # set game velocity by pausing

    def handle_event(self):
        # handle the event produced by the player input
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == MOUSEBUTTONDOWN:
            pass

    def draw(self):
    # Draw all game objects.
    # - self is the Game to draw
        self.window.clear()
        # draw every tile
        for row in self.grid:
            for tile in row:
                tile.draw()
        
        
        self.window.update()
      
      
    def update(self):
    # Update the game objects.
    # - self is the Game to update
        pass
         
    def decide_continue(self):
    # Check and remember if the game should continue
    # - self is the Game to check
        pass

class Tile:
    # class attributes
    window = None
    br_color = pygame.Color('black')
    br_width = 4
    
    def __init__(self, x, y, image):
        # x, y are integers, indicating the coordinate of the tile
        self.position = (x, y)
        self.image = image
    
    def draw(self):
        surface = self.window.get_surface()
        surface.blit(self.image, self.position)
        size = self.image.get_size()
        rectangle = pygame.rect.Rect(self.position, size)
        pygame.draw.rect(surface, self.br_color, rectangle, self.br_width)

    @classmethod
    def set_window(cls, window):
        cls.window = window

main()


