import pygame
import math
import random

from lib.colores import (
    NEGRO, BLANCO, AMARILLO, GRIS, GRIS_CLARO, ROJO, VERDE,
    HUD_FONDO, HUD_TEXTO, HUD_BORDE, MARRON_CLARO,
    VERDE_OSCURO, ROJO_OSCURO, NARANJA
)
from lib.variables import (
    ANCHO, ALTO, FPS, TITULO,
    ESTADO_MENU, ESTADO_JUEGO, ESTADO_NIVEL_OK,
    ESTADO_GAME_OVER, ESTADO_VICTORIA, ESTADO_CREDITOS,
    ACIERTOS_NIVEL, TOTAL_NIVELES,
    PUNTOS_CORRECTO, PUNTOS_BONUS_T, PUNTOS_FALLO, PUNTOS_ERRAR,
    BLANCOS_POR_RON, VEL_ANGULO
)
from lib.entidades import Arquero, Flecha, Blanco, generar_blancos
from lib.niveles import ConfigNivel, obtener_nivel, nueva_operacion
from lib.imagenes import cargar_fondo
from lib.sonido import init_audio, reproducir, reproducir_musica, toggle_musica, musica_prendida


_fuentes = {}


def _init_fuentes():
    # fuentes que uso en todo el juego
    _fuentes["titulo"] = pygame.font.SysFont("Arial", 56, bold=True)
    _fuentes["grande"] = pygame.font.SysFont("Arial", 38, bold=True)
    _fuentes["normal"] = pygame.font.SysFont("Arial", 28)
    _fuentes["pequeño"] = pygame.font.SysFont("Arial", 22)
    _fuentes["hud"] = pygame.font.SysFont("Courier", 24, bold=True)
    _fuentes["enunciado"] = pygame.font.SysFont("Arial", 34, bold=True)


def _fuente(clave):
    return _fuentes[clave]


def _dibujar_fondo(pantalla, num_nivel):
    # pongo el fondo del nivel
    fondo = cargar_fondo(num_nivel, ANCHO, ALTO)
    pantalla.blit(fondo, (0, 0))


def _dibujar_indicador_viento(pantalla, viento, x, y):
    if viento == 0.0:
        texto = _fuente("pequeño").render("Sin viento", True, HUD_TEXTO)
        pantalla.blit(texto, (x, y))
        return
    flecha = ">>> " if viento > 0 else " <<<"
    intensidad = abs(viento)
    if intensidad < 0.01:
        desc = "leve"
    elif intensidad < 0.02:
        desc = "moderado"
    else:
        desc = "fuerte"
    texto = _fuente("pequeño").render(f"Viento {desc} {flecha}", True, AMARILLO)
    pantalla.blit(texto, (x, y))


def _dibujar_hud(pantalla, puntaje, nivel_num, flechas, aciertos, enunciado, tiempo_restante, viento):
    # barra de arriba con puntaje, nivel, tiempo, etc
    pygame.draw.rect(pantalla, HUD_FONDO, (0, 0, ANCHO, 90))
    pygame.draw.line(pantalla, HUD_BORDE, (0, 90), (ANCHO, 90), 2)

    surf_e = _fuente("enunciado").render(enunciado, True, AMARILLO)
    rect_e = surf_e.get_rect(center=(ANCHO // 2, 45))
    pantalla.blit(surf_e, rect_e)

    pantalla.blit(_fuente("hud").render(f"Puntaje: {puntaje}", True, HUD_TEXTO), (15, 10))
    pantalla.blit(_fuente("hud").render(f"Nivel {nivel_num}/{TOTAL_NIVELES}", True, HUD_TEXTO), (15, 40))

    pantalla.blit(_fuente("hud").render("Flechas:", True, HUD_TEXTO), (15, 65))
    for i in range(flechas):
        pygame.draw.line(pantalla, MARRON_CLARO, (130 + i * 14, 78), (140 + i * 14, 72), 3)

    pantalla.blit(_fuente("hud").render(f"Aciertos: {aciertos}/{ACIERTOS_NIVEL}", True, HUD_TEXTO),
                  (ANCHO - 250, 10))

    color_t = VERDE if tiempo_restante > 8 else NARANJA if tiempo_restante > 4 else ROJO
    pantalla.blit(_fuente("hud").render(f"Tiempo: {tiempo_restante}s", True, color_t),
                  (ANCHO - 250, 40))

    _dibujar_indicador_viento(pantalla, viento, ANCHO - 250, 66)


def _pantalla_oscura(pantalla):
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 170))
    pantalla.blit(s, (0, 0))


