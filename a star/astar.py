"""
A* Path Finding Algorithm Visualization Module

This module provides a visualization tool for the A* path-finding algorithm using Pygame. 
It defines a Spot class representing nodes in the grid and includes functions for creating 
the grid, drawing nodes, and implementing the A* algorithm.

Functions:
---------
h(p1, p2):
    Calculate the Manhattan distance heuristic between two points.

reconstruct_path(came_from, current, draw):
    Reconstruct the shortest path and mark the nodes that belong to the path.

algorithm(draw, grid, start, end):
    The A* path-finding algorithm implementation.

make_grid(rows, width):
    Create a 2D grid of Spot instances based on the number of rows and the width of the window.

draw_grid(win, rows, width):
    Draw grid lines on the visualization window.

draw(win, grid, rows, width):
    Draw the current state of the grid and nodes on the visualization window.

get_clicked_pos(pos, rows, width):
    Get the row and column of the clicked node based on the mouse position.

main(win, width):
    The main function to run the A* path-finding visualization.

Credits:
--------
This code is written by Ellinor Sætre. 
You can find the original repository at [https://www.youtube.com/watch?v=JtiK0DOeI4A].
"""
from queue import PriorityQueue
import pygame
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')

# Defining colors for making the path-finding window RBG color code. 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Define a class to build the visualization tool. To keep track of the nodes. 
# This class will track different values:
# where it is (columns position), width, neighbours, and the color of the nodes 
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # Have we already looked at you? What would it mean that it is already looked at?
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col +1])

        if self.col > 0 and not grid[self.row][self.col -1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])
        
    
    def __lt__(self, other):
        return False
    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() # Heap sort algorithm
    open_set.put((0, count, start))
    came_from = {} # To keep track of the path

    # keeps track of the current shortest distance to get from the start node to this node
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0 # initialise the g_score

    # keeps track of the predicted distance shortest distance to the end node. Assumtion of start-end distance
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) # initialise the f_score

    open_set_hash = {start} # help us see if there is something in the open_set

    # If we dont find a path yet, the path doesn't exist:
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the game if there is no open_set

        current = open_set.get()[2]
        open_set_hash.remove(current)

        # if we find the end in the path:
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True # make path

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] +  1 # use 'random.randint(1,3)' instead of '1' to test other pathfinding
            # If we find a better path than the path before, update the path
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour)) # put in the new neighbour
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()
    
    return False
        

def make_grid(rows, width):
    grid = []
    gap = width // rows
    # Making a 2D list
    for i in range(rows): # this will be rows
        grid.append([])
        for j in range(rows): # this will be columns
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot) # A list inside a list that all store spots
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Fills the frame with with the color WHITE
def draw(win, grid, rows, width):
    win.fill(WHITE) # Not the most efficient, but is fine for this purpose
    for row in grid:
        for spot in row:
            spot.draw(win)
    # Draw the gridlines on top of the WHITE
    draw_grid(win, rows, width)
    pygame.display.update() # Take whatever we have drawn and update the display

# Find the position of the mouse to decide what cube you are clicking inside
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            # (1) Cheking if the quit-button i pressed
            if event.type == pygame.QUIT:
                run = False
        
            # Once we start the algorithm the user should only be able to press the quit botton
            if started:
                continue

            # Check the mouse status
            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                                             
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                   
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)
