import pygame

SQ_SIZE = 50
ROWS = COLS = 8
WIDTH, HEIGHT = COLS * SQ_SIZE, (ROWS + 1) * SQ_SIZE
FPS = 15

WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
GREY = pygame.Color('dark green')
BLUE = pygame.Color('blue')

LOGINS = {hash("Bhargava"):"Chess", hash("Guest"):"Guest"}