import sys
import pygame
from lib.Core import Core


def main():
    pygame.init()
    pygame.display.set_caption("Flechas y Cuentas")
    juego = Core()
    juego.iniciar()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"El juego se cerro por un error: {e}")
        pygame.quit()
        sys.exit(1)
