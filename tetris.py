# Name: Jack Shao
# File Name: tetris.py
# Description: a tetris python game

import pygame
import random


# CLASS DEFINITION


class piece:
    """Class that stores all the information about a particular piece."""

    def __init__(self, column, row, shape_type):
        self.x = column
        self.y = row
        self.shape_type = shape_type
        self.color = colorsList[shapesList.index(shape_type)]
        self.rotation = 0  # described by 0-3


# FUNCTION DEFINITIONS


def draw_text_middle(text, size, color, surface):
    """Function that draws text in the middle of the screen."""
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (playTopLeftX + playWidth / 2 - label.get_width() / 2,
                         playTopLeftY + playHeight / 2 - label.get_height() / 2))


def draw_window(surface):
    """Function that draws the main window of the game."""
    surface.fill(black)  # black background

    # draw title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, white)
    surface.blit(label, (playTopLeftX + playWidth / 2 - label.get_width() / 2, 30))

    # draw all pieces in grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (playTopLeftX + j * blockSize, playTopLeftY + i * blockSize, blockSize, blockSize), 0)

    # draw grid
    for i in range(20):
        # horizontal lines
        pygame.draw.line(surface, grey, (playTopLeftX, playTopLeftY + i * blockSize),
                         (playTopLeftX + playWidth, playTopLeftY + i * 30))
        for j in range(10):
            # vertical lines
            pygame.draw.line(surface, grey, (playTopLeftX + j * blockSize, playTopLeftY),
                             (playTopLeftX + j * blockSize, playTopLeftY + playHeight))

    # draw border
    pygame.draw.rect(surface, red, (playTopLeftX, playTopLeftY, playWidth, playHeight), 5)


def start_menu():
    """Function that initializes the start screen and calls the main game loop."""
    run = True
    while run:
        screen.fill(black)
        draw_text_middle('Press any key to begin.', 60, white, screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()


def create_grid(locked_positions=None):
    """Function that updates current game grid by checking locked_positions."""
    if locked_positions is None:
        locked_positions = {}

    current_grid = [[black for i in range(10)] for i in range(20)]

    for i in range(len(current_grid)):  # iterate in y direction
        for j in range(len(current_grid[i])):  # iterate in x direction
            if (j, i) in locked_positions:
                temp = locked_positions[(j, i)]
                current_grid[i][j] = temp

    return current_grid


def get_shape():
    """Function that chooses a random shape from the list and creates a new `piece` object."""
    return piece(5, 0, random.choice(shapesList))


def get_shape_positions(shape):
    """Function that gets the screen coordinates of every square of a specific piece."""
    positions = []
    shape_format = shape.shape_type[shape.rotation % len(shape.shape_type)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def is_valid_space(shape):
    """Function that checks if a specific piece is in a valid space."""
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == black] for i in range(20)]
    accepted_positions = [j for temp in accepted_positions for j in temp]
    positions = get_shape_positions(shape)

    for pos in positions:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def clear_row(locked_positions):
    """Function to check if any row is able to be cleared.
    If yes, delete the row(s), and shift everything above down."""
    empty_row_count = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if black not in row:
            empty_row_count += 1
            lowest_row = i
            for j in range(len(row)):
                del locked_positions[(j, i)]

    if empty_row_count > 0:
        for key in sorted(list(locked_positions), key=lambda a: a[1])[::-1]:
            # get the coordinates for all locked positions
            x, y = key
            if y < lowest_row:
                new_key = (x, y + empty_row_count)  # shift coordinates down
                locked_positions[new_key] = locked_positions.pop(key)  # assign values to locked_positions


def main():
    """The main game loop."""
    # create empty current positions
    global grid
    locked_positions = {}

    # initialize game variables
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.27
    score = 0

    while run:

        # UPDATING GAME STATE

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 4:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not is_valid_space(current_piece) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # CHECKING USER INPUT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not is_valid_space(current_piece):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not is_valid_space(current_piece):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate piece clockwise
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape_type)
                    if not is_valid_space(current_piece):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape_type)
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not is_valid_space(current_piece):
                        current_piece.y -= 1

        # add current piece to the grid
        shape_positions = get_shape_positions(current_piece)
        for i in range(len(shape_positions)):
            x, y = shape_positions[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # current piece has landed
        if change_piece:
            for position in shape_positions:
                # add current piece to locked positions
                coordinates = (position[0], position[1])
                locked_positions[coordinates] = current_piece.color

            # get next piece
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # check if row can be cleared 4 times
            for i in range(3):
                if clear_row(locked_positions):
                    score += 10

        draw_window(screen)
        pygame.display.update()

    draw_text_middle('You Lost :(', 40, white, screen)
    pygame.display.update()
    pygame.time.delay(2000)


# initialize used variables
screenWidth = 800
screenHeight = 700
# the tetris play area is 10x20 square blocks
playWidth = 300
playHeight = 600
blockSize = 30  # 300 / 10 = 30 and 600 / 20 = 30, defines block width and height
# the screen coordinates of the top left of the play area
playTopLeftX = (screenWidth - playWidth) // 2
playTopLeftY = screenHeight - playHeight
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
brightBlue = (0, 255, 255)
orange = (255, 165, 0)
purple = (128, 0, 128)
black = (0, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
grid = []  # global grid variable

# define shapes and their rotations
S_shape = [['.....',
            '.....',
            '..00.',
            '.00..',
            '.....'],
           ['.....',
            '..0..',
            '..00.'
            '...0.',
            '.....']]

Z_shape = [['.....',
            '.....',
            '.00..',
            '..00.',
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '.0...',
            '.....']]

I_shape = [['..0..',
            '..0..',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '0000.',
            '.....',
            '.....',
            '.....']]

O_shape = [['.....',
            '.00..',
            '.00..',
            '.....',
            '.....']]

J_shape = [['.....',
            '.0...',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..00.',
            '..0..',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '...0.',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '.00..',
            '.....']]

L_shape = [['.....',
            '...0.',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..0..',
            '..00.',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '.0...',
            '.....'],
           ['.....',
            '.00..',
            '..0..',
            '..0..',
            '.....']]

T_shape = [['.....',
            '..0..',
            '.000.',
            '.....',
            '.....'],
           ['.....',
            '..0..',
            '..00.',
            '..0..',
            '.....'],
           ['.....',
            '.....',
            '.000.',
            '..0..'
            '.....'],
           ['.....',
            '..0..',
            '.00..',
            '..0..',
            '.....']]

# make lists of shapes and their respective colors (same index)
shapesList = [S_shape, Z_shape, I_shape, O_shape, J_shape, L_shape, T_shape]
colorsList = [green, red, brightBlue, yellow, orange, blue, purple]

# initialize pygame modules and main screen
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Tetris')

start_menu()
