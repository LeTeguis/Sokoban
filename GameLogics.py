
class GameLogics():
    def __init__(self):
        self.load_info_logics()
    def load_info_logics(self):
        self.type_file = {}
        self.type = ["sol", "mur", "caisse", "caisse_ok", "endpoint", "joueur"]
        fichier = open("datas/levels/level_tiles_infos.lti", "r")
        position = 0
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
                        self.type_file[self.seof(infos[0])] = {}
                    liste = self.type_file[self.seof(infos[0])]
                    for i in range(len(infos) - 1):
                        liste[self.seof(infos[i + 1])] = position
                        position += 1
            else:
                break
    def complement_caisse(self, caisse, valeur):
        if caisse in self.type_file:
            valeur_dep = valeur
            caisse_ok_info = []
            endpoint_info = []
            valide = False
            for key in self.type_file.keys():
                vkey = self.type_file[key]
                for elm in vkey.keys():
                    if vkey[elm] == valeur and valeur_dep >= 0:
                        keys2 = self.type_file["caisse_ok"]
                        i = 0
                        for k in keys2.keys():
                            if i == valeur_dep:
                                caisse_ok_info.append(k)
                                caisse_ok_info.append(keys2[k])
                                #valide = True
                                break
                            i += 1
                        keys2 = self.type_file["endpoint"]
                        i = 0
                        for k in keys2.keys():
                            if i == valeur_dep%5:
                                endpoint_info.append(k)
                                endpoint_info.append(keys2[k])
                                valide = True
                                break
                            i += 1
                valeur_dep -= len(self.type_file[key])
            return  valide, caisse_ok_info, endpoint_info

    def complement_caisse_ok(self, caisse_ok, valeur):
        if caisse_ok in self.type_file:
            valeur_dep = valeur
            caisse_info = []
            endpoint_info = []
            valide = False
            for key in self.type_file.keys():
                vkey = self.type_file[key]
                for elm in vkey.keys():
                    if vkey[elm] == valeur and valeur_dep >= 0:
                        keys2 = self.type_file["caisse"]
                        i = 0
                        for k in keys2.keys():
                            if i == valeur_dep:
                                caisse_info.append(k)
                                caisse_info.append(keys2[k])
                                # valide = True
                                break
                            i += 1
                        keys2 = self.type_file["endpoint"]
                        i = 0
                        for k in keys2.keys():
                            if i == valeur_dep % 5:
                                endpoint_info.append(k)
                                endpoint_info.append(keys2[k])
                                valide = True
                                break
                            i += 1
                valeur_dep -= len(self.type_file[key])
            return valide, caisse_info, endpoint_info

    def complement_endpoint(self, caisse_ok, valeur):
        if caisse_ok in self.type_file:
            valeur_dep = valeur
            caisse_info = []
            caisse_ok_info = []
            valide = False
            for key in self.type_file.keys():
                vkey = self.type_file[key]
                for elm in vkey.keys():
                    if vkey[elm] == valeur and valeur_dep >= 0:
                        keys2 = self.type_file["caisse"]
                        i = 0
                        for k in keys2.keys():
                            if i%5 == valeur_dep:
                                caisse_info.append(k)
                                caisse_info.append(keys2[k])
                                # valide = True
                            i += 1
                        keys2 = self.type_file["caisse_ok"]
                        i = 0
                        for k in keys2.keys():
                            if i%5 == valeur_dep:
                                caisse_ok_info.append(k)
                                caisse_ok_info.append(keys2[k])
                                valide = True
                            i += 1
                valeur_dep -= len(self.type_file[key])
            return valide, caisse_info, caisse_ok_info

    def seof(self, string):
        return ((string).split("\n"))[0]

    def get_infos_value(self, valeur):
        for key in self.type_file.keys():
            vkey = self.type_file[key]
            for elm in vkey.keys():
                if vkey[elm] == valeur:
                    return key, elm, True
        return "Erreur", "Erreur", False

    def logics_game(self, xp, yp, mxp, myp, lg, cl, map, sol):
        if xp + mxp >= 0 and cl > xp + mxp and yp + myp >= 0 and lg > yp + myp:
            type_info, name_info, validate = self.get_infos_value(int(map[int(yp + myp), int(xp + mxp)]))
            if validate and int(map[int(yp + myp), int(xp + mxp)]) != -1:
                if type_info != "mur":
                    x, y = int(xp + mxp * 2), int(yp + myp * 2)
                    val1 = False
                    if x >= 0 and cl > x and y >= 0 and lg > y:
                        val1 = True

                    if type_info == "caisse":
                        if val1:
                            type_info_1, name_info_1, validate_1 = self.get_infos_value(int(map[int(y), int(x)]))
                            if validate_1 and type_info_1 != "mur" and int(map[int(y), int(x)]) != -1:
                                if type_info_1 == "sol":
                                    return int(sol), int(map[int(yp + myp), int(xp + mxp)]), True
                                if type_info_1 == "endpoint":
                                    val, caisse_ok_info, endpoint_ok_info = self.complement_caisse("caisse",map[int(yp + myp), int(xp + mxp)])
                                    if val and map[int(y), int(x)] == endpoint_ok_info[1]:
                                        return int(sol), int(caisse_ok_info[1]), True
                                    else:
                                        return int(sol), int(map[int(yp + myp), int(xp + mxp)]), True
                    elif type_info == "caisse_ok":
                        if val1:
                            type_info_1, name_info_1, validate_1 = self.get_infos_value(int(map[int(y), int(x)]))
                            if validate_1  and type_info_1 != "mur" and int(map[int(y), int(x)]) != -1:
                                val, caisse_info, endpoint_ok_info = self.complement_caisse_ok("caisse_ok",map[int(yp + myp), int(xp + mxp)])
                                if type_info_1 == "sol":
                                    return int(endpoint_ok_info[1]), int(caisse_info[1]), True
                                if type_info_1 == "endpoint":
                                    if map[int(y), int(x)] == endpoint_ok_info[1]:
                                        return int(endpoint_ok_info[1]), int(map[int(yp + myp), int(xp + mxp)]), True
                                    else:
                                        return int(endpoint_ok_info[1]), int(caisse_info[1]), True
                    elif type_info == "endpoint" or type_info == "sol":
                        #if val1:
                        #   return map[int(yp + myp), int(xp + mxp)], map[int(y), int(x)], True
                        #else:
                            #return int(map[int(yp + myp), int(xp + mxp)]), int(-1), True
                            return -1, -1, True
                    else:
                        pass
        return -1, -1, False

    def logics_one(self, xp, yp, mxp, myp, lg, cl, map, nature):
        if xp + mxp >= 0 and cl > xp + mxp and yp + myp >= 0 and lg > yp + myp:
            n, validate = self.get_nature(map[int(yp + myp), int(xp + mxp)], nature)
            if validate:
                if n != "mur" and map[int(yp + myp), int(xp + mxp)] != -1:
                    x , y = int(xp + mxp*2), int(yp + myp*2)
                    if n == "caisse":
                        if x >= 0 and cl > x and y >= 0 and lg > y:
                            n, validate = self.get_nature(map[y, x], nature)
                            if validate:
                                if n == "endpoint":
                                    n, validate = self.getValue("caisse_ok", 0, nature)
                                    n2, validate2 = self.getValue("sol", 0, nature)
                                    if validate and validate2:
                                        return True, n2, n
                                if n == "sol":
                                    n, validate = self.getValue("caisse", 0, nature)
                                    n2, validate2 = self.getValue("sol", 0, nature)
                                    if validate and validate2:
                                        return True, n2, n
                    elif n == "caisse_ok":
                        if x >= 0 and cl > x and y >= 0 and lg > y:
                            n, validate = self.get_nature(map[y, x], nature)
                            if validate:
                                if n == "endpoint":
                                    n, validate = self.getValue("caisse_ok", 0, nature)
                                    n2, validate2 = self.getValue("endpoint", 0, nature)
                                    if validate and validate2:
                                        return True, n2, n
                                if n == "sol":
                                    n, validate = self.getValue("caisse", 0, nature)
                                    n2, validate2 = self.getValue("endpoint", 0, nature)
                                    if validate and validate2:
                                        return True, n2, n
                    elif n == "sol":
                        if x >= 0 and cl > x and y >= 0 and lg > y:
                            t, validate = self.get_nature(map[y, x], nature)
                            if validate:
                                n2, validate = self.getValue(t, 0, nature)
                                n, validate1 = self.getValue("sol", 0, nature)
                                if validate and validate1:
                                    return True, n, n2
                    elif n == "endpoint":
                        if x >= 0 and cl > x and y >= 0 and lg > y:
                            n, validate = self.get_nature(map[y, x], nature)
                            if validate:
                                n2, validate = self.getValue(n, 0, nature)
                                n, validate1 = self.getValue("endpoint", 0, nature)
                                if validate and validate1:
                                    return True, n, n2
        return False, -1, -1

    def is_finish(self, lg, cl, map, nature):
        for i in range(lg):
            for j in range(cl):
                n, validate = self.get_nature(map[int(i), int(j)], nature)
                if validate and n == "endpoint":
                    return False
        return True

    def get_nature(self, valeur, nature):
        for n in nature.keys():
            name = nature.get(n)
            for v in name.keys():
                if int(name.get(v)) == int(valeur):
                    return n, True
        return "Erreur", False

    def getValue(self, name, indice, nature):
        if name in nature:
            tile = nature[name]
            if indice >= 0 and len(tile) > indice:
                k = 0
                for texture in tile.keys():
                    if k == indice:
                        return int(tile.get(texture)), True
                    k += 1
        return -1, False

gameLogics = GameLogics()