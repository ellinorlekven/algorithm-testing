import pygame
import math
from queue import PriorityQueue

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
        self.color == PURPLE 

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        pass
    
    def __lt__(self, other):
        return False
    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

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


    pygame.quit()

main(WIN, WIDTH)

# 1st problem: getting a black screen because we never called the draw function
# Solution: at the top of the while loop we are gonna call draw(win, grid, ROWS, width)

# 2nd problem: We can press the start and the end pos in the same cell.
# Solution: added 'and spot != end' in line 152 'and spot != start' in line 155

# 3rd problem: use the right mouse button to delete barriers
# Solution: added code in line 162-169. (Partly copied from line 149-151)

# NOW: The visualisation of the app is good and we need to add the algorithm.
