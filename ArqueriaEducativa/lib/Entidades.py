import pygame
import math
import random

from lib.Color import (
    MARRON, MARRON_CLARO, BEIGE, NEGRO, BLANCO, AMARILLO, ROJO_OSCURO,
    DIANA_ROJO, DIANA_BLANCO, DIANA_NEGRO, VERDE_OSCURO, NARANJA, GRIS
)
from lib.Var import (
    ARQUERO_X, ARQUERO_Y, VEL_BASE, VEL_MAX, TIEMPO_CARGA,
    GRAVEDAD, ANCHO, ALTO, BLANCO_RADIO,
    PREVIEW_PASOS, PREVIEW_SALTO
)


class Arquero:
    """Personaje central controlado por el jugador."""

    def __init__(self):
        self.x = ARQUERO_X
        self.y = ARQUERO_Y
        self.angulo = -15.0          # grados, negativo = apunta hacia arriba
        self.cargando = False
        self.tiempo_carga = 0        # frames sosteniendo ESPACIO
        self.flecha_disparada = False

        # Dimensiones del arquero (dibujado por primitivas)
        self.ancho = 40
        self.alto  = 80

    # --- Control ---
    def ajustar_angulo(self, delta: float):
        self.angulo = max(-85.0, min(10.0, self.angulo + delta))

    def iniciar_carga(self):
        self.cargando = True

    def calcular_potencia(self) -> float:
        """Potencia actual segun el tiempo de carga acumulado."""
        return VEL_BASE + (VEL_MAX - VEL_BASE) * (self.tiempo_carga / TIEMPO_CARGA)

    def liberar(self):
        """Devuelve una Flecha con la fisica calculada, o None si ya hay una activa."""
        if not self.cargando:
            return None
        self.cargando = False
        potencia = self.calcular_potencia()
        self.tiempo_carga = 0
        rad = math.radians(self.angulo)
        vx = potencia * math.cos(rad)
        vy = potencia * math.sin(rad)
        ox = self.x + 30
        oy = self.y - 10
        return Flecha(ox, oy, vx, vy)

    def puntos_trayectoria(self, viento: float = 0.0) -> list:
        """Simula el vuelo con la potencia y angulo actuales; devuelve puntos (x, y)."""
        potencia = self.calcular_potencia()
        rad = math.radians(self.angulo)
        px = float(self.x + 30)
        py = float(self.y - 10)
        vx = potencia * math.cos(rad)
        vy = potencia * math.sin(rad)
        puntos = []
        for paso in range(PREVIEW_PASOS * PREVIEW_SALTO):
            vy += GRAVEDAD
            vx += viento * 0.01
            px += vx
            py += vy
            if px > ANCHO + 50 or py > ALTO + 50 or px < -50:
                break
            if paso % PREVIEW_SALTO == 0:
                puntos.append((int(px), int(py)))
        return puntos

    def actualizar(self):
        if self.cargando:
            self.tiempo_carga = min(self.tiempo_carga + 1, TIEMPO_CARGA)

    def dibujar(self, pantalla: pygame.Surface):
        cx, cy = self.x, self.y

        # Cuerpo (rectangulo redondeado simulado con elipse + rect)
        pygame.draw.rect(pantalla, BEIGE, (cx - 15, cy - 35, 30, 50), border_radius=8)
        # Cabeza
        pygame.draw.circle(pantalla, BEIGE, (cx, cy - 45), 16)
        # Cabello
        pygame.draw.arc(pantalla, MARRON, (cx - 16, cy - 61, 32, 32), 0, math.pi, 4)
        # Piernas
        pygame.draw.rect(pantalla, MARRON, (cx - 14, cy + 15, 12, 30), border_radius=4)
        pygame.draw.rect(pantalla, MARRON, (cx + 2,  cy + 15, 12, 30), border_radius=4)

        # Arco (arco de circulo)
        arco_rect = pygame.Rect(cx + 5, cy - 40, 20, 60)
        pygame.draw.arc(pantalla, MARRON_CLARO, arco_rect, math.pi * 0.3, math.pi * 1.7, 4)

        # Cuerda del arco (linea recta que imita tension)
        if self.cargando and self.tiempo_carga > 0:
            tension = self.tiempo_carga / TIEMPO_CARGA * 10
            pygame.draw.line(pantalla, BEIGE,
                             (cx + 15, cy - 40),
                             (cx + 15 - int(tension), cy),
                             2)
            pygame.draw.line(pantalla, BEIGE,
                             (cx + 15 - int(tension), cy),
                             (cx + 15, cy + 20),
                             2)
        else:
            pygame.draw.line(pantalla, BEIGE, (cx + 15, cy - 40), (cx + 15, cy + 20), 2)

        # Indicador de angulo (linea de mira)
        largo = 55
        rad = math.radians(self.angulo)
        ex = cx + 30 + int(largo * math.cos(rad))
        ey = cy - 10 + int(largo * math.sin(rad))
        pygame.draw.line(pantalla, AMARILLO, (cx + 30, cy - 10), (ex, ey), 2)

        # Barra de potencia
        if self.cargando:
            self._dibujar_barra_potencia(pantalla, cx, cy)

    def _dibujar_barra_potencia(self, pantalla, cx, cy):
        ancho_barra = 60
        alto_barra  = 8
        bx = cx - ancho_barra // 2
        by = cy + 55
        pygame.draw.rect(pantalla, NEGRO, (bx - 1, by - 1, ancho_barra + 2, alto_barra + 2))
        lleno = int(ancho_barra * self.tiempo_carga / TIEMPO_CARGA)
        color = VERDE_OSCURO if lleno < ancho_barra * 0.6 else NARANJA if lleno < ancho_barra * 0.85 else ROJO_OSCURO
        pygame.draw.rect(pantalla, color, (bx, by, lleno, alto_barra))


