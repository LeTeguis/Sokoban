import Game

if __name__ == '__main__':
    game = Game.Game()
    game.init()
    game.load_screen()
    game.loop()
    game.load_screen()
    game.close()