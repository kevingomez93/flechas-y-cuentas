"""
generar_sonidos.py - Genera los efectos de sonido del juego (.wav).

Todos los sonidos se sintetizan con la libreria estandar de Python (wave, math,
struct), sin dependencias externas ni recursos descargados de internet: son de
produccion propia. Ejecutar una sola vez para (re)generar la carpeta Sonidos/:

    python generar_sonidos.py
"""
import os
import wave
import struct
import math
import random

SAMPLE_RATE = 22050
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sonidos")


def _envolvente(i, n, ataque=0.01, caida=0.3):
    """Envolvente de amplitud: ataque lineal corto + decaimiento exponencial."""
    a = max(1, int(n * ataque))
    if i < a:
        return i / a
    return math.exp(-(i - a) / (n * caida))


def tono(freq, dur, vol=0.5, forma="sine", caida=0.3):
    n = int(SAMPLE_RATE * dur)
    muestras = []
    for i in range(n):
        t = i / SAMPLE_RATE
        if forma == "square":
            s = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        elif forma == "saw":
            s = 2 * ((freq * t) % 1.0) - 1.0
        elif forma == "noise":
            s = random.uniform(-1, 1)
        else:
            s = math.sin(2 * math.pi * freq * t)
        muestras.append(s * _envolvente(i, n, caida=caida) * vol)
    return muestras


def barrido(f0, f1, dur, vol=0.5, forma="sine", caida=0.3):
    """Tono con frecuencia que varia linealmente de f0 a f1."""
    n = int(SAMPLE_RATE * dur)
    muestras = []
    fase = 0.0
    for i in range(n):
        freq = f0 + (f1 - f0) * (i / n)
        fase += 2 * math.pi * freq / SAMPLE_RATE
        if forma == "square":
            s = 1.0 if math.sin(fase) >= 0 else -1.0
        elif forma == "saw":
            s = 2 * ((fase / (2 * math.pi)) % 1.0) - 1.0
        else:
            s = math.sin(fase)
        muestras.append(s * _envolvente(i, n, caida=caida) * vol)
    return muestras


def secuencia(notas, forma="sine", vol=0.5, caida=0.3):
    """notas: lista de (frecuencia, duracion) reproducidas en orden."""
    out = []
    for f, d in notas:
        out.extend(tono(f, d, vol=vol, forma=forma, caida=caida))
    return out


def mezclar(*pistas):
    n = max(len(p) for p in pistas)
    out = [0.0] * n
    for p in pistas:
        for i, v in enumerate(p):
            out[i] += v
    return out


def guardar(nombre, muestras):
    ruta = os.path.join(DIR, nombre)
    with wave.open(ruta, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for s in muestras:
            v = max(-1.0, min(1.0, s))
            frames += struct.pack("<h", int(v * 32767))
        w.writeframes(bytes(frames))
    print(f"generado {nombre}  ({len(muestras) / SAMPLE_RATE:.2f}s)")


def main():
    os.makedirs(DIR, exist_ok=True)
    random.seed(7)

    # Disparo: barrido descendente + ruido (cuerda del arco)
    guardar("disparo.wav", mezclar(
        barrido(700, 180, 0.18, vol=0.40, forma="saw", caida=0.25),
        tono(120, 0.18, vol=0.22, forma="noise", caida=0.20),
    ))

    # Acierto: arpegio alegre ascendente (Do, Mi, Sol, Do agudo)
    guardar("acierto.wav", secuencia(
        [(523, 0.08), (659, 0.08), (784, 0.08), (1047, 0.18)],
        forma="square", vol=0.32, caida=0.35))

    # Incorrecto: dos notas graves descendentes
    guardar("incorrecto.wav", secuencia(
        [(196, 0.14), (147, 0.24)], forma="square", vol=0.30, caida=0.30))

    # Fallo (flecha errada / tiempo agotado): nota corta y apagada
    guardar("fallo.wav", barrido(300, 120, 0.22, vol=0.28, forma="sine", caida=0.25))

    # Nivel superado: jingle ascendente
    guardar("nivel.wav", secuencia(
        [(523, 0.10), (659, 0.10), (784, 0.10), (1047, 0.26)],
        forma="square", vol=0.30, caida=0.40))

    # Victoria: jingle triunfal mas largo
    guardar("victoria.wav", secuencia(
        [(523, 0.12), (659, 0.12), (784, 0.12), (1047, 0.12), (784, 0.12), (1047, 0.38)],
        forma="square", vol=0.31, caida=0.40))

    # Game over: descenso triste
    guardar("gameover.wav", secuencia(
        [(440, 0.18), (370, 0.18), (294, 0.18), (220, 0.42)],
        forma="sine", vol=0.32, caida=0.35))


if __name__ == "__main__":
    main()
