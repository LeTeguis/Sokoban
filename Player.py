import pygame
import LoadData

class Player():
    def __init__(self, x, y, player_pack, action):
        self.position_x = x
        self.position_y = y

        self.actions = {}
        self.size = 10
        fichier = open(player_pack, "r")

        while True:
            ligne = fichier.readline()
            if ligne != "":
                value = ligne.split(" ")
                actions = []
                for i in range(len(value) - 1):
                    actions.append(self.seof(value[i + 1]))
                self.actions[self.seof(value[0])] = actions
            else:
                break

        self.state = action
        self.frame = 0
        self.frame_leng = 0
        self.loop_number = 3
        self.loop_actual = 1
        self.x_move = 0
        self.y_move = 0
        self.get_frame_leng()

    def resize(self, size):
        self.size = size

    def seof(self, string):
        return ((string).split("\n"))[0]

    def nextFrame(self):
        self.frame += 1
        if self.state in self.actions and self.frame >= self.frame_leng:
            self.frame = 0

    def changeAction(self, action):
        if action in self.actions:
            self.state = action
            self.get_frame_leng()

    def direction_Change(self, x, y):
        if x == 0:
            if y == -1:
                self.changeAction("up_walk")
            elif y == 1:
                self.changeAction("down_walk")
        elif y == 0:
            if x == -1:
                self.changeAction("left_walk")
            elif x == 1:
                self.changeAction("right_walk")

    def setPosition(self, x, y):
        self.position_x = x
        self.position_y = y

    def move(self, x, y):
        self.position_x += x
        self.position_y += y

    def set_move(self, x, y):
        self.x_move = x
        self.y_move = y

    def draw(self, screen, ofsetX, ofsetY):
        if self.state in self.actions:
            type = self.actions[self.state]
            texture, validate = LoadData.loadData.get_texture(type[self.frame])
            if validate:
                texture = pygame.transform.scale(texture, (self.size, self.size))
                x, y = self.position_x * self.size + ofsetX, self.position_y * self.size + ofsetY
                screen.blit(texture, (x, y))

    def isIdle(self):
        if self.state == "left_idle" or self.state == "right_idle" or self.state == "up_idle" or self.state == "down_idle":
            return True
        return False

    def animation(self):
        frame = self.frame
        self.nextFrame()
        if self.frame == 0:
            if self.isIdle() == False:
                for i in range(self.frame_leng - 1):
                    self.move(-self.x_move / self.frame_leng, -self.y_move / self.frame_leng)

                self.move(self.x_move, self.y_move)
                self.x_move, self.y_move = 0, 0

            self.changeAction("down_idle")

            return False, frame
        if self.isIdle() == False:
            self.move(self.x_move/self.frame_leng, self.y_move/self.frame_leng)
        return True, frame

    def get_frame_leng(self):
        if self.state in self.actions:
            self.frame_leng = len(self.actions[self.state])