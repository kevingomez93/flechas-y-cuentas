import pygame
import math
import random

from lib.Color import (
    NEGRO, BLANCO, AMARILLO, GRIS, GRIS_CLARO, ROJO, VERDE,
    HUD_FONDO, HUD_TEXTO, HUD_BORDE, MARRON, MARRON_CLARO,
    CELESTE, VERDE_OSCURO, ROJO_OSCURO, NARANJA, AZUL_CLARO
)
from lib.Var import (
    ANCHO, ALTO, FPS, TITULO,
    ESTADO_MENU, ESTADO_JUEGO, ESTADO_NIVEL_OK,
    ESTADO_GAME_OVER, ESTADO_VICTORIA, ESTADO_CREDITOS,
    ACIERTOS_NIVEL, VIDAS, TOTAL_NIVELES,
    PUNTOS_CORRECTO, PUNTOS_BONUS_T, PUNTOS_FALLO, PUNTOS_ERRAR,
    BLANCOS_POR_RON, VEL_ANGULO
)
from lib.Entidades import Arquero, Flecha, Blanco, generar_blancos
from lib.Niveles import ConfigNivel, obtener_nivel, nueva_operacion


# ---------------------------------------------------------------------------
# Fuentes (se inicializan en Core.iniciar)
# ---------------------------------------------------------------------------
_fuentes: dict = {}


def _f(clave: str) -> pygame.font.Font:
    return _fuentes[clave]


def _init_fuentes():
    _fuentes["titulo"]   = pygame.font.SysFont("Arial", 56, bold=True)
    _fuentes["grande"]   = pygame.font.SysFont("Arial", 38, bold=True)
    _fuentes["normal"]   = pygame.font.SysFont("Arial", 28)
    _fuentes["pequeño"]  = pygame.font.SysFont("Arial", 22)
    _fuentes["hud"]      = pygame.font.SysFont("Courier", 24, bold=True)
    _fuentes["enunciado"]= pygame.font.SysFont("Arial", 34, bold=True)


# ---------------------------------------------------------------------------
# Dibujo de escenario
# ---------------------------------------------------------------------------

def _dibujar_fondo(pantalla: pygame.Surface, color_cielo: tuple, num_nivel: int):
    pantalla.fill(color_cielo)

    # Sol o luna segun nivel
    if num_nivel < 3:
        pygame.draw.circle(pantalla, AMARILLO, (820, 80), 50)
    else:
        pygame.draw.circle(pantalla, GRIS_CLARO, (820, 80), 40)
        pygame.draw.circle(pantalla, color_cielo, (835, 68), 32)  # mordida de luna

    # Nubes simples (nivel 1 y 2)
    if num_nivel < 3:
        for cx, cy in [(200, 70), (500, 50), (700, 90)]:
            for dx in [-30, 0, 30]:
                pygame.draw.circle(pantalla, BLANCO, (cx + dx, cy), 22)

    # Suelo con cesped
    pygame.draw.rect(pantalla, (80, 140, 60), (0, ALTO - 50, ANCHO, 50))
    pygame.draw.rect(pantalla, (60, 110, 40), (0, ALTO - 52, ANCHO, 6))

    # Valla de madera decorativa
    for vx in range(0, ANCHO, 60):
        pygame.draw.rect(pantalla, MARRON_CLARO, (vx + 5, ALTO - 90, 10, 45), border_radius=3)
    pygame.draw.rect(pantalla, MARRON, (0, ALTO - 80, ANCHO, 8))

    # Montañas de fondo
    puntos_mont = [(0, ALTO - 50), (150, ALTO - 200), (300, ALTO - 100),
                   (450, ALTO - 220), (600, ALTO - 130), (750, ALTO - 210),
                   (ANCHO, ALTO - 140), (ANCHO, ALTO - 50)]
    color_mont = tuple(max(0, c - 40) for c in color_cielo)
    pygame.draw.polygon(pantalla, color_mont, puntos_mont)


