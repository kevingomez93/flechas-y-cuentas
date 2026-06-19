# Trabajo Práctico Integrador – Videojuegos

## Documento académico y reflexión final

---

**Materia:** Programación 2
**Comisión:** B
**Grupo:** 14
**Año:** 2026
**Integrantes:** Franco Fernández Sica · Kevin Gómez
**Proyecto:** *Flechas y Cuentas* — videojuego de arquería con temática de fútbol para la práctica de cálculo mental

---

## 1. Introducción

El presente documento acompaña la entrega del Trabajo Práctico Integrador de la
materia Programación 2. En él describimos el videojuego desarrollado, las
decisiones de diseño que tomamos, la arquitectura del código y una reflexión
final sobre el valor educativo de la propuesta y sobre el proceso de aprendizaje
que implicó construirla.

El proyecto, titulado **Flechas y Cuentas**, es un videojuego en 2D
desarrollado con **Python 3** y la librería **pygame** (en su variante
*pygame-ce*). Su finalidad es doble: por un lado, aplicar los conceptos técnicos
trabajados en la cursada (entradas y salidas, programación orientada a objetos,
manejo de la librería pygame y buenas prácticas de programación); por otro,
ofrecer una experiencia con un propósito didáctico claro.

Para hacer la propuesta más atractiva y cercana, elegimos una **ambientación de
fútbol**: el personaje que controla el jugador es un futbolista (un arquero
inspirado en Lionel Messi, con la camiseta de la Selección Argentina) que dispara
flechas dentro de un **estadio**, y el juego incorpora **efectos de sonido** que
refuerzan cada acción. La temática es una capa de motivación sobre un contenido
educativo que sigue siendo el cálculo mental.

## 2. Tema educativo y justificación

El contenido didáctico elegido es la **práctica del cálculo mental**: sumas,
restas, multiplicaciones y divisiones. La elección responde a que se trata de una
habilidad concreta, evaluable y de utilidad transversal, que se presta a una
mecánica de juego ágil y repetible.

La integración entre juego y aprendizaje no es accesoria sino que está en el
núcleo de la mecánica: en cada ronda se plantea una operación matemática y el
jugador debe **disparar una flecha al blanco que muestra el resultado correcto**,
descartando los blancos con respuestas incorrectas. De esta manera, el acierto en
el juego depende directamente de la resolución correcta del problema matemático.

Como valor agregado, la mecánica de disparo parabólico introduce de manera
intuitiva nociones básicas de **ángulo, potencia y trayectoria**, vinculando el
contenido matemático con una noción elemental de física.

La ambientación futbolística (estadio, futbolista, hinchada) funciona como
**gancho motivacional**: para un público joven, "meterla en el ángulo" resolviendo
una cuenta resulta más atractivo que un ejercicio matemático tradicional, sin que
ello altere el contenido que se practica.

## 3. Objetivos del jugador y reglas

El objetivo del jugador es **superar los tres niveles** acumulando el mayor
puntaje posible. Las reglas que guían la experiencia son:

- En cada ronda se presenta una operación matemática en el HUD superior.
- Aparecen varios blancos numerados; solo uno contiene la respuesta correcta.
- El jugador ajusta el **ángulo** del arco (flechas ↑ / ↓) y la **potencia**
  (mantener y soltar la barra espaciadora) para disparar.
- **Acertar** al blanco correcto suma puntos, con un **bonus** proporcional al
  tiempo restante de la ronda.
- **Errar el blanco**, **golpear un blanco incorrecto** o **quedarse sin tiempo**
  restan puntos y/o flechas.
- Si se agotan las flechas, la partida termina (*Game Over*).
- Al completar la cantidad de aciertos requeridos se avanza de nivel; al superar
  el nivel 3 se alcanza la pantalla de *Victoria*.

El **sistema de puntaje es claro y visible** en todo momento en el HUD, junto con
el nivel actual, las flechas disponibles, los aciertos, el tiempo restante y el
indicador de viento.

## 4. Diseño del nivel y progresión de dificultad

El juego cumple con el requisito de **retos acumulativos con un mínimo de tres
niveles** y dificultad gradual. La progresión se diseñó modificando varios
parámetros simultáneamente:

| Nivel | Operaciones                | Blancos                      | Viento     | Tiempo | Flechas | Escenario |
|-------|----------------------------|------------------------------|------------|--------|---------|-----------|
| 1     | Sumas y restas             | Flotación leve               | Sin viento | 20 s   | 20      | Estadio de día |
| 2     | Multiplicación y división  | Movimiento vertical + flotación | Leve    | 18 s   | 18      | Estadio al atardecer |
| 3     | Operaciones mixtas         | Movimiento rápido + flotación   | Fuerte  | 15 s   | 15      | Estadio de noche |

La dificultad crece en tres dimensiones complementarias:

1. **Cognitiva**: las operaciones pasan de sumas/restas simples a
   multiplicaciones, divisiones y, finalmente, operaciones combinadas y potencias.
