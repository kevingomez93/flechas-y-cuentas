import os
import pygame

PROYECTO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cargar_sprite(ruta):
    # busca la imagen en la carpeta Sprite
    ruta_completa = os.path.join(PROYECTO_DIR, "Sprite", ruta)
    try:
        return pygame.image.load(ruta_completa).convert_alpha()
    except (pygame.error, FileNotFoundError) as e:
        raise FileNotFoundError(
            f"No se pudo cargar el sprite '{ruta}'. "
            f"Verifica que el archivo exista en la carpeta Sprite. Detalle: {e}"
        )


def cargar_fondo(num_nivel, ancho, alto):
    original = cargar_sprite(os.path.join("Fondos", f"fondo_nivel{num_nivel}.png"))
    return pygame.transform.scale(original, (ancho, alto))
