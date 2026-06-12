import random
from dataclasses import dataclass, field
from typing import Callable, Tuple


@dataclass
class ConfigNivel:
    """Parametros de dificultad para cada nivel."""
    numero:          int
    nombre:          str
    descripcion:     str
    viento:          float        # aceleracion horizontal de la flecha (px/frame^2)
    vel_x_blancos:   float        # velocidad horizontal de los blancos
    vel_y_blancos:   float        # velocidad vertical (rebote) de los blancos
    tiempo_ronda:    int          # segundos maximos por ronda
    flechas:         int          # flechas disponibles por nivel completo
    generador:       Callable[[], Tuple[str, int]]  # devuelve (enunciado, respuesta)
    color_cielo:     tuple        # color de fondo del nivel


# ---------------------------------------------------------------------------
# Generadores de operaciones matematicas
# ---------------------------------------------------------------------------

def _op_suma_resta() -> Tuple[str, int]:
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    if random.random() < 0.5:
        return f"{a} + {b} = ?", a + b
    else:
        mayor, menor = max(a, b), min(a, b)
        return f"{mayor} - {menor} = ?", mayor - menor


def _op_mult_div() -> Tuple[str, int]:
    if random.random() < 0.5:
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        return f"{a} x {b} = ?", a * b
    else:
        divisor   = random.randint(2, 10)
        resultado = random.randint(1, 10)
        dividendo = divisor * resultado
        return f"{dividendo} / {divisor} = ?", resultado


def _op_mixta() -> Tuple[str, int]:
    tipo = random.randint(1, 4)
    if tipo == 1:
        return _op_suma_resta()
    elif tipo == 2:
        return _op_mult_div()
    elif tipo == 3:
        # Dos operaciones: (a + b) * c  con numeros chicos
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        c = random.randint(2, 4)
        return f"({a} + {b}) x {c} = ?", (a + b) * c
    else:
        # a^2
        a = random.randint(2, 9)
        return f"{a}^2 = ?", a * a


# ---------------------------------------------------------------------------
# Definicion de los 3 niveles
# ---------------------------------------------------------------------------

from lib.Color import CIELO_N1, CIELO_N2, CIELO_N3

NIVELES: list[ConfigNivel] = [
    ConfigNivel(
        numero        = 1,
        nombre        = "Nivel 1 - Practica basica",
        descripcion   = "Suma y resta\nBlancos estaticos, sin viento",
        viento        = 0.0,
        vel_x_blancos = 0.0,
        vel_y_blancos = 0.0,
        tiempo_ronda  = 20,
        flechas       = 20,
        generador     = _op_suma_resta,
        color_cielo   = CIELO_N1,
    ),
    ConfigNivel(
        numero        = 2,
        nombre        = "Nivel 2 - Intermedio",
        descripcion   = "Multiplicacion y division\nBlancos en movimiento, viento leve",
        viento        = 0.008,
        vel_x_blancos = 0.0,
        vel_y_blancos = 1.8,
        tiempo_ronda  = 18,
        flechas       = 18,
        generador     = _op_mult_div,
        color_cielo   = CIELO_N2,
    ),
    ConfigNivel(
        numero        = 3,
        nombre        = "Nivel 3 - Avanzado",
        descripcion   = "Operaciones mixtas\nBlancos rapidos, viento fuerte",
        viento        = 0.02,
        vel_x_blancos = 0.0,
        vel_y_blancos = 3.5,
        tiempo_ronda  = 15,
        flechas       = 15,
        generador     = _op_mixta,
        color_cielo   = CIELO_N3,
    ),
]


def obtener_nivel(numero: int) -> ConfigNivel:
    """Devuelve la configuracion del nivel (1-indexado)."""
    return NIVELES[numero - 1]


def nueva_operacion(nivel: ConfigNivel) -> Tuple[str, int]:
    """Genera un nuevo enunciado y respuesta para el nivel dado."""
    return nivel.generador()
