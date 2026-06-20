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

_MUSICA_FONDO = "Hinchada.mp3"

_sonidos = {}
_habilitado = False
_musica_activa = True


def musica_prendida():
    return _musica_activa


def toggle_musica():
    global _musica_activa
    _musica_activa = not _musica_activa
    if _musica_activa:
        reproducir_musica()
    else:
        detener_musica()


def init_audio():
    global _habilitado
    try:
        pygame.mixer.init()
    except pygame.error:
        _habilitado = False
        return

    # cargo los soniditos
    for clave, archivo in _ARCHIVOS.items():
        ruta = os.path.join(_DIR, archivo)
        try:
            _sonidos[clave] = pygame.mixer.Sound(ruta)
        except (pygame.error, FileNotFoundError):
            pass
    _habilitado = True


def reproducir(clave):
    if not _habilitado:
        return
    sonido = _sonidos.get(clave)
    if sonido is not None:
        sonido.play()


def reproducir_musica(volumen=0.2):
    if not _habilitado or not _musica_activa:
        return
    ruta = os.path.join(_DIR, _MUSICA_FONDO)
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(loops=-1)
    except (pygame.error, FileNotFoundError):
        pass


def detener_musica():
    if not _habilitado:
        return
    pygame.mixer.music.stop()