# ---------------------------------------------------------------------------

class Flecha:
    """Proyectil disparado por el arquero con fisica parabolica."""

    LARGO  = 22
    GROSOR = 3

    def __init__(self, x: float, y: float, vx: float, vy: float):
        self.x   = x
        self.y   = y
        self.vx  = vx
        self.vy  = vy
        self.activa = True

    def aplicar_viento(self, viento: float):
        """viento positivo = hacia la derecha, negativo = izquierda."""
        self.vx += viento

    def actualizar(self, viento: float = 0.0):
        self.vy += GRAVEDAD
        self.vx += viento * 0.01     # aceleracion leve del viento por frame
        self.x  += self.vx
        self.y  += self.vy
        if self.x > ANCHO + 50 or self.y > ALTO + 50 or self.x < -50:
            self.activa = False

    @property
    def angulo_visual(self) -> float:
        """Angulo de la flecha segun su direccion de vuelo."""
        return math.degrees(math.atan2(self.vy, self.vx))

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - 5, self.y - 5, 14, 14)

    def dibujar(self, pantalla: pygame.Surface):
        rad = math.radians(self.angulo_visual)
        dx = math.cos(rad) * self.LARGO
        dy = math.sin(rad) * self.LARGO
        # Palo de la flecha
        pygame.draw.line(pantalla, MARRON,
                         (int(self.x), int(self.y)),
                         (int(self.x - dx), int(self.y - dy)),
                         self.GROSOR)
        # Punta (triangulo pequeño)
        punta = (int(self.x + dx * 0.3), int(self.y + dy * 0.3))
        pygame.draw.circle(pantalla, NEGRO, punta, 4)


# ---------------------------------------------------------------------------

