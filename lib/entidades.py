import os
import pygame
import math
import random

from lib.colores import (
    NEGRO, BLANCO, AMARILLO, ROJO_OSCURO, VERDE_OSCURO, NARANJA
)
from lib.imagenes import cargar_sprite
from lib.variables import (
    ARQUERO_X, ARQUERO_Y, VEL_BASE, VEL_MAX, TIEMPO_CARGA,
    GRAVEDAD, ANCHO, ALTO, BLANCO_RADIO,
    PREVIEW_PASOS, PREVIEW_SALTO
)


class Arquero:
    def __init__(self):
        self.x = ARQUERO_X
        self.y = ARQUERO_Y
        self.angulo = -15.0
        self.cargando = False
        self.tiempo_carga = 0

        # imagen del arquero (messi)
        self._sprite = cargar_sprite(os.path.join("Personaje", "arquero.png"))
        self._sprite_offset = (40, 60)

    def ajustar_angulo(self, delta):
        self.angulo = max(-85.0, min(10.0, self.angulo + delta))

    def iniciar_carga(self):
        self.cargando = True

    def calcular_potencia(self):
        return VEL_BASE + (VEL_MAX - VEL_BASE) * (self.tiempo_carga / TIEMPO_CARGA)

    def liberar(self):
        if not self.cargando:
            return None
        self.cargando = False
        potencia = self.calcular_potencia()
        self.tiempo_carga = 0
        rad = math.radians(self.angulo)
        vx = potencia * math.cos(rad)
        vy = potencia * math.sin(rad)
        return Flecha(self.x + 30, self.y - 10, vx, vy)

    def puntos_trayectoria(self, viento=0.0):
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

    def dibujar(self, pantalla):
        cx, cy = self.x, self.y

        ox, oy = self._sprite_offset
        pantalla.blit(self._sprite, (cx - ox, cy - oy))

        largo = 55
        rad = math.radians(self.angulo)
        ex = cx + 30 + int(largo * math.cos(rad))
        ey = cy - 10 + int(largo * math.sin(rad))
        pygame.draw.line(pantalla, NEGRO, (cx + 30, cy - 10), (ex, ey), 5)
        pygame.draw.line(pantalla, AMARILLO, (cx + 30, cy - 10), (ex, ey), 3)

        if self.cargando:
            self._dibujar_barra_potencia(pantalla, cx, cy)

    def _dibujar_barra_potencia(self, pantalla, cx, cy):
        ancho_barra = 60
        alto_barra = 8
        bx = cx - ancho_barra // 2
        by = cy + 55
        pygame.draw.rect(pantalla, NEGRO, (bx - 1, by - 1, ancho_barra + 2, alto_barra + 2))
        lleno = int(ancho_barra * self.tiempo_carga / TIEMPO_CARGA)
        if lleno < ancho_barra * 0.6:
            color = VERDE_OSCURO
        elif lleno < ancho_barra * 0.85:
            color = NARANJA
        else:
            color = ROJO_OSCURO
        pygame.draw.rect(pantalla, color, (bx, by, lleno, alto_barra))


class Flecha:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.activa = True
        # sprite de la flecha
        self._sprite = cargar_sprite(os.path.join("Obstaculos", "flecha.png"))

    def actualizar(self, viento=0.0):
        self.vy += GRAVEDAD
        self.vx += viento * 0.01
        self.x += self.vx
        self.y += self.vy
        if self.x > ANCHO + 50 or self.y > ALTO + 50 or self.x < -50:
            self.activa = False

    def angulo_visual(self):
        return math.degrees(math.atan2(self.vy, self.vx))

    def rect(self):
        return pygame.Rect(self.x - 5, self.y - 5, 14, 14)

    def dibujar(self, pantalla):
        sprite_rotado = pygame.transform.rotate(self._sprite, -self.angulo_visual())
        rect = sprite_rotado.get_rect(center=(int(self.x), int(self.y)))
        pantalla.blit(sprite_rotado, rect)


