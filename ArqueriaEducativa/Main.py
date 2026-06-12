import pygame
from lib.Core import Core


def main():
    pygame.init()
    pygame.display.set_caption("Arqueria Educativa")
    juego = Core()
    juego.iniciar()


if __name__ == "__main__":
    main()
