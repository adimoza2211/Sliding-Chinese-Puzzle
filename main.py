'''''''''
~MATHS KLOTSKI PUZZLE~
Bonus Project

Made By
Aditya Moza - 2022035
Aditya Prasad -  2022036
Pranav Bharadwaj - 2022363

'''''''''

import pygame
import random
from pygame import mixer
from classes import *
from settings import *

#initialising mixer for musik
mixer.init()
mixer.music.load("a.mp3")
mixer.music.play(loops=-1)

class Game:
    def __init__(self):
        #intiliase pygame 
        pygame.init()
        #sets screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #sets title
        pygame.display.set_caption(title)
        # Used for shuffling
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        #bool value to check if shuffle has started 
        self.start_shuffle = False
        #used in shuffle
        self.previous_choice = ""
        #bool used to quit the application 
        self.start_game = False

    # Initializes grid
    def create_game(self):
        #fills a 2D array with numbers form 1 to gamesize**2 - 1
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        #array of strings containing possible moves
        possible_moves = []
        #iterating over tiles
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
#throughout the program we are using "empty" to denote space in the grid
                if tile.text == "empty":
                    #checking functions
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break
        #if we have already moved in that direction once, we remove it from the list of possible moves
        #this prevents tiles going back and forth between the same spaces
        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves   
        #chooosing random moves
        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    # Creates tiles with numbers (Stored as a 2D list)
    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    # Creates empty tile
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        #whenever we call the class tile in sprites.py,we will pass the game into the 
        self.all_sprites = pygame.sprite.Group()
        #storing the grid in the the titles_grid varibale from create_game function
        self.tiles_grid = self.create_game()#this grid will change when we try to solve the puzzle by moving shit around
        #this is the solved grid, we compare with this to check if the game is finished
        self.tiles_grid_completed = self.create_game()
        # self.draw_tiles()#draw tiles executed
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        # Place shuffle and Reset Buttons
        self.buttons_list.append(Button(700, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(700, 170, 200, 50, "Reset", WHITE, BLACK))
        self.draw_tiles()#draw tiles executed

    # Keeps the grid visible and starts the game
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # called after every move and displays new grid
    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True
        self.all_sprites.update()
        
    def draw_grid(self):
        #draws a line after every row of tiles
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        #draws a line after every col of tiles
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))
    
    #draw function creates pixels on the main "screen surface"
    # Rewrites all the sprites over and over again when it is called by update
    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()#draw grid executed
        for button in self.buttons_list:
            button.draw(self.screen)
        pygame.display.flip()#This will update the contents of the entire display.

    
    def events(self):
    #pygame.event returns a list of possible events(as defined in module)
    #quit even occurs when we press X on top right in the window
        for event in pygame.event.get():
            #checks if we click the X button on the window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            #making the game react to mouseclicks using mbtd
            #.right,.left are defined for individual tiles in sprite.py
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()
#giving buttons functionality
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                            
#initialising a game object                            
game = Game()
while True:
    game.new()
    game.run()