class Blanco:
    def __init__(self, x, y, numero, vel_x=0.0, vel_y=0.0, es_correcto=False,
                 bob_amp=0.0, bob_speed=0.0, fase=0.0):
        self.x = x
        self.y = y
        self.base_x = x
        self.base_y = y
        self.numero = numero
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.es_correcto = es_correcto
        self.radio = BLANCO_RADIO
        self.activo = True
        self.golpeado = False
        self.anim_timer = 0
        # esto es para que el blanco se mueva un poco y no sea tan aburrido
        self.bob_amp = bob_amp
        self.bob_speed = bob_speed
        self.fase = fase
        self.t = 0
        self._sprite = cargar_sprite(os.path.join("Enemigos", "diana.png"))

    def rect(self):
        r = self.radio
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def actualizar(self):
        if self.golpeado:
            self.anim_timer += 1
            if self.anim_timer > 30:
                self.activo = False
            return
        self.t += 1
        self.base_x += self.vel_x
        self.base_y += self.vel_y
        if self.base_y - self.radio < 100 or self.base_y + self.radio > ALTO - 60:
            self.vel_y *= -1
        # Flotacion suave: oscilacion senoidal en X e Y alrededor de la base
        osc = self.t * self.bob_speed + self.fase
        self.x = self.base_x + math.sin(osc) * self.bob_amp
        self.y = self.base_y + math.cos(osc * 1.3) * (self.bob_amp * 0.6)
        if self.base_x + self.radio > ANCHO + 20:
            self.activo = False

    def registrar_impacto(self):
        self.golpeado = True
        self.vel_x = 0
        self.vel_y = 0

    def dibujar(self, pantalla):
        if not self.activo:
            return
        cx, cy = int(self.x), int(self.y)
        r = self.radio

        if self.golpeado:
            alpha = max(0, 255 - self.anim_timer * 8)
            color_flash = AMARILLO if self.es_correcto else ROJO_OSCURO
            s = pygame.Surface((r * 2 + 20, r * 2 + 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color_flash, alpha), (r + 10, r + 10), r + 10)
            pantalla.blit(s, (cx - r - 10, cy - r - 10))

        pantalla.blit(self._sprite, (cx - 45, cy - 45))

        fuente = pygame.font.SysFont("Arial", 22, bold=True)
        numero_str = str(self.numero)
        texto_blanco = fuente.render(numero_str, True, BLANCO)
        texto_negro = fuente.render(numero_str, True, NEGRO)
        rect_t = texto_blanco.get_rect(center=(cx, cy))
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            pantalla.blit(texto_negro, rect_t.move(dx, dy))
        pantalla.blit(texto_blanco, rect_t)

        pygame.draw.circle(pantalla, NEGRO, (cx, cy), r, 2)


def generar_blancos(respuesta, cantidad, vel_x=0.0, vel_y=0.0, bob_amp=0.0):
    # crea los blancos, uno con la respuesta correcta y los demas con numeros parecidos
    numeros_incorrectos = _generar_incorrectos(respuesta, cantidad - 1)
    todos = [respuesta] + numeros_incorrectos
    random.shuffle(todos)

    blancos = []
    margen_y = 120
    espacio_y = (ALTO - margen_y * 2) // cantidad
    x_base = ANCHO - 120

    for i, num in enumerate(todos):
        y = margen_y + espacio_y * i + espacio_y // 2
        x = x_base + random.randint(-20, 20)
        vy = vel_y if i % 2 == 0 else -vel_y
        es_correcto = (num == respuesta)
        fase = random.uniform(0, 6.28)
        bob_speed = random.uniform(0.05, 0.09)
        blancos.append(Blanco(x, y, num, vel_x=vel_x, vel_y=vy, es_correcto=es_correcto,
                              bob_amp=bob_amp, bob_speed=bob_speed, fase=fase))

    return blancos


def _generar_incorrectos(respuesta, cantidad):
    incorrectos = set()
    intentos = 0
    while len(incorrectos) < cantidad and intentos < 200:
        delta = random.randint(-10, 10)
        candidato = respuesta + delta
        if candidato != respuesta and candidato >= 0:
            incorrectos.add(candidato)
        intentos += 1
    extra = 1
    while len(incorrectos) < cantidad:
        candidato = respuesta + extra
        if candidato not in incorrectos and candidato != respuesta:
            incorrectos.add(candidato)
        extra += 1
    return list(incorrectos)