def _centrar_texto(pantalla, fuente, texto, y, color=BLANCO):
    surf = fuente.render(texto, True, color)
    rect = surf.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(surf, rect)


def _dibujar_menu(pantalla, fondo_cache):
    # menu principal con los botones
    pantalla.blit(fondo_cache, (0, 0))
    _pantalla_oscura(pantalla)

    _centrar_texto(pantalla, _fuente("titulo"), "FLECHAS Y CUENTAS", 140, AMARILLO)
    _centrar_texto(pantalla, _fuente("normal"), "Resolve cuentas y disparale al blanco correcto", 230, BLANCO)

    # boton jugar
    pygame.draw.rect(pantalla, VERDE_OSCURO, (ANCHO//2 - 120, 320, 240, 55), border_radius=12)
    pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 120, 320, 240, 55), border_radius=12, width=2)
    _centrar_texto(pantalla, _fuente("grande"), "JUGAR", 347, BLANCO)

    # boton creditos
    pygame.draw.rect(pantalla, HUD_FONDO, (ANCHO//2 - 120, 395, 240, 55), border_radius=12)
    pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 120, 395, 240, 55), border_radius=12, width=2)
    _centrar_texto(pantalla, _fuente("grande"), "CREDITOS", 422, BLANCO)

    # boton para prender/apagar musica
    estado_musica = "ON" if musica_prendida() else "OFF"
    pygame.draw.rect(pantalla, VERDE_OSCURO if musica_prendida() else ROJO_OSCURO,
                     (ANCHO//2 - 120, 470, 240, 55), border_radius=12)
    pygame.draw.rect(pantalla, AMARILLO, (ANCHO//2 - 120, 470, 240, 55), border_radius=12, width=2)
    _centrar_texto(pantalla, _fuente("grande"), f"MUSICA: {estado_musica}", 497, BLANCO)

    _centrar_texto(pantalla, _fuente("pequeño"), "ENTER o clic para continuar", 555, GRIS_CLARO)
    _centrar_texto(pantalla, _fuente("pequeño"), "↑↓ angulo  |  ESPACIO cargar/disparar  |  M musica  |  ESC salir", 585, GRIS)


def _dibujar_nivel_ok(pantalla, nivel_num, puntaje):
    _pantalla_oscura(pantalla)
    _centrar_texto(pantalla, _fuente("titulo"), f"Nivel {nivel_num} superado", ALTO // 2 - 80, AMARILLO)
    _centrar_texto(pantalla, _fuente("grande"), f"Puntaje: {puntaje}", ALTO // 2, BLANCO)
    _centrar_texto(pantalla, _fuente("normal"), "Presiona ENTER para continuar", ALTO // 2 + 70, GRIS_CLARO)


def _dibujar_game_over(pantalla, puntaje):
    _pantalla_oscura(pantalla)
    _centrar_texto(pantalla, _fuente("titulo"), "GAME OVER", ALTO // 2 - 80, ROJO)
    _centrar_texto(pantalla, _fuente("grande"), f"Puntaje final: {puntaje}", ALTO // 2, BLANCO)
    _centrar_texto(pantalla, _fuente("normal"), "Presiona ENTER para volver al menu", ALTO // 2 + 70, GRIS_CLARO)


def _dibujar_victoria(pantalla, puntaje):
    _pantalla_oscura(pantalla)
    _centrar_texto(pantalla, _fuente("titulo"), "VICTORIA", ALTO // 2 - 100, AMARILLO)
    _centrar_texto(pantalla, _fuente("grande"), "Completaste los 3 niveles", ALTO // 2 - 30, VERDE)
    _centrar_texto(pantalla, _fuente("grande"), f"Puntaje total: {puntaje}", ALTO // 2 + 40, BLANCO)
    _centrar_texto(pantalla, _fuente("normal"), "Presiona ENTER para volver al menu", ALTO // 2 + 110, GRIS_CLARO)


class EstadoJuego:
    def __init__(self, config, puntaje_acumulado):
        self.config = config
        self.puntaje = puntaje_acumulado
        self.flechas = config.flechas
        self.aciertos = 0
        self.arquero = Arquero()
        self.flecha_act = None
        self.blancos = []
        self.enunciado = ""
        self.respuesta = 0
        self.timer_ronda = config.tiempo_ronda * FPS
        self.mensaje = ""
        self.msg_timer = 0
        self.terminado = False
        self.derrota = False
        self.pausa = 0
        self._nueva_ronda()  # arranca la primer ronda

    def _nueva_ronda(self):
        self.enunciado, self.respuesta = nueva_operacion(self.config)
        self.blancos = generar_blancos(
            self.respuesta,
            BLANCOS_POR_RON,
            vel_x=self.config.vel_x_blancos,
            vel_y=self.config.vel_y_blancos,
            bob_amp=self.config.bob,
        )
        self.flecha_act = None
        self.timer_ronda = self.config.tiempo_ronda * FPS

    def _mostrar_mensaje(self, texto):
        self.mensaje = texto
        self.msg_timer = FPS * 2

    def actualizar(self):
        if self.terminado:
            return

        if self.pausa > 0:
            self.pausa -= 1
            if self.pausa == 0 and not self.terminado:
                self._nueva_ronda()
            return

        # controles del arquero
        if self.flecha_act is None:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_UP]:
                self.arquero.ajustar_angulo(-VEL_ANGULO)
            elif teclas[pygame.K_DOWN]:
                self.arquero.ajustar_angulo(VEL_ANGULO)

        self.arquero.actualizar()

        # cuenta regresiva de la ronda
        if self.timer_ronda > 0:
            self.timer_ronda -= 1
        elif not self.flecha_act:
            self._mostrar_mensaje("Tiempo agotado")
            reproducir("fallo")
            self.flechas = max(0, self.flechas - 1)
            if self.flechas == 0:
                self.terminado = True
                self.derrota = True
                return
            self._nueva_ronda()

        if self.msg_timer > 0:
            self.msg_timer -= 1

        for b in self.blancos:
            b.actualizar()
        self.blancos = [b for b in self.blancos if b.activo]

        if not self.blancos and self.flecha_act is None:
            self._mostrar_mensaje("Se escaparon")
            reproducir("fallo")
            self.flechas = max(0, self.flechas - 1)
            if self.flechas == 0:
                self.terminado = True
                self.derrota = True
                return
            self._nueva_ronda()

        if self.flecha_act:
            self.flecha_act.actualizar(self.config.viento)
            if not self.flecha_act.activa:
                self.puntaje = max(0, self.puntaje + PUNTOS_ERRAR)
                self.flechas = max(0, self.flechas - 1)
                reproducir("fallo")
                self._mostrar_mensaje(f"Fallaste {PUNTOS_ERRAR} pts")
                self.flecha_act = None
                if self.flechas == 0:
                    self.terminado = True
                    self.derrota = True
                return

            self._verificar_colision()

    def _verificar_colision(self):
        # veo si la flecha pego en algun blanco
        if not self.flecha_act:
            return
        for b in self.blancos:
            if b.activo and not b.golpeado:
                dx = self.flecha_act.x - b.x
                dy = self.flecha_act.y - b.y
                distancia = math.sqrt(dx * dx + dy * dy)
                if distancia < b.radio:
                    b.registrar_impacto()
                    self.flecha_act.activa = False
                    self.flecha_act = None
                    if b.es_correcto:
                        bonus = int(self.timer_ronda / FPS) * PUNTOS_BONUS_T
                        ganados = PUNTOS_CORRECTO + bonus
                        self.puntaje += ganados
                        self.aciertos += 1
                        reproducir("acierto")
                        self._mostrar_mensaje(f"Correcto +{ganados} pts")
                        if self.aciertos >= ACIERTOS_NIVEL:
                            self.terminado = True
                        else:
                            self.pausa = int(FPS * 0.4)
                    else:
                        self.puntaje = max(0, self.puntaje + PUNTOS_FALLO)
                        self.flechas = max(0, self.flechas - 1)
                        reproducir("incorrecto")
                        self._mostrar_mensaje(f"Incorrecto {PUNTOS_FALLO} pts")
                        if self.flechas == 0:
                            self.terminado = True
                            self.derrota = True
                        else:
                            self.pausa = int(FPS * 0.3)
                    return

    def procesar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                self.arquero.iniciar_carga()
            elif evento.key == pygame.K_m:
                toggle_musica()
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE:
                if self.flecha_act is None and not self.terminado:
                    flecha = self.arquero.liberar()
                    if flecha:
                        self.flecha_act = flecha
                        reproducir("disparo")

    def dibujar(self, pantalla):
        for b in self.blancos:
            b.dibujar(pantalla)

        if self.flecha_act is None and not self.terminado:
            alpha = 180 if self.arquero.cargando else 70
            puntos = self.arquero.puntos_trayectoria(self.config.viento)
            s_guia = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            for i, (px, py) in enumerate(puntos):
                radio = 3 if self.arquero.cargando else 2
                a_punto = max(20, alpha - i * 2)
                pygame.draw.circle(s_guia, (255, 255, 100, a_punto), (px, py), radio)
            pantalla.blit(s_guia, (0, 0))

        if self.flecha_act:
            self.flecha_act.dibujar(pantalla)

        self.arquero.dibujar(pantalla)

        t_restante = max(0, self.timer_ronda // FPS)
        _dibujar_hud(pantalla, self.puntaje, self.config.numero,
                     self.flechas, self.aciertos, self.enunciado,
                     t_restante, self.config.viento)

        if self.msg_timer > 0:
            alpha = min(255, self.msg_timer * 6)
            if "Correcto" in self.mensaje:
                color = VERDE
            elif "Incorrecto" in self.mensaje:
                color = ROJO
            else:
                color = AMARILLO
            surf = _fuente("grande").render(self.mensaje, True, color)
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(ANCHO // 2, ALTO // 2 - 60))
            pantalla.blit(surf, rect)

        inst = _fuente("pequeño").render("↑↓ angulo  |  ESPACIO cargar/disparar  |  ESC menu", True, GRIS)
        pantalla.blit(inst, inst.get_rect(center=(ANCHO // 2, ALTO - 20)))


class Core:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.estado = ESTADO_MENU
        self.nivel_actual = 1
        self.puntaje_total = 0
        self.estado_juego = None
        self._fondo_menu = None

    def iniciar(self):
        _init_fuentes()
        init_audio()
        reproducir_musica()
        self._fondo_menu = pygame.Surface((ANCHO, ALTO))
        _dibujar_fondo(self._fondo_menu, 1)
        self._loop()

    def _loop(self):
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    if self.estado == ESTADO_JUEGO:
                        self.estado = ESTADO_MENU
                    elif self.estado == ESTADO_CREDITOS:
                        self.estado = ESTADO_MENU
                    else:
                        ejecutando = False

                elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                    toggle_musica()

                elif self.estado == ESTADO_MENU:
                    self._manejar_menu(evento)

                elif self.estado == ESTADO_JUEGO:
                    if self.estado_juego:
                        self.estado_juego.procesar_evento(evento)

                elif self.estado in (ESTADO_NIVEL_OK, ESTADO_GAME_OVER, ESTADO_VICTORIA):
                    self._manejar_transicion(evento)

                elif self.estado == ESTADO_CREDITOS:
                    self._manejar_creditos(evento)

            self._actualizar()
            self._dibujar()
            self.reloj.tick(FPS)

        pygame.quit()

    def _manejar_menu(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                self._iniciar_juego()
            elif evento.key == pygame.K_m:
                toggle_musica()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos
            if ANCHO//2 - 120 <= mx <= ANCHO//2 + 120 and 320 <= my <= 375:
                self._iniciar_juego()
            elif ANCHO//2 - 120 <= mx <= ANCHO//2 + 120 and 395 <= my <= 450:
                self.estado = ESTADO_CREDITOS
            elif ANCHO//2 - 120 <= mx <= ANCHO//2 + 120 and 470 <= my <= 525:
                toggle_musica()

    def _manejar_transicion(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            if self.estado == ESTADO_NIVEL_OK:
                self.nivel_actual += 1
                if self.nivel_actual > TOTAL_NIVELES:
                    self.estado = ESTADO_VICTORIA
                else:
                    config = obtener_nivel(self.nivel_actual)
                    self.estado_juego = EstadoJuego(config, self.puntaje_total)
                    self.estado = ESTADO_JUEGO
            else:
                self.estado = ESTADO_MENU
                self.nivel_actual = 1
                self.puntaje_total = 0
                self.estado_juego = None

    def _manejar_creditos(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.estado = ESTADO_MENU

    def _iniciar_juego(self):
        self.nivel_actual = 1
        self.puntaje_total = 0
        config = obtener_nivel(self.nivel_actual)
        self.estado_juego = EstadoJuego(config, 0)
        self.estado = ESTADO_JUEGO

    def _actualizar(self):
        if self.estado == ESTADO_JUEGO and self.estado_juego:
            self.estado_juego.actualizar()
            if self.estado_juego.terminado:
                self.puntaje_total = self.estado_juego.puntaje
                if self.estado_juego.derrota:
                    self.estado = ESTADO_GAME_OVER
                    reproducir("gameover")
                else:
                    if self.nivel_actual >= TOTAL_NIVELES:
                        self.estado = ESTADO_VICTORIA
                        reproducir("victoria")
                    else:
                        self.estado = ESTADO_NIVEL_OK
                        reproducir("nivel")

    def _dibujar(self):
        config_n = obtener_nivel(self.nivel_actual)

        if self.estado == ESTADO_MENU:
            _dibujar_menu(self.pantalla, self._fondo_menu)

        elif self.estado == ESTADO_JUEGO and self.estado_juego:
            _dibujar_fondo(self.pantalla, self.nivel_actual)
            self.estado_juego.dibujar(self.pantalla)

        elif self.estado == ESTADO_NIVEL_OK:
            _dibujar_fondo(self.pantalla, self.nivel_actual)
            _dibujar_nivel_ok(self.pantalla, self.nivel_actual, self.puntaje_total)

        elif self.estado == ESTADO_GAME_OVER:
            _dibujar_fondo(self.pantalla, self.nivel_actual)
            _dibujar_game_over(self.pantalla, self.puntaje_total)

        elif self.estado == ESTADO_VICTORIA:
            _dibujar_fondo(self.pantalla, TOTAL_NIVELES)
            _dibujar_victoria(self.pantalla, self.puntaje_total)

        elif self.estado == ESTADO_CREDITOS:
            from creditos import dibujar_creditos
            _dibujar_fondo(self.pantalla, 1)
            dibujar_creditos(self.pantalla, _fuentes)

        pygame.display.flip()
