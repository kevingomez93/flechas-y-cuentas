"""
generar_sprites.py
Genera los sprites del juego como imagenes PNG usando pygame y los guarda
en las carpetas Sprite/. Ejecutar una sola vez antes de distribuir el .rar.
El juego NO necesita este script para funcionar (los graficos se dibujan
por primitivas en tiempo real), pero los archivos PNG documentan los assets.
"""
import os
import pygame
import math

pygame.init()

BASE = os.path.dirname(__file__)


def guardar(surface: pygame.Surface, ruta: str):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    pygame.image.save(surface, ruta)
    print(f"  guardado: {ruta}")


# ---------------------------------------------------------------------------
# Arquero  (80x120 px)
# ---------------------------------------------------------------------------
def sprite_arquero():
    surf = pygame.Surface((80, 120), pygame.SRCALPHA)
    BEIGE       = (245, 222, 179)
    MARRON      = (101,  67,  33)
    MARRON_CLARO= (160, 110,  60)

    cx, cy = 32, 75
    # Cuerpo
    pygame.draw.rect(surf, BEIGE, (cx - 15, cy - 35, 30, 50), border_radius=8)
    # Cabeza
    pygame.draw.circle(surf, BEIGE, (cx, cy - 45), 16)
    pygame.draw.arc(surf, MARRON, (cx - 16, cy - 61, 32, 32), 0, math.pi, 4)
    # Piernas
    pygame.draw.rect(surf, MARRON, (cx - 14, cy + 15, 12, 30), border_radius=4)
    pygame.draw.rect(surf, MARRON, (cx + 2,  cy + 15, 12, 30), border_radius=4)
    # Arco
    arco_rect = pygame.Rect(cx + 5, cy - 40, 20, 60)
    pygame.draw.arc(surf, MARRON_CLARO, arco_rect, math.pi * 0.3, math.pi * 1.7, 4)
    pygame.draw.line(surf, BEIGE, (cx + 15, cy - 40), (cx + 15, cy + 20), 2)
    guardar(surf, os.path.join(BASE, "Sprite", "Personaje", "arquero.png"))


# ---------------------------------------------------------------------------
# Flecha  (40x8 px)
# ---------------------------------------------------------------------------
def sprite_flecha():
    surf = pygame.Surface((40, 8), pygame.SRCALPHA)
    MARRON = (101, 67, 33)
    NEGRO  = (30,  30, 30)
    pygame.draw.line(surf, MARRON, (0, 4), (35, 4), 3)
    pygame.draw.polygon(surf, NEGRO, [(35, 0), (40, 4), (35, 8)])
    guardar(surf, os.path.join(BASE, "Sprite", "Obstaculos", "flecha.png"))


# ---------------------------------------------------------------------------
# Diana  (90x90 px)
# ---------------------------------------------------------------------------
def sprite_diana():
    r = 45
    surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    cx, cy = r, r
    pygame.draw.circle(surf, (220,  50,  50), (cx, cy), r)
    pygame.draw.circle(surf, (255, 255, 255), (cx, cy), int(r * 0.75))
    pygame.draw.circle(surf, (220,  50,  50), (cx, cy), int(r * 0.50))
    pygame.draw.circle(surf, ( 30,  30,  30), (cx, cy), int(r * 0.25))
    pygame.draw.circle(surf, ( 30,  30,  30), (cx, cy), r, 2)
    guardar(surf, os.path.join(BASE, "Sprite", "Enemigos", "diana.png"))


# ---------------------------------------------------------------------------
# Fondo nivel 1  (960x600)
# ---------------------------------------------------------------------------
def sprite_fondo_n1():
    surf = pygame.Surface((960, 600))
    surf.fill((135, 206, 235))
    pygame.draw.rect(surf, (80, 140, 60), (0, 550, 960, 50))
    pygame.draw.circle(surf, (255, 220, 40), (820, 80), 50)
    for cx2, cy2 in [(200, 70), (500, 50), (700, 90)]:
        for dx in [-30, 0, 30]:
            pygame.draw.circle(surf, (255, 255, 255), (cx2 + dx, cy2), 22)
    guardar(surf, os.path.join(BASE, "Sprite", "Fondos", "fondo_nivel1.png"))


# ---------------------------------------------------------------------------
# Fondo nivel 2
# ---------------------------------------------------------------------------
def sprite_fondo_n2():
    surf = pygame.Surface((960, 600))
    surf.fill((90, 140, 200))
    pygame.draw.rect(surf, (60, 110, 40), (0, 550, 960, 50))
    pygame.draw.circle(surf, (255, 220, 40), (820, 80), 50)
    guardar(surf, os.path.join(BASE, "Sprite", "Fondos", "fondo_nivel2.png"))


# ---------------------------------------------------------------------------
# Fondo nivel 3 (noche)
# ---------------------------------------------------------------------------
def sprite_fondo_n3():
    surf = pygame.Surface((960, 600))
    surf.fill((40, 40, 80))
    pygame.draw.rect(surf, (30, 60, 30), (0, 550, 960, 50))
    pygame.draw.circle(surf, (200, 200, 200), (820, 80), 40)
    pygame.draw.circle(surf, (40, 40, 80),    (835, 68), 32)
    for _ in range(60):
        import random
        sx = random.randint(0, 960)
        sy = random.randint(0, 350)
        pygame.draw.circle(surf, (255, 255, 255), (sx, sy), 1)
    guardar(surf, os.path.join(BASE, "Sprite", "Fondos", "fondo_nivel3.png"))


if __name__ == "__main__":
    print("Generando sprites...")
    sprite_arquero()
    sprite_flecha()
    sprite_diana()
    sprite_fondo_n1()
    sprite_fondo_n2()
    sprite_fondo_n3()
    print("Listo.")
    pygame.quit()
