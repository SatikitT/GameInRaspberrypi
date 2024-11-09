from settings import *
from button import Button

class Menu:
    def __init__(self, app):
        pg.init()
        self.app = app  
        self.font = pg.font.SysFont("arialblack", 40)
        self.color = (255,255,255)
        self.start = False

    def draw_text(self, text, x, y, size=40, font_fam="arialblack", text_col=(255, 255, 255), center_x=True):
        font = pg.font.SysFont(font_fam, size)
        img = font.render(text, True, text_col)
        if center_x:
            x = x - img.get_width() // 2 
        self.app.screen.blit(img, (x, y))

    def run(self):

        resume = Button("Start", WIDTH/2, 400)

        while not self.start:
            mouse_pos = pg.mouse.get_pos()
            self.app.screen.fill((0,0,0))

            self.draw_text("multiplayer racing game", WIDTH/2, 200)
            resume.update(self.app.screen)

            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if resume.check_for_input(mouse_pos):
                        self.start = True
                        self.app.server.connect_to_server()
                if event.type == pg.QUIT:
                    pg.quit()

            pg.display.update()



