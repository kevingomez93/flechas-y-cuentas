# Variables y constantes globales del juego

# --- Ventana ---
ANCHO           = 960
ALTO            = 600
TITULO          = "Arqueria Educativa"
FPS             = 60

# --- Fisica ---
GRAVEDAD        = 0.25       # pixeles/frame^2, aplicada a la flecha
VEL_BASE        = 14         # velocidad minima de disparo
VEL_MAX         = 24         # velocidad maxima de disparo (carga completa)
TIEMPO_CARGA    = 150        # frames maximos de carga de potencia

# --- Control de angulo ---
VEL_ANGULO      = 0.8        # grados por frame al mantener la tecla presionada

# --- Previsualizacion de trayectoria ---
PREVIEW_PASOS   = 60         # cantidad de puntos del arco a dibujar
PREVIEW_SALTO   = 3          # frames simulados entre cada punto visible

# --- Arquero ---
ARQUERO_X       = 90         # posicion fija horizontal del arquero
ARQUERO_Y       = 420        # posicion fija vertical (centro del arquero)

# --- Blancos ---
BLANCO_RADIO    = 45         # radio visual de la diana
BLANCOS_POR_RON = 4          # cantidad de blancos por ronda

# --- Puntaje ---
PUNTOS_CORRECTO = 100        # puntos base por acertar al correcto
PUNTOS_BONUS_T  = 2          # multiplicador de bonus por segundo restante
PUNTOS_FALLO    = -30        # penalizacion por acertar al incorrecto
PUNTOS_ERRAR    = -10        # penalizacion por flecha que no da en ningun blanco

# --- Juego ---
ACIERTOS_NIVEL  = 5          # aciertos correctos para pasar de nivel
VIDAS           = 5          # flechas/vidas iniciales

# --- Estados del juego ---
ESTADO_MENU     = "menu"
ESTADO_JUEGO    = "juego"
ESTADO_NIVEL_OK = "nivel_ok"
ESTADO_GAME_OVER= "game_over"
ESTADO_VICTORIA = "victoria"
ESTADO_CREDITOS = "creditos"

# --- Niveles ---
TOTAL_NIVELES   = 3
