import pygame
import sys
from code.game import Game  # Importa Game de code/game.py
from code.menu import Menu  # Importa Menu de code/menu.py

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600

def main():
    while True:
        menu = Menu(WIN_WIDTH, WIN_HEIGHT)
        escolha = menu.run()

        if escolha == "start":
            game = Game(WIN_WIDTH, WIN_HEIGHT)
            game.tocar_musica_fase()
            game.run()
        elif escolha == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()