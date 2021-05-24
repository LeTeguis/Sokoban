import pygame
from pygame.locals import *
import LoadData
import Levels
import numpy as np

class Bouton():
    def __init__(self, text = "Default", x = 0, y = 0, ftSize = 60):
        self.hover_file = (250, 192, 56)
        self.normal_file = (245, 174, 48)
        self.click_file = (227, 160, 47)
        self.grid_file = (91, 92, 94)
        self.state = self.normal_file
        self.text = text
        self.fontsize = ftSize
        #self.font = pygame.font.Font("datas/police/Game Played.otf", self.fontsize)
        self.font = pygame.font.SysFont("Showcard Gothic", self.fontsize)
        self.text_image = self.font.render(self.text, True, (255,255,255))
        self.rect = pygame.Rect(x, y, 350, 80)
        self.border = 6
        self.border_radius = 12

    def set_font_size(self, size):
        self.fontsize = size
        self.font = pygame.font.SysFont("Showcard Gothic", self.fontsize)
        self.text_image = self.font.render(self.text, True, (255, 255, 255))

    def set_text(self, texte):
        self.text = texte
        self.text_image = self.font.render(self.text, True, (255, 255, 255))

    def set_size(self, w, h, bd, bdr):
        self.rect.width = w
        self.rect.height = h
        self.border = bd
        self.border_radius = bdr

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_position(self):
        return self.rect.x, self.rect.y

    def draw(self, screen):
        pygame.draw.rect(screen, color = (192, 192, 194), rect=self.rect, width=self.border, border_radius=self.border_radius)
        rect = pygame.Rect(self.rect.x + self.border, self.rect.y + self.border, self.rect.width - self.border*2, self.rect.height - self.border*2)
        pygame.draw.rect(screen, color = self.state, rect=rect, border_radius=self.border_radius - self.border)
        x = self.rect.x + (self.rect.width - self.text_image.get_rect().w)/2
        y = self.rect.y + (self.rect.height - self.text_image.get_rect().h)/2
        screen.blit(self.text_image, (x, y))

    def updateEvent(self, event):
        if self.state != self.grid_file:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.is_enter(event.pos[0], event.pos[1]):
                        self.state = self.click_file
            elif event.type == MOUSEBUTTONUP:
                if self.state == self.click_file:
                    self.state = self.hover_file
            elif event.type == MOUSEMOTION:
                if self.is_enter(event.pos[0], event.pos[1]):
                    self.state = self.hover_file
                else:
                    self.state = self.normal_file


    def is_enter(self, x, y):
        if x < self.rect.x or x > self.rect.x + self.rect.width or y < self.rect.y or y > self.rect.y+self.rect.height:
            return False
        return True

    def is_hover(self):
        if self.state == self.hover_file:
            return True
        return False

    def is_click(self):
        if self.state == self.click_file:
            return True
        return False

    def is_normal(self):
        return not (self.is_hover() or self.is_click() or self.is_grid())

    def is_grid(self):
        if self.state == self.grid_file:
            return True
        return False

    def enable(self):
        self.state = self.normal_file

    def deseable(self):
        self.state = self.grid_file

class Selected_Bouton():
    def __init__(self, image):
        self.image_name = image
        self.size = pygame.Rect(0, 0, 32, 32)
        self.hover = (150, 150, 150)
        self.normal = (245, 174, 48)
        self.selected = (0, 0, 0)
        self.state = self.normal
        self.is_selected = False

    def draw(self, screen):
        if self.state != self.normal:
            rect = pygame.Rect(self.size.x - 2, self.size.y - 2, self.size.width + 3, self.size.height + 3)
            pygame.draw.rect(screen, self.state, rect=rect, width=2)
        texture, validate = LoadData.loadData.get_texture(self.image_name)
        if validate:
            texture = pygame.transform.scale(texture, (self.size.width, self.size.height))
            screen.blit(texture, (self.size.x, self.size.y))

    def set_position(self, x, y):
        self.size.x, self.size.y = x, y

    def set_size(self, w, h):
        self.size.width, self.size.height = w, h

    def is_enter(self, x, y):
        if x < self.size.x or x > self.size.x + self.size.width or y < self.size.y or y > self.size.y+self.size.height:
            return False
        return True

    def updateEvent(self, event):
        selection = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.is_enter(event.pos[0], event.pos[1]):
                    if self.is_selected:
                        self.state = self.normal
                        self.is_selected = False
                    else:
                        self.state = self.selected
                        self.is_selected = True
                        selection = True

        elif event.type == MOUSEMOTION:
            if self.is_enter(event.pos[0], event.pos[1]):
                self.state = self.hover
            else:
                if self.is_selected:
                    self.state = self.selected
                else:
                    self.state = self.normal

        return selection

    def item_is_selected(self):
        return self.is_selected