def _dibujar_indicador_viento(pantalla: pygame.Surface, viento: float, x: int, y: int):
    if viento == 0.0:
        texto = _f("pequeño").render("Sin viento", True, HUD_TEXTO)
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
    texto = _f("pequeño").render(f"Viento {desc} {flecha}", True, AMARILLO)
    pantalla.blit(texto, (x, y))


# ---------------------------------------------------------------------------
# HUD principal
# ---------------------------------------------------------------------------

def _dibujar_hud(pantalla: pygame.Surface, puntaje: int, nivel_num: int,
                 flechas: int, aciertos: int, enunciado: str,
                 tiempo_restante: int, viento: float):
    # Barra superior
    pygame.draw.rect(pantalla, HUD_FONDO, (0, 0, ANCHO, 90))
    pygame.draw.line(pantalla, HUD_BORDE, (0, 90), (ANCHO, 90), 2)

    # Enunciado centrado
    surf_e = _f("enunciado").render(enunciado, True, AMARILLO)
    rect_e = surf_e.get_rect(center=(ANCHO // 2, 45))
    pantalla.blit(surf_e, rect_e)

    # Puntaje
    pantalla.blit(_f("hud").render(f"Puntaje: {puntaje}", True, HUD_TEXTO), (15, 10))

    # Nivel
    pantalla.blit(_f("hud").render(f"Nivel {nivel_num}/{TOTAL_NIVELES}", True, HUD_TEXTO), (15, 40))

    # Flechas restantes (iconos)
    pantalla.blit(_f("hud").render("Flechas:", True, HUD_TEXTO), (15, 65))
    for i in range(flechas):
        pygame.draw.line(pantalla, MARRON_CLARO, (130 + i * 14, 78), (140 + i * 14, 72), 3)

    # Aciertos
    pantalla.blit(_f("hud").render(f"Aciertos: {aciertos}/{ACIERTOS_NIVEL}", True, HUD_TEXTO),
                  (ANCHO - 250, 10))

    # Tiempo
    color_t = VERDE if tiempo_restante > 8 else NARANJA if tiempo_restante > 4 else ROJO
    pantalla.blit(_f("hud").render(f"Tiempo: {tiempo_restante}s", True, color_t),
                  (ANCHO - 250, 40))

    # Viento
    _dibujar_indicador_viento(pantalla, viento, ANCHO - 250, 66)


# ---------------------------------------------------------------------------
# Pantallas auxiliares
# ---------------------------------------------------------------------------

def _pantalla_con_fondo_oscuro(pantalla: pygame.Surface):
    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 170))
    pantalla.blit(s, (0, 0))


def _centrar_texto(pantalla, fuente, texto, y, color=BLANCO):
    surf = fuente.render(texto, True, color)
    rect = surf.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(surf, rect)


