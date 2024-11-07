from settings import *

class Button:
    def __init__(self, text, x, y, size= 40, font_fam= "arialblack", text_color = (255,255,255)):
        self.pos_x = x
        self.pos_y = y
        self.size = size
        self.font = pg.font.SysFont(font_fam, size)
        self.text = self.font.render(text, True, text_color)
        self.rect = self.text.get_rect(center=(self.pos_x, self.pos_y))

    def update(self, screen):
        screen.blit(self.text, self.rect)

    def check_for_input(self, position):
        if (position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)):
            return True
        return False