2. **De puntería**: todos los blancos tienen una **flotación suave** que les da
   vida, y a medida que se avanza se suman desplazamiento vertical y un viento que
   desvía progresivamente la trayectoria de la flecha, obligando a corregir el
   ángulo y la potencia.
3. **De tiempo**: el límite por ronda y la cantidad de flechas disponibles se
   reducen en cada nivel.

Además, cada nivel transcurre en un **fondo de estadio distinto** (día, atardecer
y noche con reflectores), de modo que la ambientación también acompaña la
progresión y refuerza la sensación de avance.

Los **elementos de diseño** del PDF están presentes: el personaje central
(el futbolista arquero), los blancos como objetivos/“enemigos”, los obstáculos
físicos (viento, gravedad), el reto lógico (la operación) y un sistema de
recompensa/penalización —reforzado con sonido— que retroalimenta el aprendizaje.

## 5. Arquitectura y organización del código

El proyecto respeta la estructura de carpetas sugerida en la consigna y separa
responsabilidades en módulos dentro de `lib/`:

```
flechas-y-cuentas/
├── lib/
│   ├── __init__.py
│   ├── Color.py       # Paleta de colores centralizada
│   ├── Var.py         # Constantes y variables globales (física, puntaje, estados)
│   ├── Core.py        # Bucle principal, estados del juego y HUD
│   ├── Entidades.py   # Clases Arquero, Flecha y Blanco
│   ├── Niveles.py     # Configuración de niveles y generación de operaciones
│   ├── Assets.py      # Carga de sprites y fondos
│   └── Audio.py       # Carga y reproducción de los efectos de sonido
├── Sprite/
│   ├── Personaje/     ├── Enemigos/     ├── Obstaculos/     └── Fondos/
├── Sonidos/           # Efectos de sonido (.wav) generados por el grupo
├── Main.py            # Punto de acceso al juego
├── Creditos.py        # Información del juego y autores
└── generar_sonidos.py # Script que sintetiza los efectos de sonido
```

### Programación orientada a objetos

El diseño se apoya en **clases y objetos**, tal como exige la consigna:

- **`Core`**: orquesta el bucle principal del juego, la máquina de estados
  (menú, juego, transición de nivel, game over, victoria, créditos) y el dibujado.
- **`EstadoJuego`**: encapsula la lógica de una partida en curso (rondas,
  puntaje, temporizador, mensajes).
- **`Arquero`**: el personaje central (el futbolista); gestiona ángulo, carga de
  potencia, disparo y la vista previa de la trayectoria.
- **`Flecha`**: el proyectil, con su física de gravedad y viento.
- **`Blanco`**: los objetivos numerados, con movimiento, **flotación senoidal** y
  animación de impacto.
- **`ConfigNivel`**: agrupa los parámetros de cada nivel (operaciones, viento,
  movimiento y flotación de blancos, tiempo, flechas), lo que permite añadir o
  ajustar niveles sin modificar la lógica del juego.
- **Módulo `Audio`**: encapsula la inicialización del mezclador y la reproducción
  de los efectos de sonido, de forma tolerante a fallos (si no hay salida de audio
  disponible, el juego continúa sin sonido en lugar de cerrarse).

### Sistema de colisiones

El sistema de colisiones —uno de los objetivos centrales del TP— se implementó
mediante **detección por distancia euclidiana** entre el centro de la flecha y el
centro de cada blanco. Cuando la distancia es menor que el radio del blanco, se
registra el impacto y se evalúa si el blanco golpeado era el correcto, aplicando
en consecuencia el puntaje o la penalización correspondiente.

### Entradas y salidas

- **Entradas**: teclado para el control del ángulo (↑/↓), la carga y el disparo
  (barra espaciadora), la navegación de menús (ENTER) y la salida (ESC); además
  del mouse para seleccionar opciones en el menú principal.
- **Salidas**: la pantalla con el HUD, los sprites, la vista previa de la
  trayectoria, los mensajes de retroalimentación y las pantallas de transición,
  más la **salida de audio** con los efectos de sonido.

### Sistema de audio

El juego incorpora **siete efectos de sonido** (disparo, acierto, error, fallo,
nivel superado, victoria y game over) que acompañan cada acción y mejoran la
retroalimentación al jugador. Una particularidad de nuestra implementación es que
los sonidos **no se descargaron de internet**, sino que se **sintetizan por
código** en `generar_sonidos.py` usando únicamente la librería estándar de Python
(`wave`, `math`, `struct`): se generan tonos, barridos de frecuencia y pequeños
arpegios con su propia envolvente de amplitud. Esto los convierte en producción
propia y mantiene el proyecto libre de dependencias externas adicionales.

## 6. Buenas prácticas aplicadas

Durante el desarrollo procuramos respetar las buenas prácticas discutidas en
clase:

- **Separación de responsabilidades** en módulos cohesivos dentro de `lib/`.
- **Centralización de constantes** (colores en `Color.py`, parámetros de juego en
  `Var.py`), evitando “números mágicos” dispersos por el código.