class Fleche_Bouton():
    def __init__(self):
        font_size = 12
        self.next = Bouton("N", ftSize=font_size)
        self.next.set_size(25, 25, 4, 8)
        self.precedent = Bouton("P", ftSize=font_size)
        self.precedent.set_size(25, 25, 4, 8)

        self.max_value = 900 // 16
        self.min_value = 900 // 64

        self.value = self.min_value
        self.font = pygame.font.SysFont("Showcard Gothic", font_size)
        self.value_image = self.font.render(str(int(self.value)), True, (220, 220, 220))

        self.size = pygame.Rect(0, 0, 100, 25)
        self.value_change = False

    def set_min_value(self, min):
        if self.max_value < min:
            return
        self.min_value = min
        if self.min_value > self.value:
            self.value = self.min_value

    def set_max_value(self, max):
        if self.min_value > max:
            return
        self.max_value = max
        if self.max_value < self.value:
            self.value = self.max_value

    def set_size(self, w, h):
        if w < self.value_image.get_rect().width + self.next.rect.width + self.precedent.rect.width:
            return
        if h < self.value_image.get_rect().height + self.next.rect.height + self.precedent.rect.height:
            return
        self.size.width, self.size.height = w, h
        self.next.set_size(self.size.height, self.size.height, 4, 8)
        self.precedent.set_size(self.size.height, self.size.height, 4, 8)


    def set_position(self, x, y):
        self.size.x, self.size.y = x, y
        self.next.set_position(x + self.size.width - self.next.rect.width, y)
        self.precedent.set_position(x, y)

    def get_position(self):
        return self.size.x, self.size.y

    def get_value(self):
        return int(self.value)

    def set_value(self, value):
        if self.max_value < value or self.min_value > value:
            return
        self.value = value
        self.value_image = self.font.render(str(int(self.value)), True, (220, 220, 220))

    def add_value(self, add):
        if self.max_value < self.value + add:
            return
        if self.min_value > self.value + add:
            return
        self.value += add
        self.value_image = self.font.render(str(int(self.value)), True, (220, 220, 220))

    def draw(self, screen):
        self.next.draw(screen)
        self.precedent.draw(screen)

        x = self.size.x + (self.size.width - self.value_image.get_rect().width)/2
        y = self.size.y + (self.size.height - self.value_image.get_rect().height)/2
        screen.blit(self.value_image, (x, y))

    def updateEvent(self, event):
        self.value_change = False
        self.next.updateEvent(event)
        self.precedent.updateEvent(event)

        if self.next.is_click():
            if self.value + 1 <= self.max_value:
                self.add_value(1)
                self.value_change = True

        if self.precedent.is_click():
            if self.value - 1 >= 0:
                self.add_value(-1)
                self.value_change = True

class Number_Selected():
    def __init__(self):
        pass

