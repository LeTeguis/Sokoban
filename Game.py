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


        #self.background_sound = pygame.mixer.music.load("datas/audios/African Safari Loop.wav")
        #self.background_sound = pygame.mixer.music.load("datas/audios/Blazer Rail 2.wav")
        #self.background_sound = pygame.mixer.music.load("datas/audios/Free Synthwave Loop.wav")
        #pygame.mixer.music.play(-1)
    def loop(self):
        while self.game_running:
            self.event()
            self.update()
            texture, validate = LoadData.loadData.get_texture("mario-550x365")
            if validate:
                texture = pygame.transform.scale(texture, (1000, 700))
                self.screen.blit(texture, (0, 0))
            else:
                self.screen.fill((51, 153, 218))
            self.draw()
            pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            #event = pygame.event.poll()
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