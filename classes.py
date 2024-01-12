import pygame
from settings import *
pygame.font.init()

# Creates tile UI
class Tile(pygame.sprite.Sprite):
    def __init__(self,game,x,y,text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.x,self.y = x,y
        self.text = text
        self.rect = self.image.get_rect()
        # add colour and text of number on tile 
        # add bg colour to tile if there is no number on it
        if self.text != "empty":
            self.font = pygame.font.SysFont("Geneva", 50)
            font_surface = self.font.render(self.text, True, WHITE)
            self.image.fill(LOTUS)
            self.font_size = self.font.size(self.text)
            # defining variables to shift the numbers from corners to center of tiles
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(DARKBLUE)
            
    def update(self):
        # Multiplying x and y with tilesize provides exact size/coordinates of tile in pixels
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    
    # pass coordinates of mouse pointer
    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
        # returns true if mouse is within boundaries of tile

    # functions to check if tile is inside the grid
    # moving offset is TILESIZE, and the tile is inside the grid if offset is lesser than (number of tiles in a row * TILESIZE)
    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE
    
    def left(self):
        # tile is at the left edge if value of (self.rect.x - TILESIZE) is 0
        return self.rect.x - TILESIZE >= 0

    def up(self):
        # tile is at the top edge if value of (self.rect.x - TILESIZE) is 0
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE

# mainly used to text elements to the game
class UIElement:
    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text
        
    def draw(self,screen):
        font = pygame.font.SysFont("Geneva",30)
        text = font.render(self.text,True,WHITE)
        screen.blit(text,(self.x,self.y))

class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text
        
    def draw(self, screen):
        # place button on screen
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Geneva", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        
        # Set position of text within the button
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
