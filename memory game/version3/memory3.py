
import os
from uagame import Window
import pygame
from pygame import QUIT
from pygame import image, MOUSEBUTTONDOWN
import random
import datetime
import time


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
        self.window.set_font_size(100)
        self.pause_time = 0.15 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
      
        self.grid_size = (rows, columns)
        self.images = self.get_images()
        self.grid = self.create_grid()
        self.start_time = datetime.datetime.now()
        self.timer = datetime.timedelta()
        self.clicked = None
        self.recover = []

    def get_images(self):
        # load the images in to memory
        images = []
        # get the absolute path of the image files
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

        default_image = image.load(path + prefix + str(0) + suffix)
        
        images = [default_image] + images
        return images

    def create_grid(self):
        # create a grid of tiles given numbers of row and column
        Tile.set_window(self.window)
        Tile.set_default_image(self.images[0])
        grid = []
        for row_index in range(self.grid_size[0]):
            row = self.create_row(row_index)
            grid.append(row)
        return grid
    
    def create_row(self, row_index):
        # create a row of tiles
        # row_index is the index of the row this function is 
        #           creating, it's used to calculate the index of image
        row = []
        for column_index in range(self.grid_size[1]):
            # set the image and position of a tile
            img_index = row_index*self.grid_size[1] + column_index + 1
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
        if event.type == MOUSEBUTTONDOWN and self.continue_game is True:
            self.handle_mouseup(event)
    
    def handle_mouseup(self, event):
        # handle a click event performed by the player
        for row in self.grid:
            for tile in row:
                if tile.select(event.pos):
                    if self.clicked is None:
                        self.clicked = tile
                    else:
                        if self.clicked != tile:
                            self.recover.append(self.clicked)
                            self.recover.append(tile)
                        self.clicked = None

    def draw(self):
    # Draw all game objects.
    # - self is the Game to draw
        self.window.clear()
        # draw every tile
        for row in self.grid:
            for tile in row:
                tile.draw()
        
        self.draw_timer()
        self.window.update()
      
    def draw_timer(self):
        string = str(self.timer.seconds)
        self.window.draw_string(string, 
            self.window.get_width() - self.window.get_string_width(string), 0)

    def update(self):
    # Update the game objects.
    # - self is the Game to update
        self.timer = datetime.datetime.now() - self.start_time
        for tile in self.recover:
            tile.recover()
            #time.sleep(0.5)
        self.recover = []
    def decide_continue(self):
    # Check and remember if the game should continue
    # - self is the Game to check
        self.continue_game = False
        for row in self.grid:
            for tile in row:
                if not tile.is_exposed:
                    self.continue_game = True

class Tile:
    # class attributes
    window = None
    br_color = pygame.Color('black')
    br_width = 4
    default_image = None
    
    def __init__(self, x, y, image):
        # initialize the tile object
        # x, y are int, indicating the position of the tile
        # image is the image the tile has
        self.position = (x, y)
        self.image = image
        self.is_exposed = False
        size = self.image.get_size()
        self.rect = pygame.rect.Rect(self.position, size)
    
    def draw(self):
        # draw the tile
        surface = self.window.get_surface()
        if self.is_exposed:
            surface.blit(self.image, self.position)
        else:
            surface.blit(Tile.default_image, self.position)
        pygame.draw.rect(surface, self.br_color, self.rect, self.br_width)
    
    def select(self, position):
        # handle the click action
        # position passed is event.pos, indicaing the osition of the click
        if self.rect.collidepoint(position):
            if not self.is_exposed:
                self.is_exposed = True
                return True
        return False
    
    def recover(self):
        self.is_exposed = False
    
    def __eq__(self, other):
        if self.image == other.image:
            return True
        else:
            return False

    # set the class attributes
    @classmethod
    def set_window(cls, window):
        cls.window = window
    @classmethod
    def set_default_image(cls, image):
        cls.default_image = image

if __name__ == '__main__':
     main()