def _dibujar_menu(pantalla: pygame.Surface, fondo_cache: pygame.Surface):
    pantalla.blit(fondo_cache, (0, 0))
    _pantalla_con_fondo_oscuro(pantalla)

    _centrar_texto(pantalla, _f("titulo"), "ARQUERIA EDUCATIVA", 140, AMARILLO)
    _centrar_texto(pantalla, _f("normal"), "Resuelve operaciones matematicas", 220, BLANCO)
    _centrar_texto(pantalla, _f("normal"), "disparando al blanco con la respuesta correcta.", 255, BLANCO)

    pygame.draw.rect(pantalla, VERDE_OSCURO, (ANCHO//2 - 120, 320, 240, 55), border_radius=12)
    pygame.draw.rect(pantalla, AMARILLO,     (ANCHO//2 - 120, 320, 240, 55), border_radius=12, width=2)
    _centrar_texto(pantalla, _f("grande"), "JUGAR", 347, BLANCO)

    pygame.draw.rect(pantalla, HUD_FONDO,  (ANCHO//2 - 120, 395, 240, 55), border_radius=12)
    pygame.draw.rect(pantalla, AMARILLO,   (ANCHO//2 - 120, 395, 240, 55), border_radius=12, width=2)
    _centrar_texto(pantalla, _f("grande"), "CREDITOS", 422, BLANCO)

    _centrar_texto(pantalla, _f("pequeño"), "[ ENTER o clic para continuar ]", 480, GRIS_CLARO)
    _centrar_texto(pantalla, _f("pequeño"), "Controles: mantener ↑↓ angulo  |  ESPACIO cargar y disparar  |  ESC salir", 520, GRIS)


def _dibujar_nivel_ok(pantalla: pygame.Surface, nivel_num: int, puntaje: int):
    _pantalla_con_fondo_oscuro(pantalla)
    _centrar_texto(pantalla, _f("titulo"), f"¡Nivel {nivel_num} superado!", ALTO // 2 - 80, AMARILLO)
    _centrar_texto(pantalla, _f("grande"), f"Puntaje: {puntaje}", ALTO // 2, BLANCO)
    _centrar_texto(pantalla, _f("normal"), "Presiona ENTER para continuar", ALTO // 2 + 70, GRIS_CLARO)


def _dibujar_game_over(pantalla: pygame.Surface, puntaje: int):
    _pantalla_con_fondo_oscuro(pantalla)
    _centrar_texto(pantalla, _f("titulo"), "GAME OVER", ALTO // 2 - 80, ROJO)
    _centrar_texto(pantalla, _f("grande"), f"Puntaje final: {puntaje}", ALTO // 2, BLANCO)
    _centrar_texto(pantalla, _f("normal"), "Presiona ENTER para volver al menu", ALTO // 2 + 70, GRIS_CLARO)


def _dibujar_victoria(pantalla: pygame.Surface, puntaje: int):
    _pantalla_con_fondo_oscuro(pantalla)
    _centrar_texto(pantalla, _f("titulo"), "¡VICTORIA!", ALTO // 2 - 100, AMARILLO)
    _centrar_texto(pantalla, _f("grande"), "Completaste los 3 niveles", ALTO // 2 - 30, VERDE)
    _centrar_texto(pantalla, _f("grande"), f"Puntaje total: {puntaje}", ALTO // 2 + 40, BLANCO)
    _centrar_texto(pantalla, _f("normal"), "Presiona ENTER para volver al menu", ALTO // 2 + 110, GRIS_CLARO)


# ---------------------------------------------------------------------------
# Estado de juego por nivel
# ---------------------------------------------------------------------------

class EstadoJuego:
    def __init__(self, config: ConfigNivel, puntaje_acumulado: int):
        self.config     = config
        self.puntaje    = puntaje_acumulado
        self.flechas    = config.flechas
        self.aciertos   = 0
        self.arquero    = Arquero()
        self.flecha_act: Flecha | None = None
        self.blancos:   list[Blanco] = []
        self.enunciado  = ""
        self.respuesta  = 0
        self.timer_ronda= config.tiempo_ronda * FPS   # en frames
        self.mensaje    = ""
        self.msg_timer  = 0
        self.terminado  = False   # True cuando se cumplen los aciertos o flechas == 0
        self.derrota    = False   # True si se queda sin flechas antes de los aciertos
        self._nueva_ronda()

    def _nueva_ronda(self):
        self.enunciado, self.respuesta = nueva_operacion(self.config)
        self.blancos = generar_blancos(
            self.respuesta,
            BLANCOS_POR_RON,
            vel_x=self.config.vel_x_blancos,
            vel_y=self.config.vel_y_blancos,
        )
        self.flecha_act = None
        self.timer_ronda = self.config.tiempo_ronda * FPS

    def _mostrar_mensaje(self, texto: str):
        self.mensaje   = texto
        self.msg_timer = FPS * 2   # 2 segundos

    def actualizar(self):
        if self.terminado:
            return

        # Control continuo de angulo mientras no hay flecha en vuelo
        if self.flecha_act is None:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_UP]:
                self.arquero.ajustar_angulo(-VEL_ANGULO)
            elif teclas[pygame.K_DOWN]:
                self.arquero.ajustar_angulo(VEL_ANGULO)

        self.arquero.actualizar()

        # Timer de ronda
        if self.timer_ronda > 0:
            self.timer_ronda -= 1
        elif not self.flecha_act:
            # Tiempo agotado sin flecha en vuelo
            self._mostrar_mensaje("¡Tiempo agotado!")
            self.flechas = max(0, self.flechas - 1)
            if self.flechas == 0:
                self.terminado = True
                self.derrota   = True
                return
            self._nueva_ronda()

        # Mensaje temporal
        if self.msg_timer > 0:
            self.msg_timer -= 1

        # Actualizar blancos
        for b in self.blancos:
            b.actualizar()
        self.blancos = [b for b in self.blancos if b.activo]

        # Si todos los blancos salieron sin ser golpeados → nueva ronda
        if not self.blancos and self.flecha_act is None:
            self._mostrar_mensaje("¡Se escaparon!")
            self.flechas = max(0, self.flechas - 1)
            if self.flechas == 0:
                self.terminado = True
                self.derrota   = True
                return
            self._nueva_ronda()

        # Actualizar flecha
        if self.flecha_act:
            self.flecha_act.actualizar(self.config.viento)
            if not self.flecha_act.activa:
                # Flecha salio de pantalla sin acertar
                self.puntaje   = max(0, self.puntaje + PUNTOS_ERRAR)
                self.flechas   = max(0, self.flechas - 1)
                self._mostrar_mensaje(f"Fallaste! {PUNTOS_ERRAR} pts")
                self.flecha_act = None
                if self.flechas == 0:
                    self.terminado = True
                    self.derrota   = True
                return

            # Colisiones flecha-blancos
            self._verificar_colision()

    def _verificar_colision(self):
        if not self.flecha_act:
            return
        fr = self.flecha_act.rect
        for b in self.blancos:
            if b.activo and not b.golpeado:
                # Colision circular (mas precisa que rect-rect)
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
                        self._mostrar_mensaje(f"¡Correcto! +{ganados} pts")
                        if self.aciertos >= ACIERTOS_NIVEL:
                            self.terminado = True
                        else:
                            # Esperar a que desaparezca la animacion y generar nueva ronda
                            pygame.time.wait(400)
                            self._nueva_ronda()
                    else:
                        self.puntaje = max(0, self.puntaje + PUNTOS_FALLO)
                        self.flechas = max(0, self.flechas - 1)
                        self._mostrar_mensaje(f"Incorrecto! {PUNTOS_FALLO} pts")
                        if self.flechas == 0:
                            self.terminado = True
                            self.derrota   = True
                        else:
                            pygame.time.wait(300)
                            self._nueva_ronda()
                    return

    def procesar_evento(self, evento: pygame.event.Event):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                self.arquero.iniciar_carga()
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_SPACE:
                if self.flecha_act is None and not self.terminado:
                    flecha = self.arquero.liberar()
                    if flecha:
                        self.flecha_act = flecha

    def dibujar(self, pantalla: pygame.Surface):
        # Blancos
        for b in self.blancos:
            b.dibujar(pantalla)

        # Guia de trayectoria (solo cuando no hay flecha en vuelo)
        if self.flecha_act is None and not self.terminado:
            alpha = 180 if self.arquero.cargando else 70
            puntos = self.arquero.puntos_trayectoria(self.config.viento)
            s_guia = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            for i, (px, py) in enumerate(puntos):
                radio = 3 if self.arquero.cargando else 2
                a_punto = max(20, alpha - i * 2)
                pygame.draw.circle(s_guia, (255, 255, 100, a_punto), (px, py), radio)
            pantalla.blit(s_guia, (0, 0))

        # Flecha
        if self.flecha_act:
            self.flecha_act.dibujar(pantalla)

        # Arquero
        self.arquero.dibujar(pantalla)

        # HUD
        t_restante = max(0, self.timer_ronda // FPS)
        _dibujar_hud(pantalla, self.puntaje, self.config.numero,
                     self.flechas, self.aciertos, self.enunciado,
                     t_restante, self.config.viento)

        # Mensaje flotante
        if self.msg_timer > 0:
            alpha = min(255, self.msg_timer * 6)
            color = VERDE if "Correcto" in self.mensaje else ROJO if "Incorrecto" in self.mensaje else AMARILLO
            surf = _f("grande").render(self.mensaje, True, color)
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(ANCHO // 2, ALTO // 2 - 60))
            pantalla.blit(surf, rect)

        # Instrucciones en pantalla
        inst = _f("pequeño").render("Mantener ↑↓ = angulo  |  ESPACIO = cargar y disparar  |  ESC = menu", True, GRIS)
        pantalla.blit(inst, inst.get_rect(center=(ANCHO // 2, ALTO - 20)))


# ---------------------------------------------------------------------------
# Bucle principal
# ---------------------------------------------------------------------------

class Core:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj    = pygame.time.Clock()
        self.estado   = ESTADO_MENU
        self.nivel_actual = 1
        self.puntaje_total = 0
        self.estado_juego: EstadoJuego | None = None

        # Cache del fondo de menu (nivel 1 por defecto)
        self._fondo_menu = pygame.Surface((ANCHO, ALTO))
        _dibujar_fondo(self._fondo_menu, obtener_nivel(1).color_cielo, 1)

    def iniciar(self):
        _init_fuentes()
        self._fondo_menu = pygame.Surface((ANCHO, ALTO))
        _dibujar_fondo(self._fondo_menu, obtener_nivel(1).color_cielo, 1)
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

    def _manejar_menu(self, evento: pygame.event.Event):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            self._iniciar_juego()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos
            # Boton JUGAR
            if ANCHO//2 - 120 <= mx <= ANCHO//2 + 120 and 320 <= my <= 375:
                self._iniciar_juego()
            # Boton CREDITOS
            elif ANCHO//2 - 120 <= mx <= ANCHO//2 + 120 and 395 <= my <= 450:
                self.estado = ESTADO_CREDITOS

    def _manejar_transicion(self, evento: pygame.event.Event):
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
                # Game over o Victoria → volver al menu
                self.estado = ESTADO_MENU
                self.nivel_actual  = 1
                self.puntaje_total = 0
                self.estado_juego  = None

    def _manejar_creditos(self, evento: pygame.event.Event):
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.estado = ESTADO_MENU

    def _iniciar_juego(self):
        self.nivel_actual  = 1
        self.puntaje_total = 0
        config = obtener_nivel(self.nivel_actual)
        self.estado_juego  = EstadoJuego(config, 0)
        self.estado        = ESTADO_JUEGO

    def _actualizar(self):
        if self.estado == ESTADO_JUEGO and self.estado_juego:
            self.estado_juego.actualizar()
            if self.estado_juego.terminado:
                self.puntaje_total = self.estado_juego.puntaje
                if self.estado_juego.derrota:
                    self.estado = ESTADO_GAME_OVER
                else:
                    if self.nivel_actual >= TOTAL_NIVELES:
                        self.estado = ESTADO_VICTORIA
                    else:
                        self.estado = ESTADO_NIVEL_OK

    def _dibujar(self):
        config_n = obtener_nivel(self.nivel_actual)

        if self.estado == ESTADO_MENU:
            _dibujar_menu(self.pantalla, self._fondo_menu)

        elif self.estado == ESTADO_JUEGO and self.estado_juego:
            _dibujar_fondo(self.pantalla, config_n.color_cielo, self.nivel_actual)
            self.estado_juego.dibujar(self.pantalla)

        elif self.estado == ESTADO_NIVEL_OK:
            _dibujar_fondo(self.pantalla, config_n.color_cielo, self.nivel_actual)
            _dibujar_nivel_ok(self.pantalla, self.nivel_actual, self.puntaje_total)

        elif self.estado == ESTADO_GAME_OVER:
            _dibujar_fondo(self.pantalla, config_n.color_cielo, self.nivel_actual)
            _dibujar_game_over(self.pantalla, self.puntaje_total)

        elif self.estado == ESTADO_VICTORIA:
            _dibujar_fondo(self.pantalla, obtener_nivel(TOTAL_NIVELES).color_cielo, TOTAL_NIVELES)
            _dibujar_victoria(self.pantalla, self.puntaje_total)

        elif self.estado == ESTADO_CREDITOS:
            from Creditos import dibujar_creditos
            _dibujar_fondo(self.pantalla, obtener_nivel(1).color_cielo, 1)
            dibujar_creditos(self.pantalla, _fuentes)

        pygame.display.flip()
