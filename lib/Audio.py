"""
Audio.py - Carga y reproduccion de los efectos de sonido del juego.

Los .wav viven en la carpeta Sonidos/ (ver generar_sonidos.py). El modulo es
tolerante a fallos: si el sistema no tiene salida de audio disponible, el juego
sigue funcionando sin sonido en lugar de cerrarse con error.
"""
import os
import pygame

_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Sonidos")

_ARCHIVOS = {
    "disparo":    "disparo.wav",
    "acierto":    "acierto.wav",
    "incorrecto": "incorrecto.wav",
    "fallo":      "fallo.wav",
    "nivel":      "nivel.wav",
    "victoria":   "victoria.wav",
    "gameover":   "gameover.wav",
}

_sonidos = {}
_habilitado = False


def init_audio():
    """Inicializa el mezclador y precarga los sonidos. Llamar tras pygame.init()."""
    global _habilitado
    try:
        pygame.mixer.init()
    except pygame.error:
        _habilitado = False
        return

    for clave, archivo in _ARCHIVOS.items():
        ruta = os.path.join(_DIR, archivo)
        try:
            _sonidos[clave] = pygame.mixer.Sound(ruta)
        except (pygame.error, FileNotFoundError):
            pass
    _habilitado = True


def reproducir(clave):
    """Reproduce el efecto indicado si el audio esta disponible."""
    if not _habilitado:
        return
    sonido = _sonidos.get(clave)
    if sonido is not None:
        sonido.play()
