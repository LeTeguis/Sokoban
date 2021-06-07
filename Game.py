import pygame
import Interface
import LoadData

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def init(self):
        self.game_width = 1000
        self.game_height = 700
        self.screen = pygame.display.set_mode((self.game_width, self.game_height)) # , pygame.FULLSCREEN
        pygame.display.set_caption("Sokoban")
        self.game_running = True

        self.menu_principale = Interface.MenuPrincipal(self)
        self.menu_choix_level = Interface.LevelChoix(self)
        self.menu_cajouter_level = Interface.Menu_Level_Add(self)
        self.menu_credit = Interface.Menu_Credit(self)
        self.state = self.menu_principale
        self.state.play_sound = True
        self.state_not_error = True

    def load_screen(self):
        opacity = 0
        sens = True
        count_anim = 0
        image = pygame.image.load("datas/logo_gap.png").convert_alpha()

        x_position = (self.game_width - image.get_rect().width)/2
        y_position = (self.game_height - image.get_rect().height)/2

        self.font = pygame.font.SysFont("Showcard Gothic", 50)
        self.slogan = self.font.render("dream, school, game", True, (255, 255, 255))
        self.slogan1 = self.font.render("reinvent yourself", True, (255, 255, 255))

        x_position_slogan = (self.game_width - self.slogan.get_rect().width) / 2
        y_position_slogan = y_position + image.get_rect().height + 20

        x_position_slogan1 = (self.game_width - self.slogan1.get_rect().width) / 2
        y_position_slogan1 = y_position_slogan + self.slogan.get_rect().height + 5

        slogan_listen = True

        while slogan_listen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    slogan_listen = False

            if opacity >= 255 and sens == True:
                sens = False

            if opacity <= 0 and sens == False:
                sens = True
                count_anim += 1

            if count_anim == 5:
                break

            if sens == True:
                opacity += 2
            else:
                opacity -= 2

            image.set_alpha(opacity)

            texture, validate = LoadData.loadData.get_texture("mario-550x365")
            if validate:
                texture = pygame.transform.scale(texture, (self.game_width, self.game_height))
                self.screen.blit(texture, (0, 0))
            else:
                self.screen.fill((51, 153, 218))
            self.screen.blit(image, (x_position, y_position))
            self.screen.blit(self.slogan, (x_position_slogan, y_position_slogan))
            self.screen.blit(self.slogan1, (x_position_slogan1, y_position_slogan1))
            pygame.display.flip()

    def loop(self):
        while self.game_running:
            self.event()
            self.update()
            texture, validate = LoadData.loadData.get_texture("mario-550x365")
            if validate:
                texture = pygame.transform.scale(texture, (self.game_width, self.game_height))
                self.screen.blit(texture, (0, 0))
            else:
                self.screen.fill((51, 153, 218))
            self.draw()
            pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            if self.state_not_error:
                self.state.updateEvent(event)

    def draw(self):
        if self.state_not_error:
            self.state.draw(self.screen)

    def update(self):
        if self.state_not_error:
            self.state.update(0)

    def close(self):
        pygame.quit()