class Menu_Level_Add():
    def __init__(self, parent):
        self.parent = parent
        self.type = ["sol", "mur", "caisse", "caisse_ok", "endpoint", "joueur"]
        self.type_file = {}
        self.type_actuel = 0
        font_size = 12
        self.home = Bouton("HOME", ftSize=font_size)
        self.next_theme = Bouton(self.type[self.type_actuel+1], ftSize=font_size)
        self.previous_them = Bouton("NONE", ftSize=font_size)
        self.previous_them.deseable()
        self.save = Bouton("ENREGISTRER", ftSize=font_size)
        self.save.deseable()
        self.nouveau = Bouton("NOUVEAU", ftSize=font_size)
        self.nouveau.deseable()

        self.clear_map = Bouton("EFFACER", ftSize=font_size)

        self.largeur = Fleche_Bouton()
        self.hauteur = Fleche_Bouton()

        self.bouton_principal()

        self.font = pygame.font.SysFont("Showcard Gothic", font_size)
        self.type_image = self.font.render(self.type[self.type_actuel], True, (220, 220, 220))

        fichier = open("datas/levels/level_tiles_infos.lti", "r")
        while True:
            ligne = fichier.readline()
            if ligne != "":
                infos = ligne.split(" ")
                ajouter = False
                for i in range(len(self.type)):
                    if self.type[i] == self.seof(infos[0]):
                        ajouter = True
                        break

                if ajouter:
                    if not self.seof(infos[0]) in self.type_file:
                        self.type_file[self.seof(infos[0])] = []
                    liste = self.type_file[self.seof(infos[0])]
                    for i in range(len(infos) - 1):
                        bouton = Selected_Bouton(self.seof(infos[i + 1]))
                        liste.append(bouton)
                    #self.type_file[self.seof(infos[0])] = liste
            else:
                break

        self.update_type(False)
        self.selected_element_type = -1

        self.largeur_dessin = 900
        self.hauteur_dessin = 700-120

        self.largeur.set_max_value(self.largeur_dessin // 32)
        self.largeur.set_min_value(self.largeur_dessin // 64)
        self.largeur.set_value(self.largeur.min_value)
        self.dimenssion = self.largeur_dessin // self.largeur.min_value
        self.hauteur.set_max_value(self.hauteur_dessin // 32)
        self.hauteur.set_min_value(self.hauteur_dessin // 64)
        self.hauteur.set_value(self.hauteur_dessin//self.dimenssion)

        self.map = np.full(shape=(self.hauteur.get_value(),self.largeur.get_value()),fill_value=int(-1))

        self.x_hover, self.y_hover = -1, -1
        self.level_name = "level_"+str(Levels.levels.get_size() + 1)
        self.indice_sol = -1

        self.deja_enregistre = False

        self.caisse_erreur = False
        self.endpoint_erreur = False
        self.joueur_erreur = True

        self.message_erreur_caisse = "le nombre de caisse et le nombre de endpoint sont different"
        self.message_erreur_endpoint = "vous n'avez pas mis de endpoint"
        self.message_erreur_joueur = "vous n'avez pas ajouter de joueur"

        self.erreur_creation_image = self.font.render("", True, (220, 220, 220))

        self.x_player = -1
        self.y_player = -1
        self.choix_player = ""

        self.enregistrer = False

    def seof(self, string):
        return ((string).split("\n"))[0]

    def draw_rect_alpha(self, surface, color, rect, epaisseur = 0):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        if epaisseur == 0:
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        else:
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), width=epaisseur)
        surface.blit(shape_surf, rect)

    def bouton_principal(self):
        self.home.set_size(100, 25, bd=2, bdr=6)
        self.home.set_position(10, 5)
        self.next_theme.set_size(100, 25, bd=2, bdr=6)
        self.next_theme.set_position(10, self.home.rect.y + self.home.rect.height + 5)
        self.previous_them.set_size(100, 25, bd=2, bdr=6)
        self.previous_them.set_position(10, self.next_theme.rect.y + self.next_theme.rect.height + 5)

        self.save.set_size(100, 25, bd=2, bdr=6)
        self.save.set_position(10 + self.home.rect.x + self.home.rect.width, self.home.rect.y + self.home.rect.height + 5)
        self.nouveau.set_size(100, 25, bd=2, bdr=6)
        self.nouveau.set_position(self.save.rect.x, self.save.rect.y + self.save.rect.height + 5)

        self.largeur.set_size(100, 25)
        self.largeur.set_position(10 + self.save.rect.x + self.save.rect.width, 5)
        self.hauteur.set_size(100, 25)
        self.hauteur.set_position(self.largeur.size.x, self.largeur.size.y + self.largeur.size.height + 5)

        self.clear_map.set_size(100, 25, bd=2, bdr=6)
        self.clear_map.set_position(self.hauteur.size.x, self.hauteur.size.y + self.hauteur.size.height + 5)

    def update_type(self, next_or_previous):
        if next_or_previous == True:
            self.type_actuel += 1
        else:
            self.type_actuel -= 1

        if self.type_actuel >= len(self.type):
            self.type_actuel = len((self.type)) - 1
        if self.type_actuel < 0:
            self.type_actuel = 0

        if self.type_actuel >= 0 and self.type_actuel < len((self.type)):
            if self.type_actuel + 1 >= len((self.type)):
                self.next_theme.set_text("NONE")
                self.next_theme.deseable()
            else:
                self.next_theme.set_text(self.type[self.type_actuel+1])
                self.next_theme.enable()

            if self.type_actuel - 1 < 0:
                self.previous_them.set_text("NONE")
                self.previous_them.deseable()
            else:
                self.previous_them.set_text(self.type[self.type_actuel - 1])
                self.previous_them.enable()
            self.type_image = self.font.render(self.type[self.type_actuel], True, (220, 220, 220))

            liste = self.type_file[self.type[self.type_actuel]]
            dimension = 40
            space = 5
            ligne = 100 // (dimension + space)
            colone = (1000 - (self.save.rect.width*3 + 10*4))//(dimension + space)

            decalage = self.save.rect.width*3 + 10*4
            x, y = decalage, space
            for i in range(ligne):
                break_to = False
                for j in range(colone):
                    if i*colone + j >= len(liste):
                        break_to = True
                        break
                    liste[i * colone + j].set_size(dimension, dimension)
                    liste[i*colone + j].set_position(x, y)
                    #liste[i*colone + j].is_selected = False
                    x += dimension + space
                if break_to:
                    break
                y += space

    def value_of_element(self, type_actuel, selected_element_type):
        if type_actuel >= 0 and type_actuel < len(self.type):
            indice = 0
            for i in range(len(self.type)):
                if i == type_actuel:
                    type = self.type_file[self.type[i]]
                    if selected_element_type  >= 0 and selected_element_type < len(type):
                        return int(indice + selected_element_type), True
                indice += len(self.type_file[self.type[i]])
        return -1, False

    def element_of_value(self, indice):
        if indice < 0:
            return "Erreur", False
        valeur = indice
        for i in range(len(self.type)):
            if self.type[i] in self.type_file:
                type = self.type_file[self.type[i]]
                if valeur < len(type):
                    return LoadData.loadData.get_texture(type[valeur].image_name)
                valeur -= len(self.type_file[self.type[i]])
        return "Erreur", False

    def get_name_by_value(self, value):
        if value < 0:
            return "Erreur", "Erreur", False
        valeur = value
        for i in range(len(self.type)):
            if self.type[i] in self.type_file:
                type = self.type_file[self.type[i]]
                if valeur < len(type):
                    return self.type[i], type[valeur].image_name, True
                valeur -= len(self.type_file[self.type[i]])
        return "Erreur", "Erreur", False

    def get_info_by_name(self, name):
        indice = 0
        for key in self.type_file.keys():
            keys = self.type_file[key]
            for v in keys:
                if v.image_name == name:
                    return indice, key, True
            indice += 1
        return -1, "Erreur", False

    def updateEvent(self, event):
        self.home.updateEvent(event)
        self.next_theme.updateEvent(event)
        self.previous_them.updateEvent(event)
        self.save.updateEvent(event)
        self.nouveau.updateEvent(event)
        self.clear_map.updateEvent(event)

        self.largeur.updateEvent(event)
        self.hauteur.updateEvent(event)

        indice = -1
        if self.next_theme.is_click():
            self.update_type(True)
            indice = -2

        if self.previous_them.is_click():
            self.update_type(False)
            indice = -2

        liste = self.type_file[self.type[self.type_actuel]]

        for i in range(len(liste)):
            actual = liste[i].updateEvent(event)
            if actual:
                indice = i

        if indice != -1:
            self.selected_element_type = -1
            for i in range(len(liste)):
                if indice == -2 and liste[i].is_selected:
                    self.selected_element_type = i
                elif indice != i:
                    liste[i].is_selected = False
                    liste[i].state = liste[i].normal
                else:
                    self.selected_element_type = i

        if event.type == MOUSEBUTTONDOWN:
            validate, x, y = self.is_enter(event.pos[0], event.pos[1])
            if event.button == pygame.BUTTON_LEFT:
                if validate:
                    indice, validate = self.value_of_element(self.type_actuel, self.selected_element_type)
                    if validate:
                        a1, b1, c1 = self.get_name_by_value(indice)
                        if self.type[self.type_actuel] == "joueur":
                            self.x_player = x
                            self.y_player = y
                            self.choix_player = b1
                            self.joueur_erreur = False
                            self.map[x, y] = self.indice_sol
                        else:
                            self.map[x, y] = indice
                            self.save.enable()
                            self.nouveau.enable()
                            self.indice_sol = -1
                            for i in range(self.hauteur.value):
                                for j in range(self.largeur.value):
                                    a, b, c = self.get_name_by_value(self.map[i, j])
                                    if c and a == "sol":
                                        self.indice_sol = self.map[i, j]

            elif event.button == pygame.BUTTON_RIGHT:
                if validate:
                    self.map[x, y] = -1
                    self.save.deseable()
                    self.nouveau.deseable()
                    for i in range(self.hauteur.value):
                        break_to = False
                        for j in range(self.largeur.value):
                            if self.map[i, j] != -1:
                                self.save.enable()
                                self.nouveau.enable()
                                break_to = True
                                break
                        if break_to:
                            break
                    self.indice_sol = -1
                    for i in range(self.hauteur.value):
                        for j in range(self.largeur.value):
                            a, b, c = self.get_name_by_value(self.map[i, j])
                            if c and a == "sol":
                                self.indice_sol = self.map[i, j]


        elif event.type == MOUSEMOTION:
            validate, self.x_hover, self.y_hover = self.is_enter(event.pos[0], event.pos[1])

        if self.largeur.value_change:
            self.dimenssion = self.largeur_dessin // self.largeur.value
            self.hauteur.set_value(self.hauteur_dessin // self.dimenssion)
            self.map = np.resize(self.map, new_shape=(self.hauteur.value, self.largeur.value))

        if self.hauteur.value_change:
            self.dimenssion = self.hauteur_dessin // self.hauteur.value
            self.largeur.set_value(self.largeur_dessin // self.dimenssion)
            self.map = np.resize(self.map, new_shape=(self.hauteur.value, self.largeur.value))

        if self.home.is_click():
            self.parent.state = self.parent.menu_principale
            self.home.state = self.home.normal_file
            self.enregistrer = False

        if self.clear_map.is_click():
            for i in range(self.hauteur.value):
                for j in range(self.largeur.value):
                    self.map[i, j] = -1
            self.save.deseable()
            self.nouveau.deseable()
            self.enregistrer = False

        if self.save.is_click():
            self.enregistrer = True
            endpoint_is_in = False

            nombre_endpoint = {}
            for value in self.type_file["endpoint"]:
                nombre_endpoint[value.image_name] = 0
            nombre_caisse = {}
            nombre_caisse_ok = {}
            for value in self.type_file["caisse"]:
                nombre_caisse[value.image_name] = 0
            for value in self.type_file["caisse_ok"]:
                nombre_caisse_ok[value.image_name] = False

            for i in range(self.hauteur.value):
                for j in range(self.largeur.value):
                    a, b, c = self.get_name_by_value(self.map[i, j])
                    if c and a == "endpoint":
                        endpoint_is_in = True
                        nombre_endpoint[b] += 1
                    if c and a == "caisse":
                        nombre_caisse[b] += 1
            path, validate = LoadData.loadData.get_level_path(0)
            if endpoint_is_in:
                caisse = [0, 0, 0, 0, 0]
                k = 0
                for key in nombre_caisse.keys():
                    caisse[k%5] += nombre_caisse[key]
                    if nombre_caisse[key] > 0:
                        p = 0
                        for keys in nombre_caisse_ok.keys():
                            if p == k:
                                nombre_caisse_ok[keys] = True
                                break
                            p += 1
                    k += 1
                k = 0
                for key in nombre_endpoint.keys():
                    if nombre_endpoint[key] != caisse[k]:
                        endpoint_is_in = False
                        self.caisse_erreur = True
                        break
                    k += 1
            else:
                self.endpoint_erreur = True

            if validate and endpoint_is_in and self.joueur_erreur == False:
                if self.deja_enregistre == False:
                    fichier = open(path, "a")
                    fichier.write("\n")
                    fichier.write(self.level_name+" datas/levels/"+self.level_name+".lvl"+" false")
                    fichier.close()
                    self.deja_enregistre = True

                fichier = open("datas/levels/"+self.level_name+".lvl", "w")
                fichier.write("name "+self.level_name+"\n")
                minx, miny, maxx, maxy = self.largeur.value,self.hauteur.value, 0, 0
                liste = {}
                sol_indice = -1
                for i in range(self.hauteur.value):
                    for j in range(self.largeur.value):
                        if self.map[i, j] != -1:
                            if i < miny:
                                miny = i
                            if i > maxy:
                                maxy = i

                            if j < minx:
                                minx = j
                            if j > maxx:
                                maxx = j

                        a, b, c = self.get_name_by_value(self.map[i, j])
                        if c:
                            if not (a in liste):
                                liste[a] = {}
                            lt = liste[a]
                            if b in liste:
                                continue
                            lt[b] = str(self.map[i, j])
                            if a == 'sol':
                                sol_indice = self.map[i, j]
                fichier.write("lh " + str(maxy - miny + 1) + " " + str(maxx - minx + 1) + "\n")

                typeM = ""
                if self.choix_player == "player_21":
                    typeM = "datas/players/mario.pin"
                elif self.choix_player == "player_03":
                    typeM = "datas/players/mario_outline.pin"

                if self.y_player != -1 and self.x_player != -1:
                    fichier.write("pp " + str(self.y_player-minx) + " " + str(self.x_player - miny) +" down_idle " +typeM+ "\n")
                fichier.write("\n")

                for key in liste.keys():
                    lt = liste[key]
                    for key1 in lt.keys():
                        if key != "joueur" and key != "caisse_ok":
                            fichier.write("ttn " + key + " "+ key1 + " "+ lt[key1]+"\n")

                for key in nombre_caisse_ok.keys():
                    if nombre_caisse_ok[key] == True:
                        a, b, c = self.get_info_by_name(key)
                        if c:
                            fichier.write("ttn caisse_ok " + key + " " + str(a) + "\n")

                fichier.write("\n")
                for i in range(maxy - miny + 1):
                    fichier.write("lg")
                    for j in range((maxx - minx + 1)):
                        a, b, c = self.get_name_by_value(self.map[i + miny, j + minx])
                        if c:
                            if a == "joueur":
                                fichier.write(" " + str(sol_indice))
                            else:
                                fichier.write(" " + str(self.map[i + miny, j + minx]))
                        else:
                            fichier.write(" "+str(self.map[i + miny, j + minx]))
                    fichier.write("\n")
                fichier.close()
                Levels.levels.init_loader()
            else:
                pass

        if self.nouveau.is_click():
            for i in range(self.hauteur.value):
                for j in range(self.largeur.value):
                    self.map[i, j] = -1
            self.save.deseable()
            self.nouveau.deseable()

            self.level_name = "level_"+str(Levels.levels.get_size() + 1)
            self.deja_enregistre = False
            self.enregistrer = False


    def is_enter(self, x, y):
        xdep = (self.largeur_dessin - self.dimenssion * self.largeur.value) / 2 + 50
        ydep = (self.hauteur_dessin - self.dimenssion * self.hauteur.value) / 2 + 110
        if x < xdep or y < ydep or x >= xdep + (self.dimenssion * self.largeur.value) or y >= ydep + (self.dimenssion * self.hauteur.value):
            return False, -1, -1
        for i in range(self.hauteur.value):
            for j in range(self.largeur.value):
                if x >= xdep and x < xdep + self.dimenssion and y >= ydep and y < ydep + self.dimenssion:
                    return True, i, j
                xdep += self.dimenssion
            xdep = (self.largeur_dessin - self.dimenssion * self.largeur.value) / 2 + 50
            ydep += self.dimenssion


    def draw(self, screen):
        pygame.draw.rect(screen, color=(0, 100, 100, 0), rect=(0, 0, 1000, 100))
        self.home.draw(screen)
        self.next_theme.draw(screen)
        self.previous_them.draw(screen)
        self.save.draw(screen)
        self.nouveau.draw(screen)
        self.clear_map.draw(screen)
        increment = (self.nouveau.rect.width - self.type_image.get_rect().width)/2
        screen.blit(self.type_image, (self.home.rect.x + self.home.rect.width + 10 + increment, (self.home.rect.height - self.type_image.get_rect().height)/2 + 5))
        self.hauteur.draw(screen)
        self.largeur.draw(screen)
        if self.enregistrer:
            if self.caisse_erreur:
                #print("un")
                self.erreur_creation_image = self.font.render(self.message_erreur_caisse, True, (220, 220, 220))
                screen.blit(self.erreur_creation_image, (1000 - self.erreur_creation_image.get_rect().width - 50, 100))
            elif self.joueur_erreur:
                #print("deux")
                self.erreur_creation_image = self.font.render(self.message_erreur_joueur, True, (220, 220, 220))
                screen.blit(self.erreur_creation_image, (1000 - self.erreur_creation_image.get_rect().width - 50, 100))
            elif self.message_erreur_endpoint:
                #print("trois")
                self.erreur_creation_image = self.font.render(self.message_erreur_endpoint, True, (220, 220, 220))
                screen.blit(self.erreur_creation_image, (1000 - self.erreur_creation_image.get_rect().width - 50, 100))
            else:
                self.erreur_creation_image = self.font.render(self.message_erreur_endpoint, True, (220, 220, 220))
                screen.blit(self.erreur_creation_image, (1000 - self.erreur_creation_image.get_rect().width - 50, 100))

        liste = self.type_file[self.type[self.type_actuel]]
        for i in range(len(liste)):
            liste[i].draw(screen)

        x = (self.largeur_dessin - self.dimenssion*self.largeur.value)/2 + 50
        y = (self.hauteur_dessin - self.dimenssion*self.hauteur.value)/2 + 110
        for i in range(self.hauteur.value):
            for j in range(self.largeur.value):
                if self.map[i, j] != -1:
                    a, b, c = self.get_name_by_value(self.map[i, j])
                    if c and a == "sol":
                        self.indice_sol = self.map[i, j]
                    texture, validate = self.element_of_value(self.indice_sol)
                    if validate:
                        texture = pygame.transform.scale(texture, (self.dimenssion, self.dimenssion))
                        screen.blit(texture, (x, y))

                    texture, validate = self.element_of_value(self.map[i, j])
                    if validate:
                        texture = pygame.transform.scale(texture, (self.dimenssion, self.dimenssion))
                        screen.blit(texture, (x, y))

                rect = pygame.Rect(x, y, self.dimenssion, self.dimenssion)
                self.draw_rect_alpha(screen, (100, 100, 100, 100), rect, epaisseur=1)
                self.draw_rect_alpha(screen, (0, 0, 0, 100), rect)
                if self.x_hover == i and self.y_hover == j:
                    self.draw_rect_alpha(screen, (200, 200, 200, 100), rect)
                    #pygame.draw.rect(screen, (200,200,200), rect=rect, width=1)
                #else:
                    #pygame.draw.rect(screen, (0,0,0), rect=rect, width=1)
                x += self.dimenssion
            y += self.dimenssion
            x = (self.largeur_dessin - self.dimenssion*self.largeur.value)/2 + 50
        if self.x_player >= 0 and self.x_player < self.largeur.value:
            if self.y_player >= 0 and self.y_player < self.hauteur.value:
                a, b = LoadData.loadData.get_texture(self.choix_player)
                if b:
                    x = (self.largeur_dessin - self.dimenssion * self.largeur.value) / 2 + 50
                    y = (self.hauteur_dessin - self.dimenssion * self.hauteur.value) / 2 + 110
                    a = pygame.transform.scale(a, (self.dimenssion, self.dimenssion))
                    screen.blit(a, (x + self.y_player*self.dimenssion, y + self.x_player*self.dimenssion))

    def update(self, delta_time):
        liste = self.type_file[self.type[self.type_actuel]]
        for i in range(len(liste)):
            if liste[i].is_selected :
                self.selected_element_type = i

class LevelChoix():
    def __init__(self, parent):
        self.parent = parent
        self.init_interface()

    def init_interface(self):
        self.bouton_back = Bouton("PRECEDENT", ftSize=30)
        self.bouton_next = Bouton("SUIVANT", ftSize=30)
        self.bouton_home = Bouton("HOME", ftSize=30)
        self.top_bouton()
        self.bouton_level = {}
        self.bouton_size_w = 100
        self.bouton_size_h = 35
        self.bouton_space = 10
        self.page_number = 0
        self.ligne_page = int((700 - self.bouton_space) / (self.bouton_size_h + self.bouton_space))
        self.colone_page = int((1000 - self.bouton_space) / (self.bouton_size_w + self.bouton_space))
        self.actual_page = 0
        self.level_bouton()

        self.erreur_fichier = "BIEN"
        self.font = pygame.font.SysFont("Showcard Gothic", 30)
        self.titre_image = self.font.render(self.erreur_fichier, True, (220, 220, 220))

    def change_error(self, message):
        self.erreur_fichier = message
        self.titre_image = self.font.render(self.erreur_fichier, True, (200, 10, 10))

    def top_bouton(self):
        self.bouton_back.set_size(200, 50, bd=4, bdr=10)
        self.bouton_back.set_position(20, 20)
        self.bouton_back.deseable()
        self.bouton_home.set_size(200, 50, bd=4, bdr=10)
        self.bouton_home.set_position((1000 - self.bouton_home.rect.width)/2, 20)
        self.bouton_next.set_size(200, 50, bd=4, bdr=10)
        self.bouton_next.set_position(1000 - (self.bouton_next.rect.width + 20), 20)
        self.bouton_next.deseable()

    def level_bouton(self):
        taille = Levels.levels.get_size()
        for i in range(taille):
            niveau, erreur = Levels.levels.get_level_by_position(i)
            niveau.parent = self.parent
            self.bouton_level[i] = [Bouton(str(i+1), ftSize=20), niveau, erreur]

        self.page_number = int(taille/(self.ligne_page*self.colone_page))

        if self.page_number == 0 and taille > 0:
            self.page_number = 1
            self.actual_page = 1

        if self.page_number > 1:
            self.bouton_back.enable()
            self.bouton_next.enable()

        self.got_page(self.actual_page)

    def got_page(self, position):
        if position <= 0 and position > self.page_number:
            return False
        self.actual_page = position
        prev_x = self.bouton_space
        prev_y = self.bouton_next.rect.height + 60 + self.bouton_space
        break_to = False
        for i in range(len(self.bouton_level)):
            bouton = self.bouton_level[i]
            bouton[0].deseable()
        for i in range(self.ligne_page):
            for j in range(self.colone_page):
                p_b = i * self.colone_page + j + ((self.actual_page-1) * self.ligne_page * self.colone_page)
                if p_b >= len(self.bouton_level):
                    break_to = True
                    break
                bouton = self.bouton_level[p_b]
                bouton[0].set_size(self.bouton_size_w, self.bouton_size_h, bd=4, bdr=10)
                bouton[0].set_position(prev_x, prev_y)
                bouton[0].enable()
                if bouton[1].is_finish:
                    bouton[0].normal_file = (0, 201, 252)
                    bouton[0].hover_file = (74, 214, 249)
                    bouton[0].click_file = (0, 187, 235)
                prev_x += self.bouton_space + self.bouton_size_w
            if break_to:
                break
            prev_x = self.bouton_space
            prev_y += self.bouton_size_h + self.bouton_space

    def updateEvent(self, event):

        if self.actual_page == 1:
            self.bouton_back.deseable()

        if self.actual_page == self.page_number:
            self.bouton_next.deseable()

        self.bouton_back.updateEvent(event)
        self.bouton_home.updateEvent(event)
        self.bouton_next.updateEvent(event)

        if self.bouton_home.is_click():
            self.parent.state = self.parent.menu_principale
            self.bouton_home.state = self.bouton_home.normal_file

        if self.bouton_back.is_click():
            self.got_page(self.actual_page - 1)

        if self.bouton_next.is_click():
            self.got_page(self.actual_page + 1)

        for i in range(len(self.bouton_level)):
            bouton = self.bouton_level[i]
            bouton[0].updateEvent(event)

            if bouton[0].is_click():
                if bouton[2] == False:
                    self.change_error("NIVEAU * "+ str(i + 1) +" * INTROUVABLE")
                else:
                    bouton[1].load_level()
                    if bouton[1].map_error:
                        self.change_error("NIVEAU * "+ str(i + 1) +" * COROMPU")
                    else:
                        self.change_error("BIEN")
                        self.parent.state = bouton[1]
                        bouton[0].state = bouton[0].normal_file

    def draw(self, screen):
        pygame.draw.rect(screen, color=(0, 100, 100, 0), rect=(0, 0, 1000, self.bouton_next.rect.height + 40))
        self.bouton_back.draw(screen)
        self.bouton_home.draw(screen)
        self.bouton_next.draw(screen)

        if self.erreur_fichier != "BIEN":
            screen.blit(self.titre_image, ((1000 - self.titre_image.get_rect().width) / 2, 80))

        for i in range(len(self.bouton_level)):
            bouton = self.bouton_level[i]
            bouton[0].draw(screen)

    def update(self, delta_time):
        pass


class MenuPrincipal():
    def __init__(self, parent):
        self.parent = parent
        self.bouton_play = Bouton("JOUER")
        self.bouton_play.rect.x = (1000 - self.bouton_play.rect.width)/2
        self.bouton_play.rect.y = 250
        self.bouton_create_level = Bouton("CREATION")
        self.bouton_create_level.rect.x = self.bouton_play.rect.x
        self.bouton_create_level.rect.y = self.bouton_play.rect.y + self.bouton_play.rect.height + 20
        #self.bouton_create_level.deseable()
        self.bouton_credit = Bouton("CREDIT")
        self.bouton_credit.rect.x = self.bouton_create_level.rect.x
        self.bouton_credit.rect.y = self.bouton_create_level.rect.y + self.bouton_create_level.rect.height + 20
        #self.bouton_credit.deseable()
        self.bouton_quit = Bouton("BYE BYE")
        self.bouton_quit.rect.x = self.bouton_credit.rect.x
        self.bouton_quit.rect.y = self.bouton_credit.rect.y + self.bouton_credit.rect.height + 20

        self.font = pygame.font.SysFont("Showcard Gothic", 100)
        self.titre_image = self.font.render("S O K O G A P", True, (255, 255, 255))

    def updateEvent(self, event):
        self.bouton_play.updateEvent(event)
        self.bouton_create_level.updateEvent(event)
        self.bouton_credit.updateEvent(event)
        self.bouton_quit.updateEvent(event)

        if self.bouton_play.is_click():
            self.parent.menu_choix_level.init_interface()
            self.parent.state = self.parent.menu_choix_level
            self.bouton_play.state = self.bouton_play.normal_file
        if self.bouton_credit.is_click():
            pass
        if self.bouton_quit.is_click():
            self.parent.game_running = False
        if self.bouton_create_level.is_click():
            self.parent.state = self.parent.menu_cajouter_level
            self.bouton_create_level.state = self.bouton_create_level.normal_file

    def draw(self, screen):
        screen.blit(self.titre_image, ((1000 - self.titre_image.get_rect().width)/2, 75))
        self.bouton_play.draw(screen)
        self.bouton_create_level.draw(screen)
        self.bouton_credit.draw(screen)
        self.bouton_quit.draw(screen)

        texture, validate = LoadData.loadData.get_texture("playerFace_dark")
        if validate:
            screen.blit(texture, ((1000 - 128) / 2, 50))

    def update(self, delta_time):
        pass

class CreditInterface():
    def __init__(self, parent):
        pass