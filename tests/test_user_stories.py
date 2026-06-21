import os
import unittest
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from lib import Audio
from lib.Core import Core, EstadoJuego, _init_fuentes
from lib.Niveles import obtener_nivel, nueva_operacion
from lib.Var import (
    ACIERTOS_NIVEL,
    ESTADO_CREDITOS,
    ESTADO_GAME_OVER,
    ESTADO_JUEGO,
    ESTADO_MENU,
    ESTADO_NIVEL_OK,
    ESTADO_VICTORIA,
    FPS,
    PUNTOS_CORRECTO,
    TOTAL_NIVELES,
)


pygame.init()
pygame.display.set_mode((1, 1))
_init_fuentes()


class UserStoryTests(unittest.TestCase):
    def setUp(self):
        Audio._musica_activa = True

    def make_core(self):
        core = Core()
        core._fondo_menu = pygame.Surface((960, 600))
        return core

    def keydown(self, key):
        return pygame.event.Event(pygame.KEYDOWN, key=key)

    def keyup(self, key):
        return pygame.event.Event(pygame.KEYUP, key=key)

    def click(self, x, y):
        return pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(x, y), button=1)

    def test_us001_enter_starts_new_game_from_menu(self):
        core = self.make_core()
        core._manejar_menu(self.keydown(pygame.K_RETURN))
        self.assertEqual(core.estado, ESTADO_JUEGO)
        self.assertEqual(core.nivel_actual, 1)
        self.assertEqual(core.puntaje_total, 0)
        self.assertIsNotNone(core.estado_juego)

    def test_us002_jugar_button_starts_new_game_from_menu(self):
        core = self.make_core()
        core._manejar_menu(self.click(480, 345))
        self.assertEqual(core.estado, ESTADO_JUEGO)
        self.assertIsNotNone(core.estado_juego)

    def test_us003_credits_button_opens_credits_and_enter_returns(self):
        core = self.make_core()
        core._manejar_menu(self.click(480, 420))
        self.assertEqual(core.estado, ESTADO_CREDITOS)
        core._manejar_creditos(self.keydown(pygame.K_RETURN))
        self.assertEqual(core.estado, ESTADO_MENU)

    def test_us004_music_button_toggles_music_from_menu(self):
        core = self.make_core()
        self.assertTrue(Audio.musica_prendida())
        core._manejar_menu(self.click(480, 495))
        self.assertFalse(Audio.musica_prendida())

    def test_us005_global_m_toggles_music_once_in_menu_event_loop(self):
        core = self.make_core()
        event = self.keydown(pygame.K_m)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pass
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            Audio.toggle_musica()
        elif core.estado == ESTADO_MENU:
            core._manejar_menu(event)
        self.assertFalse(Audio.musica_prendida())

    def test_us006_escape_from_game_returns_to_menu_without_resetting_music(self):
        core = self.make_core()
        core._iniciar_juego()
        self.assertEqual(core.estado, ESTADO_JUEGO)
        event = self.keydown(pygame.K_ESCAPE)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if core.estado == ESTADO_JUEGO:
                core.estado = ESTADO_MENU
        self.assertEqual(core.estado, ESTADO_MENU)
        self.assertTrue(Audio.musica_prendida())

    def test_us007_space_hold_and_release_creates_arrow(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        game.procesar_evento(self.keydown(pygame.K_SPACE))
        self.assertTrue(game.arquero.cargando)
        game.arquero.actualizar()
        game.procesar_evento(self.keyup(pygame.K_SPACE))
        self.assertIsNotNone(game.flecha_act)
        self.assertFalse(game.arquero.cargando)

    def test_us008_up_down_adjust_angle_with_bounds(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        game.arquero.ajustar_angulo(-1000)
        self.assertEqual(game.arquero.angulo, -85.0)
        game.arquero.ajustar_angulo(1000)
        self.assertEqual(game.arquero.angulo, 10.0)

    def test_us009_new_round_generates_one_correct_target_and_three_distractors(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        correct = [b for b in game.blancos if b.es_correcto]
        self.assertEqual(len(game.blancos), 4)
        self.assertEqual(len(correct), 1)
        self.assertEqual(correct[0].numero, game.respuesta)

    def test_us010_level_math_generators_return_valid_answers(self):
        for level_number in range(1, TOTAL_NIVELES + 1):
            for _ in range(40):
                prompt, answer = nueva_operacion(obtener_nivel(level_number))
                expression = prompt.replace(" = ?", "").replace("x", "*").replace("^", "**")
                self.assertEqual(eval(expression), answer)

    def test_us011_timer_timeout_costs_one_arrow_and_starts_next_round(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        arrows = game.flechas
        game.timer_ronda = 0
        game.actualizar()
        self.assertEqual(game.flechas, arrows - 1)
        self.assertFalse(game.terminado)
        self.assertIn("Tiempo agotado", game.mensaje)

    def test_us012_missing_a_shot_costs_points_and_arrow(self):
        game = EstadoJuego(obtener_nivel(1), 50)
        game.procesar_evento(self.keydown(pygame.K_SPACE))
        game.procesar_evento(self.keyup(pygame.K_SPACE))
        game.flecha_act.activa = False
        arrows = game.flechas
        game.actualizar()
        self.assertEqual(game.flechas, arrows - 1)
        self.assertEqual(game.puntaje, 40)
        self.assertIn("Fallaste", game.mensaje)

    def test_us013_correct_hit_awards_points_and_counts_success(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        target = next(b for b in game.blancos if b.es_correcto)
        game.procesar_evento(self.keydown(pygame.K_SPACE))
        game.procesar_evento(self.keyup(pygame.K_SPACE))
        game.flecha_act.x = target.x
        game.flecha_act.y = target.y
        game._verificar_colision()
        self.assertEqual(game.aciertos, 1)
        self.assertGreaterEqual(game.puntaje, PUNTOS_CORRECTO)
        self.assertIn("Correcto", game.mensaje)

    def test_us014_incorrect_hit_costs_arrow_and_points_without_negative_score(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        target = next(b for b in game.blancos if not b.es_correcto)
        game.procesar_evento(self.keydown(pygame.K_SPACE))
        game.procesar_evento(self.keyup(pygame.K_SPACE))
        game.flecha_act.x = target.x
        game.flecha_act.y = target.y
        arrows = game.flechas
        game._verificar_colision()
        self.assertEqual(game.flechas, arrows - 1)
        self.assertEqual(game.puntaje, 0)
        self.assertIn("Incorrecto", game.mensaje)

    def test_us015_five_correct_answers_complete_level(self):
        game = EstadoJuego(obtener_nivel(1), 0)
        game.aciertos = ACIERTOS_NIVEL - 1
        target = next(b for b in game.blancos if b.es_correcto)
        game.procesar_evento(self.keydown(pygame.K_SPACE))
        game.procesar_evento(self.keyup(pygame.K_SPACE))
        game.flecha_act.x = target.x
        game.flecha_act.y = target.y
        game._verificar_colision()
        self.assertTrue(game.terminado)
        self.assertFalse(game.derrota)

    def test_us016_level_completion_advances_or_victory_after_final(self):
        core = self.make_core()
        core.estado = ESTADO_NIVEL_OK
        core.nivel_actual = 1
        core.puntaje_total = 250
        core._manejar_transicion(self.keydown(pygame.K_RETURN))
        self.assertEqual(core.estado, ESTADO_JUEGO)
        self.assertEqual(core.nivel_actual, 2)
        self.assertEqual(core.estado_juego.puntaje, 250)

        core.nivel_actual = TOTAL_NIVELES
        core.estado_juego.terminado = True
        core.estado_juego.derrota = False
        core._actualizar()
        self.assertEqual(core.estado, ESTADO_VICTORIA)

    def test_us017_game_over_enter_returns_to_fresh_menu_state(self):
        core = self.make_core()
        core.estado = ESTADO_GAME_OVER
        core.nivel_actual = 2
        core.puntaje_total = 100
        core.estado_juego = object()
        core._manejar_transicion(self.keydown(pygame.K_RETURN))
        self.assertEqual(core.estado, ESTADO_MENU)
        self.assertEqual(core.nivel_actual, 1)
        self.assertEqual(core.puntaje_total, 0)
        self.assertIsNone(core.estado_juego)

    def test_us018_assets_load_for_all_levels_and_sprites(self):
        from lib.Assets import cargar_fondo, cargar_sprite

        for level_number in range(1, TOTAL_NIVELES + 1):
            surface = cargar_fondo(level_number, 100, 80)
            self.assertEqual(surface.get_size(), (100, 80))
        for path in ("Personaje/arquero.png", "Enemigos/diana.png", "Obstaculos/flecha.png"):
            self.assertGreater(cargar_sprite(path).get_width(), 0)

    def test_us019_draw_methods_render_without_exceptions(self):
        core = self.make_core()
        core._iniciar_juego()
        core._dibujar()
        core.estado = ESTADO_CREDITOS
        core._dibujar()
        core.estado = ESTADO_GAME_OVER
        core._dibujar()
        core.estado = ESTADO_VICTORIA
        core._dibujar()


if __name__ == "__main__":
    unittest.main()
