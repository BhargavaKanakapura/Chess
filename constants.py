import pygame

SQ_SIZE = 50
ROWS = COLS = 8
WIDTH, ACT_WIDTH, HEIGHT = (COLS) * SQ_SIZE, int((COLS + 2.5) * SQ_SIZE), (ROWS + 1) * SQ_SIZE
FPS = 15

WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
GREY = pygame.Color('dark green')
BLUE = pygame.Color('blue')

LOGINS = {hash("Bhargava"):"Chess", hash("Guest"):"Guest"}

LEVEL = -1

STDOUT = []

def PRINT(value):

    if type(value) in [str, int]:
        STDOUT.append(value)
        print(value)

    elif type(value) in [list, set]:
        STDOUT.append(value)
        for item in value:
            print(item)