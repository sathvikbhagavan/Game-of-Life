import pygame
import numpy as np

WIDTH = 500
HEIGHT = 600
SIZE = 10
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 40
pygame.init()
grid = np.zeros((WIDTH // SIZE, WIDTH // SIZE))
n_grid = np.zeros((WIDTH // SIZE, WIDTH // SIZE))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')
colors = {0: '#7E7E7E', 1: 'yellow'}
screen.fill(pygame.Color('#7E7E7E'))
for i in range(WIDTH // SIZE):
    pygame.draw.line(screen, pygame.Color('#999999'), (0, i * SIZE), (WIDTH, i * SIZE))
for i in range(HEIGHT // SIZE):
    pygame.draw.line(screen, pygame.Color('#999999'), (i * SIZE, 0), (i * SIZE, WIDTH))
pygame.draw.line(screen, pygame.Color('#999999'), (0, WIDTH), (WIDTH, WIDTH))
pygame.display.update()


# Button Class
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_pressed(self, position):
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False


# Calculates number of neighbors for a particular cell
def number_of_neighbors(x, y):
    rows = grid.shape[0]
    cols = grid.shape[1]
    n = 0
    if x - 1 >= 0:
        n += grid[x-1, y]
        if y - 1 >= 0:
            n += grid[x-1, y-1]
        if y + 1 < cols:
            n += grid[x-1, y+1]
    if x + 1 < rows:
        n += grid[x+1, y]
        if y - 1 >= 0:
            n += grid[x+1, y-1]
        if y + 1 < cols:
            n += grid[x+1, y+1]
    if y - 1 >= 0:
        n += grid[x, y-1]
    if y + 1 < cols:
        n += grid[x, y+1]
    return n


# Update each cell as per the rules (number of neighbors)
def calculate():
    global grid
    change = False
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            n = number_of_neighbors(x, y)
            n_grid[x, y] = n
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == 1:
                if n_grid[x, y] < 2 or n_grid[x, y] >= 4:
                    grid[x, y] = 0
                    change = True
            else:
                if n_grid[x, y] == 3:
                    grid[x, y] = 1
                    change = True
    return not change


# Draw the grid
def draw():
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            pygame.draw.rect(screen, pygame.Color(colors[grid[x, y]]), (y * SIZE + 1, x * SIZE + 1,
                                                                        SIZE - 1, SIZE - 1))
    pygame.display.update()


start_button = Button(pygame.Color('blue'), WIDTH//4-BUTTON_WIDTH, WIDTH + 2*SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, 'START')
start_button.draw(screen)
pause_button = Button(pygame.Color('blue'), WIDTH//2-BUTTON_WIDTH//2, WIDTH + 2*SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, 'PAUSE')
pause_button.draw(screen)
end_button = Button(pygame.Color('blue'), 3*WIDTH//4, WIDTH + 2*SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, 'END')
end_button.draw(screen)
pygame.display.update()

run = True
start = False
not_change = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x_pos = pos[0] // 10
            y_pos = pos[1] // 10
            if 0 <= x_pos < grid.shape[0] and 0 <= y_pos < grid.shape[1] and not start:
                grid[y_pos, x_pos] = 1 - grid[y_pos, x_pos]
                draw()
            elif start_button.is_pressed(pos):
                start = True
            elif pause_button.is_pressed(pos):
                start = False
            elif end_button.is_pressed(pos):
                run = False
    if start:
        not_change = calculate()
        draw()
        pygame.time.delay(100)
        if not_change:
            print('[INFO] Simulation is over')
            not_change = False
            start = False
