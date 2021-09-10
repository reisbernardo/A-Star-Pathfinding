import pygame

# Used colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Defines Node class
class Node:
    def __init__(self, row, col, width, total_rows): # Node constructor
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self): # Get node position
        return self.row, self.col

    def is_closed(self): # Check if node is closed
        return self.color == RED

    def is_open(self):  # Check if node is open
        return self.color == GREEN

    def is_barrier(self): # Check if node is barrier
        return self.color == BLACK

    def is_start(self): # Check if node is start
        return self.color == ORANGE

    def is_end(self): # Check if node is end
        return self.color == TURQUOISE

    def is_path(self): # Check if node is path
        return self.color == PURPLE

    def reset(self): # Resets node
        self.color = WHITE

    def make_start(self): # Make node the start
        self.color = ORANGE

    def make_closed(self): # Closes node
        self.color = RED

    def make_open(self): # Open node to calculation
        self.color = GREEN
    
    def make_barrier(self): # Make node a barrier
        self.color = BLACK

    def make_end(self): # Make node the end
        self.color = TURQUOISE

    def make_path(self): # Make node the path
        self.color = PURPLE

    def draw(self, win): # Draw node
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid): # Check current node neighbors
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():# down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():# right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col - 1])