- **Nombres descriptivos** para clases, funciones y variables.
- **Reutilización de código** mediante funciones auxiliares para el dibujado y la
  generación de operaciones y blancos.
- **Configuración de niveles orientada a datos**, que facilita extender el juego.
- **Tolerancia a fallos** en el sistema de audio: el juego no se cae si el equipo
  no tiene salida de sonido disponible.
- **Recursos de producción propia**: los efectos de sonido se generan por código y
  los sprites/fondos fueron elaborados por el grupo, evitando recursos de terceros.

## 7. Dificultades encontradas y soluciones

Durante el desarrollo enfrentamos varios desafíos que nos obligaron a aplicar y
profundizar lo aprendido:

- **Ajuste de la física del disparo**: equilibrar gravedad, potencia y rango de
  ángulos para que el juego resultara desafiante pero jugable requirió varias
  iteraciones de prueba y ajuste de constantes.
- **Detección de colisiones precisa**: pasamos de comparaciones por rectángulos a
  una verificación por distancia al centro, que se ajusta mejor a la forma
  circular de los blancos.
- **Sensación de control**: incorporamos una vista previa de la trayectoria para
  que el jugador pudiera anticipar el efecto del ángulo, la potencia y el viento,
  mejorando la experiencia y reforzando la noción física.
- **Generación de respuestas incorrectas plausibles**: para que los blancos
  erróneos no fueran obvios, generamos distractores cercanos al resultado correcto.
- **Movimiento de los blancos sin afectar las colisiones**: para dar más vida al
  juego sumamos una flotación senoidal a cada blanco; tuvimos que separar la
  posición "base" (que se desplaza) de la oscilación, cuidando que la detección de
  impactos siguiera usando la posición real en pantalla.
- **Síntesis de sonido propia**: en lugar de buscar audios externos, aprendimos a
  generar ondas y envolventes para producir efectos retro con la librería estándar.
- **Tratamiento de los recursos gráficos**: ajustar los sprites y fondos al tamaño
  y la posición correctos (recorte, escalado y transparencia) para que encajaran
  con la lógica de dibujado existente.

## 8. Reflexión final sobre el valor educativo

El proceso de construir este videojuego nos permitió **integrar en un único
producto** los contenidos de la materia: pasamos de escribir funciones aisladas a
diseñar un sistema con estado, entidades que interactúan y un bucle de juego
coherente. Comprendimos en la práctica por qué la **programación orientada a
objetos** y la **separación en módulos** no son una formalidad, sino herramientas
que vuelven el código mantenible y extensible: agregar un nivel o cambiar una
regla se reduce a modificar datos de configuración, no la lógica central.

Respecto al **valor educativo de la propuesta**, consideramos que la fortaleza de
*Flechas y Cuentas* está en que el aprendizaje no es un añadido decorativo sino la
condición para avanzar: no se puede ganar sin resolver correctamente las
operaciones. La presión del tiempo y la progresión de dificultad fomentan la
**agilidad en el cálculo mental**, mientras que la mecánica de disparo introduce
de forma lúdica nociones de ángulo y trayectoria. La **ambientación de fútbol**, el
movimiento de los blancos y los **efectos de sonido** aportan motivación y
retroalimentación, elementos que la literatura sobre gamificación asocia a una
mayor adherencia del estudiante. Creemos que una herramienta así podría usarse
efectivamente para reforzar el cálculo en estudiantes de los primeros años de la
escolaridad, combinando motivación y contenido.

En lo personal, el trabajo nos dejó una valoración del proceso completo de
desarrollo de software: planificar la arquitectura antes de programar, probar de
forma iterativa, y cuidar la legibilidad y organización del código para poder
trabajar en equipo sobre una misma base.

## 9. Declaración de uso de Inteligencia Artificial

En conformidad con las pautas del TP, declaramos que parte de la estructura y del
código de este proyecto fue asistida por herramientas de inteligencia artificial
(Cursor / Claude). El uso se limitó a apoyo en la organización del código, la
redacción de documentación y la resolución de dudas técnicas. El diseño del juego,
las decisiones pedagógicas, las pruebas y la integración final son producción
propia del grupo, y comprendemos el funcionamiento de cada componente del código
entregado.

## 10. Conclusión

*Flechas y Cuentas* cumple con los lineamientos del Trabajo Práctico Integrador:
presenta una modalidad educativa concreta, un personaje central, un sistema de
puntaje claro y visible, reglas definidas, tres niveles con dificultad gradual y
un sistema de colisiones funcional, todo organizado según la estructura de
proyecto solicitada y aplicando las buenas prácticas trabajadas en la cursada.
A esa base le sumamos una **ambientación de fútbol** (personaje, estadios y
sonido) y **movimiento en los blancos** que hacen la experiencia más entretenida
sin perder el foco educativo. Más allá del resultado, el proyecto nos sirvió para
consolidar los conocimientos de Programación 2 en un desarrollo integral y con
sentido.

---

*Franco Fernández Sica · Kevin Gómez — Grupo 14 — Programación 2 — 2026*