class Blanco:
    """Diana circular con un numero y logica de movimiento."""

    def __init__(self, x: float, y: float, numero: int,
                 vel_x: float = 0.0, vel_y: float = 0.0,
                 es_correcto: bool = False):
        self.x          = x
        self.y          = y
        self.numero     = numero
        self.vel_x      = vel_x
        self.vel_y      = vel_y
        self.es_correcto= es_correcto
        self.radio      = BLANCO_RADIO
        self.activo     = True
        self.golpeado   = False
        self.anim_timer = 0          # frames de animacion post-impacto

    @property
    def rect(self) -> pygame.Rect:
        r = self.radio
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def actualizar(self):
        if self.golpeado:
            self.anim_timer += 1
            if self.anim_timer > 30:
                self.activo = False
            return
        self.x += self.vel_x
        self.y += self.vel_y
        # Rebotar en los bordes verticales del area de juego
        if self.y - self.radio < 100 or self.y + self.radio > ALTO - 60:
            self.vel_y *= -1
        if self.x + self.radio > ANCHO + 20:
            self.activo = False      # salio de pantalla

    def registrar_impacto(self):
        self.golpeado = True
        self.vel_x = 0
        self.vel_y = 0

    def dibujar(self, pantalla: pygame.Surface):
        if not self.activo:
            return
        cx, cy = int(self.x), int(self.y)
        r = self.radio

        # Flash de impacto
        if self.golpeado:
            alpha = max(0, 255 - self.anim_timer * 8)
            color_flash = AMARILLO if self.es_correcto else ROJO_OSCURO
            s = pygame.Surface((r * 2 + 20, r * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color_flash, alpha), (r + 10, r + 10), r + 10)
            pantalla.blit(s, (cx - r - 10, cy - r - 10))

        # Anillos de la diana
        pygame.draw.circle(pantalla, DIANA_ROJO,    (cx, cy), r)
        pygame.draw.circle(pantalla, DIANA_BLANCO,  (cx, cy), int(r * 0.75))
        pygame.draw.circle(pantalla, DIANA_ROJO,    (cx, cy), int(r * 0.50))
        pygame.draw.circle(pantalla, DIANA_NEGRO,   (cx, cy), int(r * 0.25))

        # Numero centrado
        fuente = pygame.font.SysFont("Arial", 22, bold=True)
        texto  = fuente.render(str(self.numero), True, BLANCO)
        rect_t = texto.get_rect(center=(cx, cy))
        pantalla.blit(texto, rect_t)

        # Borde (resaltar si es frame impar para efecto pulso leve)
        pygame.draw.circle(pantalla, NEGRO, (cx, cy), r, 2)


# ---------------------------------------------------------------------------

def generar_blancos(respuesta: int, cantidad: int,
                    vel_x: float = 0.0, vel_y: float = 0.0) -> list:
    """
    Crea `cantidad` Blancos. Uno tiene el numero correcto (respuesta),
    el resto tienen numeros incorrectos plausibles.
    Los distribuye verticalmente en el tercio derecho de la pantalla.
    """
    numeros_incorrectos = _generar_incorrectos(respuesta, cantidad - 1)
    todos = [respuesta] + numeros_incorrectos
    random.shuffle(todos)

    blancos = []
    margen_y = 120
    espacio_y = (ALTO - margen_y * 2) // cantidad
    x_base = ANCHO - 120

    for i, num in enumerate(todos):
        y = margen_y + espacio_y * i + espacio_y // 2
        # Pequena variacion horizontal para no quedar en fila perfecta
        x = x_base + random.randint(-20, 20)
        # Velocidades con direccion alterna
        vy = vel_y if i % 2 == 0 else -vel_y
        es_correcto = (num == respuesta)
        blancos.append(Blanco(x, y, num, vel_x=vel_x, vel_y=vy,
                               es_correcto=es_correcto))

    return blancos


def _generar_incorrectos(respuesta: int, cantidad: int) -> list:
    """Genera numeros incorrectos cercanos a la respuesta (evita duplicados)."""
    incorrectos = set()
    intentos = 0
    while len(incorrectos) < cantidad and intentos < 200:
        delta = random.randint(-10, 10)
        candidato = respuesta + delta
        if candidato != respuesta and candidato >= 0:
            incorrectos.add(candidato)
        intentos += 1
    # Rellenar si faltan
    extra = 1
    while len(incorrectos) < cantidad:
        candidato = respuesta + extra
        if candidato not in incorrectos and candidato != respuesta:
            incorrectos.add(candidato)
        extra += 1
    return list(incorrectos)
