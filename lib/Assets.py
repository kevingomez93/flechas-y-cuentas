import os
import pygame

PROYECTO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cargar_sprite(ruta):
    return pygame.image.load(os.path.join(PROYECTO_DIR, "Sprite", ruta)).convert_alpha()


def cargar_fondo(num_nivel, ancho, alto):
    original = cargar_sprite(os.path.join("Fondos", f"fondo_nivel{num_nivel}.png"))
    return pygame.transform.scale(original, (ancho, alto))
