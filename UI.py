import pygame

pygame.font.init()

class Text:

    def __init__(self, text, pos, color, size, display):
        self.text = text
        self.pos = pos
        self.color = color
        self.size = size
        self.display = display

    def render_text(self):       
        font_name = pygame.font.SysFont('freesansbold.ttf', self.size)
        text_surf = font_name.render(self.text, False, self.color)
        self.display.blit(text_surf, self.pos)

    def change_text(self, new_text):
        self.text = new_text
        self.render_text()

class Button:

    def __init__(self, text_object, color, pos, on_click):
        pass