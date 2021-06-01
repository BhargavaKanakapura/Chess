from constants import *
import pygame

class InvalidLogin(Exception):
    def __init__(self, uop):
        self.message = "INVALID LOGIN --> " + uop.upper() + " IVALID"
        super().__init__(self.message)

class InvalidInput(Exception):
    def __init__(self, text_field):
        self.message = "INVALID INPUT FOR " + text_field
        super().__init__(self.message)

def valid_login(username, password):

    username = hash(username)

    try:
        if LOGINS[username] == password: return True
        else: raise InvalidLogin("PASSWORD")

    except KeyError:
        raise InvalidLogin("USERNAME")


class MoveLog:

    def __init__(self, surf):

        self.line = 1
        self.new_page = False

        self.c_x, self.c_y = WIDTH + SQ_SIZE // 10, 10
        self.txt_size = 13

        self.padding = 4

        self.surf = surf

    def write_line(self, line, next_line=True):
        
        font = pygame.font.Font('freesansbold.ttf', self.txt_size)
        text_img = font.render(str(self.line) + ". " + line, False, WHITE)

        if next_line:
            self.break_line()

        return text_img, (self.c_x, self.c_y)

    def break_line(self):
        
        self.line += 1
        self.c_y += self.txt_size + self.padding

        if self.line == 10:
            self.scroll()

    def scroll(self):

        self.line = 0
        self.scroll = False
        self.c_x, self.c_y = WIDTH + SQ_SIZE // 10, 10


