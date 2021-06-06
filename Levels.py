import pygame
import Player
import LoadData
import GameLogics
import numpy as np
import Interface

class Level():
    def __init__(self, path_level, finish, lvn, tln):
        self.path = path_level
        self.name = "default"
        self.level_name = "default"
        self.ligne = 0
        self.colone = 0
        self.tileset = {}
        self.map = np.zeros(shape=(self.ligne, self.colone))
        self.map_error = False
        self.is_finish = finish
        self.level_number = lvn
        self.level_all = tln
        self.parent = None
        self.sol_name = None

        self.play_sound = False

    def load_level(self):
        fichier = open(self.path, "r")
        ligne_map = 0
        self.map_error = False
        self.indice_sol = -1
        while True:
            ligne = fichier.readline()
            if ligne != "":
                infos = ligne.split(" ")
                if self.seof(infos[0]) == "name":
                    self.name = self.seof(infos[1])
                    self.level_name = self.seof(infos[1])
                elif self.seof(infos[0]) == "lh":
                    self.ligne, self.colone = int(self.seof(infos[1])), int(self.seof(infos[2]))
                    self.map = np.zeros(shape=(self.ligne, self.colone))
                elif self.seof(infos[0]) == "pp":
                    x, y = int(self.seof(infos[1])), int(self.seof(infos[2]))
                    action, player_pack = self.seof(infos[3]), self.seof(infos[4])
                    self.player = Player.Player(x, y, player_pack, action)
                elif self.seof(infos[0]) == "ttn":
                    if self.seof(infos[1]) not in self.tileset:
                        self.tileset[self.seof(infos[1])] = {}
                    value = self.tileset[self.seof(infos[1])]
                    value[self.seof(infos[2])] = self.seof(infos[3])

                    if self.seof(infos[1]) == "sol":
                        self.indice_sol = self.seof(infos[3])
                        self.sol_name = self.seof(infos[2])

                elif self.seof(infos[0]) == "lg":
                    if len(infos) - 1 == self.colone:
                        for i in range(len(infos) - 1):
                            self.map[ligne_map, i] = int(self.seof(infos[i + 1]))
                        ligne_map += 1
                    else:
                        self.map_error = True
                elif ligne != "\n":
                    self.map_error = True
            else:
                break

        if ligne_map != self.ligne:
            self.map_error = True
        else:
            if self.ligne == 0 or self.colone == 0:
                self.map_error = True
            else:
                w, h = 1000, 700
                d1 = (h - 120) // self.ligne
                d2 = (w - 100) // self.colone

                if d1 < d2:
                    self.dimension = d1
                else:
                    self.dimension = d2

                if 64 < self.dimension:
                    self.dimension = 64
                if self.dimension < 32:
                    self.dimension = 32

                self.x_deplacement = (w - self.dimension * self.colone - 100) / 2 + 50
                self.y_deplacement = (h - self.dimension * self.ligne - 100) / 2 + 100

                self.player.resize(self.dimension)

                self.last_time = pygame.time.get_ticks()
                self.validate = False
                self.xmove = 0
                self.ymove = 0

                self.x_mapUpdate = 0
                self.y_mapUpdate = 0

                self.precedent = Interface.Bouton("PRECEDENT", ftSize=20, x=20, y=20)
                self.precedent.set_size(150, 30, bd=4, bdr=10)

                self.home = Interface.Bouton("HOME", ftSize=20, x=200, y=20)
                self.home.set_size(150, 30, bd=4, bdr=10)

                self.undo = Interface.Bouton("undo", ftSize=20, x=20, y=60)
                self.undo.set_size(150, 30, bd=4, bdr=10)
                self.undo.deseable()

                self.redo = Interface.Bouton("redo", ftSize=20, x=200, y=60)
                self.redo.set_size(150, 30, bd=4, bdr=10)
                self.redo.deseable()

                self.actual_modif = -1
                self.liste_map_accumulation = []
                self.liste_player_position = []

                self.liste_map_accumulation.append(self.map.copy())
                self.liste_player_position.append([self.player.position_x, self.player.position_y])
                self.actual_modif = 0
                self.number_back_game = 15

                fini = "PAS FINI"
                if self.is_finish:
                    fini = "FINI"
                self.infos_level = "Level (" + fini + ") : " + str(self.level_number) + " / " + str(self.level_all)
                self.font = pygame.font.SysFont("Showcard Gothic", 30)
                self.titre_image = self.font.render(self.infos_level, True, (255, 142, 43))

                self.info_bulle = NextStape(self.parent, self.level_number, self)
                self.info_bulle.visible = False
                self.info_bulle.set_position((1000 - self.info_bulle.rect.width) // 2, (700 - self.info_bulle.rect.height) // 2)

                self.load_sound()
        fichier.close()
    def seof(self, string):
        return ((string).split("\n"))[0]

    def is_win(self):
        return GameLogics.gameLogics.is_finish(lg = self.ligne, cl = self.colone, map = self.map, nature=self.tileset)

    def load_sound(self, click = 'datas/audios/mixkit-medieval-show-fanfare-announcement-226.wav'):
        self.sound_click = pygame.mixer.Sound(click)
        self.sound_walk = pygame.mixer.Sound('datas/audios/mixkit-boxing-punch-2051.wav')
        self.sound_hit = pygame.mixer.Sound('datas/audios/mixkit-boxer-getting-hit-2055.wav')
        self.sound_complited = pygame.mixer.Sound('datas/audios/mixkit-unlock-new-item-game-notification-254.wav')
        self.sound_complited_out = pygame.mixer.Sound('datas/audios/220208__gameaudio__click-pop-two-part.wav')
        self.play_it = False

    def updateEvent(self, event):
        game_running = True

        if not self.map_error:
            if self.info_bulle.visible == False:
                if self.play_sound:
                    self.background_sound = pygame.mixer.music.load(
                        "datas/audios/ES_Glitching Through the Sky - William Benckert.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    self.play_sound = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                    if self.player.isIdle() and self.xmove == 0 and self.ymove == 0:
                            if event.key == pygame.K_UP:
                                self.ymove = -1
                            elif event.key == pygame.K_DOWN:
                                self.ymove = 1
                            elif event.key == pygame.K_LEFT:
                                self.xmove = -1
                            elif event.key == pygame.K_RIGHT:
                                self.xmove = 1
                            else:
                                pass
                self.precedent.updateEvent(event)
                self.home.updateEvent(event)

                self.undo.updateEvent(event)
                self.redo.updateEvent(event)

                if self.undo.is_click():
                    self.actual_modif -= 1
                    if self.actual_modif < 0:
                        self.actual_modif = 0
                    else:
                        self.redo.enable()
                        self.map = (self.liste_map_accumulation[self.actual_modif]).copy()
                        p = self.liste_player_position[self.actual_modif]
                        self.player.setPosition(p[0], p[1])
                        if self.actual_modif == 0:
                            self.undo.deseable()

                if self.redo.is_click():
                    self.actual_modif += 1
                    if self.actual_modif >= len(self.liste_player_position):
                        self.actual_modif = len(self.liste_player_position) - 1
                    else:
                        self.undo.enable()
                        self.map = (self.liste_map_accumulation[self.actual_modif]).copy()
                        p = self.liste_player_position[self.actual_modif]
                        self.player.setPosition(p[0], p[1])
                        if self.actual_modif == len(self.liste_player_position) - 1:
                            self.redo.deseable()

                if self.precedent.is_click() and not (self.parent is None):
                    self.parent.state = self.parent.menu_choix_level
                    self.precedent.state = self.precedent.normal_file
                    self.parent.state.play_sound = True
                if self.home.is_click() and not (self.parent is None):
                    self.parent.state = self.parent.menu_principale
                    self.parent.state.play_sound = True
                    self.home.state = self.home.normal_file
            else:
                self.info_bulle.updateEvent(event)
        return game_running

    def update(self, delta_time):
        if not self.map_error:
            if self.player.isIdle() and (self.xmove != 0 or self.ymove != 0) and self.validate == False:
                self.player.direction_Change(self.xmove, self.ymove)
                xp, yp = self.player.position_x, self.player.position_y
                if self.xmove != 0:
                    self.ymove = 0
                elif self.ymove != 0:
                    self.xmove = 0
                self.n, self.n2, self.validate = GameLogics.gameLogics.logics_game(xp, yp, self.xmove, self.ymove, self.ligne, self.colone, self.map, self.indice_sol)
                if self.validate:
                    if GameLogics.gameLogics.put_end_point:
                        GameLogics.gameLogics.put_end_point = False
                        self.sound_complited.play()
                    if GameLogics.gameLogics.out_end_point:
                        GameLogics.gameLogics.out_end_point = False
                        self.sound_complited_out.play()
                    if self.xmove != 0:
                        self.player.set_move(self.xmove, 0)
                        self.ymove = 0
                    elif self.ymove != 0:
                        self.player.set_move(0, self.ymove)
                        self.xmove = 0
                    self.x_mapUpdate = int(self.player.position_x)
                    self.y_mapUpdate = int(self.player.position_y)
                    self.sound_walk.play()
                else:
                    self.xmove, self.ymove = 0, 0
                    self.sound_hit.play()
            now = pygame.time.get_ticks()
            if now - self.last_time > 150:
                v2, f = self.player.animation()
                if self.validate and v2 and f == 0:
                    if self.n != -1:
                        if self.actual_modif != -1:
                            while True:
                                if self.actual_modif + 1 >= len(self.liste_player_position):
                                    break
                                print((self.actual_modif + 1)," : ", len(self.liste_player_position))
                                del self.liste_player_position[self.actual_modif + 1]
                                del self.liste_map_accumulation[self.actual_modif + 1]
                        self.map[int(self.y_mapUpdate + self.ymove), int(self.x_mapUpdate + self.xmove)] = self.n
                        if self.n2 != -1:
                            if int(self.y_mapUpdate + self.ymove * 2) >= 0 and int(self.y_mapUpdate + self.ymove * 2) < self.ligne:
                                if int(self.x_mapUpdate + self.xmove * 2) >= 0 and int(self.x_mapUpdate + self.xmove * 2) < self.colone:
                                    self.map[int(self.y_mapUpdate + self.ymove * 2), int(self.x_mapUpdate + self.xmove * 2)] = self.n2

                        self.liste_map_accumulation.append(self.map.copy())
                        self.liste_player_position.append([self.x_mapUpdate + self.xmove, self.y_mapUpdate + self.ymove])
                        self.actual_modif += 1
                        self.undo.enable()

                        if self.actual_modif > self.number_back_game:
                            self.actual_modif -= 1
                            self.liste_player_position.remove(self.liste_player_position[0])
                            self.liste_map_accumulation.remove(self.liste_map_accumulation[0])

                        #print(self.actual_modif)

                    self.xmove, self.ymove = 0, 0
                    self.validate = False
                self.last_time = now

    def draw(self, screen):
        if self.map_error == False:
            pygame.draw.rect(screen, color=(0, 100, 100, 0), rect=(0, 0, 1000, 100))
            for i in range(self.ligne):
                for j in range(self.colone):
                    if int(self.map[i, j]) != -1:
                        key, name, val = GameLogics.gameLogics.get_infos_value(int(self.map[i, j]))
                        if val:
                            texture, validate = LoadData.loadData.get_texture(name)
                            if validate:
                                texture1, validate1 = LoadData.loadData.get_texture(self.sol_name)
                                if validate1:
                                    self.blit(screen, texture1, i, j)
                                self.blit(screen, texture, i, j)
            self.player.draw(screen, self.x_deplacement, self.y_deplacement)
            self.precedent.draw(screen)
            self.home.draw(screen)
            self.undo.draw(screen)
            self.redo.draw(screen)
            screen.blit(self.titre_image, ((1000 - self.titre_image.get_rect().width)  - 20, (100 - self.titre_image.get_rect().height)/2))

            if self.is_win():
                self.is_finish = True
                levels.saved_loader(self.level_name, True)
                levels.init_loader()
                self.parent.menu_choix_level.got_page(self.parent.menu_choix_level.actual_page)
                if self.player.isIdle():
                    self.info_bulle.visible = True
                    if self.play_it == False:
                        self.sound_click.play()
                        self.play_it = True

                        self.info_bulle.stop_sound = self.sound_click

            if self.info_bulle.visible:
                self.info_bulle.draw_rect_alpha(screen, (0, 0, 0, 100), pygame.Rect(0, 0, 1000, 700))
                self.info_bulle.draw(screen)

    def blit(self, screen, texture, i, j):
        if not self.map_error:
            texture = pygame.transform.scale(texture, (self.dimension, self.dimension))
            x = j * self.dimension + self.x_deplacement
            y = i * self.dimension + self.y_deplacement
            screen.blit(texture, (x, y))

class NextStape():
    def __init__(self, parent, num_level, this_level):
        self.rect = pygame.Rect(0, 0, 400, 200)
        self.next = Interface.Bouton("SUIVANT", ftSize=18)
        self.recommencer = Interface.Bouton("REJOUER", ftSize=18)
        self.home = Interface.Bouton("HOME", ftSize=18)
        self.message = "BRAVOS"

        self.visible = False
        self.parent = parent
        self.this_level = this_level

        self.num_level = num_level

        self.space = 5
        w = (self.rect.width - self.space*4) // 3
        self.recommencer.set_size(w, w // 2, 2, 6)
        self.home.set_size(w, w // 2, 2, 6)
        self.next.set_size(w, w // 2, 2, 6)

        self.set_position(0, 0)

        self.set_message("BRAVOS")

        self.stop_sound = None

        lv = self.num_level - 1
        self.next_level, validate = levels.get_next_level2(lv)
        if validate:
            self.next_level.parent = self.parent
            self.next_level.load_level()
            if self.next_level.map_error:
                self.next.deseable()
        else:
            self.next.deseable()

    def set_message(self, string):
        self.message = str(string)
        self.font = pygame.font.SysFont("Showcard Gothic", 70)
        self.message_image = self.font.render(self.message, True, (255, 255, 255))

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.recommencer.set_position(x + self.space, y + self.rect.height - self.recommencer.rect.height - self.space)
        self.home.set_position(self.recommencer.rect.x + self.home.rect.width + self.space, self.recommencer.rect.y)
        self.next.set_position(self.home.rect.x + self.home.rect.width + self.space, self.recommencer.rect.y)

    def draw_rect_alpha(self, surface, color, rect, epaisseur = 0):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        if epaisseur == 0:
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        else:
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), width=epaisseur)
        surface.blit(shape_surf, rect)

    def draw(self, screen):
        if self.visible:
            self.draw_rect_alpha(screen, (220, 220, 220, 125), self.rect)
            self.draw_rect_alpha(screen, (150, 150, 150, 150), self.rect, 2)
            screen.blit(self.message_image, (self.rect.x + (self.rect.width - self.message_image.get_rect().width)//2,
                                             self.rect.y + (self.rect.height - self.home.rect.height - self.message_image.get_rect().height)//2))
            self.next.draw(screen)
            self.recommencer.draw(screen)
            self.home.draw(screen)

    def update(self, delta_time):
        if self.visible:
            pass

    def updateEvent(self, event):
        if self.visible:
            self.next.updateEvent(event)
            self.recommencer.updateEvent(event)
            self.home.updateEvent(event)

            if self.home.is_click():
                self.parent.menu_choix_level.got_page(self.parent.menu_choix_level.actual_page)
                self.parent.state = self.parent.menu_principale
                self.home.state = self.home.normal_file
                self.visible = False

                if self.stop_sound != None:
                    self.stop_sound.stop()
            if self.next.is_click():
                self.visible = False
                self.parent.menu_choix_level.got_page(self.parent.menu_choix_level.actual_page)
                self.parent.state = self.next_level
                self.next.state = self.next.normal_file

                if self.stop_sound != None:
                    self.stop_sound.stop()

            if self.recommencer.is_click():
                self.parent.menu_choix_level.got_page(self.parent.menu_choix_level.actual_page)
                self.visible = False
                p = self.parent
                self.this_level.parent = p
                self.this_level.load_level()
                self.recommencer.state = self.recommencer.normal_file

                if self.stop_sound != None:
                    self.stop_sound.stop()

class Levels():
    def __init__(self):
        self.path, self.not_error = LoadData.loadData.get_level_path(0)
        self.levels = {}
        self.actual = 0
        self.init_loader()

    def init_loader(self):
        if self.not_error:
            fichier = open(self.path, "r")
            while True:
                ligne = fichier.readline()
                if ligne != "":
                    infos = ligne.split(" ")
                    identifiant = [self.seof(infos[1])]
                    if str.upper(self.seof(infos[2])) == "FALSE":
                        identifiant.append(False)
                    elif str.upper(self.seof(infos[2])) == "TRUE":
                        identifiant.append(True)
                    else:
                        identifiant.append(False)
                    self.levels[self.seof(infos[0])] = identifiant
                else:
                    break
            fichier.close()

    def saved_loader(self, name, finish):
        if self.not_error:
            if name in self.levels.keys():
                (self.levels[name])[1] = finish
                fichier = open(self.path, "w")
                for element in self.levels.keys():
                    validation = "True"
                    if (self.levels[element])[1] == False:
                        validation = "False"
                    fichier.write(element+" "+(self.levels[element])[0]+" "+validation+"\n")
                fichier.close()
            else:
                pass

    def seof(self, string):
        return ((string).split("\n"))[0]

    def get_level_by_name(self, name):
        if name in self.levels:
            self.actual = 0
            for i in self.levels.keys():
                if i != name:
                    self.actual += 1
                else:
                    break
            identifiant = self.levels[name]
            return Level(identifiant[0], identifiant[1], self.actual + 1, len(self.levels)), True
        return "Erreur", False

    def get_level_by_position(self, position):
        if position < 0:
            return "Erreur", False
        i = 0
        for k in self.levels.keys():
            if i == position:
                self.actual = position
                return self.get_level_by_name(k)
            i += 1
        return "Erreur", False

    def get_next_level(self):
        self.actual += 1
        if self.actual >= len(self.levels):
            self.actual = 0
        return self.get_level_by_position(self.actual)

    def get_next_level2(self, indice):
        if indice + 1 >= len(self.levels):
            return "Erreur", False
        return self.get_level_by_position(indice + 1)

    def get_previous_level(self):
        self.actual -= 1
        if 0 > self.actual:
            self.actual = 0

        return self.get_level_by_position(self.actual)

    def get_size(self):
        return len(self.levels)

levels = Levels()