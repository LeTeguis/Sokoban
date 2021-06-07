import pygame

class LoadData():
    def __init__(self):
        self.path = "datas/game_init.gin"
        fichier = open(self.path, "r")
        self.texture = {}
        texture_path = "default"
        self.levels_path = {}
        self.player_infos = {}

        while True:
            ligne = fichier.readline()
            if ligne != "":
                if ligne != "\n":
                    infos_copy = ligne.split(" ")
                    infos = []
                    for value in infos_copy:
                        if value != "":
                            infos.append(value)
                    if self.seof(infos[0]) == "texture":
                        texture_path = self.loadTexture(ligne, texture_path)
                    elif self.seof(infos[0]) == "level":
                        self.levels_path[self.seof(infos[1])] = self.seof(infos[2])
            else:
                break

    def seof(self, string):
        return ((string).split("\n"))[0]

    def loadPlayer(self, ligne):
        infos = ligne.split(" ")
        self.player_infos[self.seof(infos[1])] = self.seof(infos[2])

    def loadTexture(self, ligne, path):
        infos_copy = ligne.split(" ")
        infos = []
        for value in infos_copy:
            if value != "":
                infos.append(value)
        if self.seof(infos[1]) == "path" and len(infos) == 3:
            return self.seof(infos[2])
        elif self.seof(infos[1]) == "add":
            for i in range(len(infos) - 2):
                image = self.seof(infos[i + 2])
                nom = image.split(".")
                #print(path + "/" + image)
                self.texture[nom[0]] = pygame.image.load(path + "/" + image)
        return path

    def get_player(self, name):
        if name in self.player_infos:
            return self.player_infos[name], True
        return "Erreur", False

    def get_texture(self, nom):
        if nom in self.texture:
            return self.texture[nom], True
        return "Erreur", False

    def get_level_path(self, position):
        if position >= 0 and position < len(self.levels_path):
            indice = 0
            for level in self.levels_path:
                if indice == position:
                    return self.levels_path[level], True
                indice += 1
        return "Erreur", False

loadData = LoadData()