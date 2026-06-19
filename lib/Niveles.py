import random


class ConfigNivel:
    def __init__(self, numero, nombre, viento, vel_x, vel_y, tiempo, flechas, generador, bob=0.0):
        self.numero = numero
        self.nombre = nombre
        self.viento = viento
        self.vel_x_blancos = vel_x
        self.vel_y_blancos = vel_y
        self.tiempo_ronda = tiempo
        self.flechas = flechas
        self.generador = generador
        self.bob = bob


def _op_suma_resta():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    if random.random() < 0.5:
        return f"{a} + {b} = ?", a + b
    mayor, menor = max(a, b), min(a, b)
    return f"{mayor} - {menor} = ?", mayor - menor


def _op_mult_div():
    if random.random() < 0.5:
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        return f"{a} x {b} = ?", a * b
    divisor = random.randint(2, 10)
    resultado = random.randint(1, 10)
    dividendo = divisor * resultado
    return f"{dividendo} / {divisor} = ?", resultado


def _op_mixta():
    tipo = random.randint(1, 4)
    if tipo == 1:
        return _op_suma_resta()
    if tipo == 2:
        return _op_mult_div()
    if tipo == 3:
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        c = random.randint(2, 4)
        return f"({a} + {b}) x {c} = ?", (a + b) * c
    a = random.randint(2, 9)
    return f"{a}^2 = ?", a * a


NIVELES = [
    ConfigNivel(1, "Nivel 1", 0.0, 0.0, 0.0, 20, 20, _op_suma_resta, bob=10.0),
    ConfigNivel(2, "Nivel 2", 0.008, 0.0, 1.8, 18, 18, _op_mult_div, bob=16.0),
    ConfigNivel(3, "Nivel 3", 0.02, 0.0, 3.5, 15, 15, _op_mixta, bob=22.0),
]


def obtener_nivel(numero):
    return NIVELES[numero - 1]


def nueva_operacion(nivel):
    return nivel.generador()
