from settings import *
from button import Button

class Menu:
    def __init__(self, app):
        pg.init()
        self.app = app  
        self.font = pg.font.SysFont("arialblack", 40)
        self.color = (255,255,255)
        self.start = False
        self.winner = ""

        self.resume = Button("Start", WIDTH/2, 400)

    def draw_text(self, text, x, y, size=40, font_fam="arialblack", text_col=(255, 255, 255), center_x=True):
        font = pg.font.SysFont(font_fam, size)
        img = font.render(text, True, text_col)
        if center_x:
            x = x - img.get_width() // 2 
        self.app.screen.blit(img, (x, y))

    def run(self):
        mouse_pos = pg.mouse.get_pos()
        self.app.screen.fill((0,0,0))

        self.draw_text(self.winner, WIDTH/2, 100)
        self.draw_text("multiplayer racing game", WIDTH/2, 200)
        self.resume.update(self.app.screen)

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.resume.check_for_input(mouse_pos):
                    self.app.game_state = 'start'
                    # self.app.server.connect_to_server()
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.app.game_state = ''

        pg.display.update()



