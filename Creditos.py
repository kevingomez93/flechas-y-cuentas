"""
Creditos.py - Informacion del juego y autores.
Se invoca desde Core cuando el estado es ESTADO_CREDITOS.
"""
import pygame

from lib.Color import NEGRO, BLANCO, AMARILLO, GRIS, GRIS_CLARO, HUD_FONDO, HUD_BORDE
from lib.Var import ANCHO, ALTO


def dibujar_creditos(pantalla: pygame.Surface, fuentes: dict):
    """Dibuja la pantalla de creditos sobre el fondo actual."""
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 185))
    pantalla.blit(s, (0, 0))

    def centrar(fuente_key, texto, y, color=BLANCO):
        surf = fuentes[fuente_key].render(texto, True, color)
        rect = surf.get_rect(center=(ANCHO // 2, y))
        pantalla.blit(surf, rect)

    centrar("titulo",  "FLECHAS Y CUENTAS",           100, AMARILLO)
    centrar("normal",  "Trabajo Practico Integrador  - Programacion 2", 170, GRIS_CLARO)

    # Linea separadora
    pygame.draw.line(pantalla, HUD_BORDE, (ANCHO//2 - 300, 200), (ANCHO//2 + 300, 200), 2)

    # Autores
    centrar("grande",  "Autores", 240, AMARILLO)
    centrar("normal",  "Franco Fernandez Sica  -  Kevin Gomez", 285, BLANCO)
    centrar("pequeño", "Programacion 2   |   Comision B   |   Grupo: 14   |   Año: 2026", 325, GRIS_CLARO)

    pygame.draw.line(pantalla, HUD_BORDE, (ANCHO//2 - 300, 360), (ANCHO//2 + 300, 360), 2)

    # Descripcion educativa
    centrar("grande",  "Objetivo educativo", 395, AMARILLO)
    centrar("normal",  "Practicar calculo mental mediante mecanicas de flechas.", 435, BLANCO)
    centrar("pequeño", "El jugador entrena suma, resta, multiplicacion y division", 465, GRIS_CLARO)
    centrar("pequeño", "mientras comprende el concepto de angulo y trayectoria.", 492, GRIS_CLARO)

    pygame.draw.line(pantalla, HUD_BORDE, (ANCHO//2 - 300, 520), (ANCHO//2 + 300, 520), 2)

    centrar("pequeño", "Desarrollado con Python 3 y pygame-ce  |  2026", 545, GRIS)
    centrar("pequeño", "[ ENTER o ESC para volver al menu ]", 575, GRIS)
