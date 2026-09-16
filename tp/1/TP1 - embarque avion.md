# TP1 — Simulación de embarque de avión (Di Tella Flying Circus)

> Contexto de trabajo para acompañar a Luca en el TP1 de Aplicaciones Computacionales en Negocios. Se lee junto con `contexto-tutor-socratico.md` (mismo enfoque pedagógico, aplicado acá a un trabajo práctico en vez de al parcial).

## Logística

- Grupo de 4 personas (obligatorio salvo excepción del profesor).
- Entregables: presentación de 15 slides (formato consultoría) + exposición oral grupal de 15 min + código Python entregado a los ayudantes.
- Nicolás anuncia la fecha de presentación de cada grupo **durante la semana del 21 de septiembre de 2026** — o sea, la fecha se define muy pronto (hoy es 15/9). Conviene tener al menos el modelo y una implementación funcionando antes de esa semana.
- 30% de bonus por una sección de exploración libre (trade-offs adicionales, heterogeneidad, ideas de negocio propias testeadas vía simulación).

## El problema (consigna, resumida)

Un avión de 25 filas, 4 asientos por fila (2 izquierda, 2 derecha), pasillo central de una sola persona de ancho. Cada pasajero tiene asiento fijo asignado (no se puede reordenar). Cada pasajero tiene carry-on con probabilidad *p*. Reglas dadas:

- Caminar por el pasillo: 3 seg/fila sin carry-on, 6 seg/fila con carry-on, a velocidad constante, avanzando de a una fila cuando el espacio de adelante estuvo libre 3 segundos.
- Si alguien bloquea el paso al asiento asignado, hay que esperar a que esa persona se pare, deje pasar, y luego ambos se sientan.

Pide comparar 4 políticas de embarque: Back-to-Front, Random, WILMA (Window-Middle-Aisle), Steffen Method — investigar en qué consisten.

Para cada política, estimar vía Monte Carlo (con suficientes corridas y error de estimación reportado):
- Tiempo esperado de llenado del avión.
- Desvío estándar del tiempo de llenado.
- Cómo cambian esas respuestas si p=1 (todos con carry-on) o p=0 (nadie).
- Costo de negocio de una demora de 30 min para una aerolínea (investigar costos operacionales) y si conviene dejar asientos vacíos / acelerar el embarque.

## Plan de trabajo (etapas)

1. **Entender la mecánica** del problema tal cual está dada. ✅
2. **Definir los supuestos faltantes** de comportamiento, con justificación propia. ✅ (ver Decisiones tomadas)
3. **Investigar las 4 políticas** de embarque. ✅ (ver Decisiones tomadas)
4. **Diseñar el modelo de simulación**: qué es un "agente" acá, cómo avanza el reloj. Agente ya definido. Falta: definir el mecanismo del reloj (pasos fijos vs. eventos) y traducir cada política en un algoritmo concreto de orden de embarque.
5. **Implementar en Python**: motor de simulación + visualización del embarque.
6. **Corridas de Monte Carlo**: tiempo esperado, desvío estándar y error de estimación por política.
7. **Análisis de sensibilidad**: variar p (0, 1, valores intermedios).
8. **Análisis de negocio**: costo de demora de 30 min, trade-off asientos vacíos vs. velocidad de embarque.
9. **(Bonus, 30%)**: heterogeneidad adicional, otros trade-offs, ideas de negocio propias.
10. **Armar la presentación** (15 slides) y ensayar la oral de 15 min.

## Decisiones tomadas

**Modelo de agente (el "pasajero"):** cada pasajero es una entidad separada con estado propio: ubicación en el avión, dirección/destino asignado, si tiene carry-on, velocidad de movimiento, y estado de embarque (sentado / parado / caminando / bloqueado-esperando).

**Supuestos de tiempo (todos justificados con fuentes académicas sobre boarding, no inventados a ciegas):**

- *Tiempo de "dejar pasar" cuando el pasajero de pasillo bloquea al de ventana* (en este avión, sin asiento del medio, siempre es el caso más simple — una sola persona se mueve): **Triangular(mín=9, moda=10, máx=13) segundos**. Basado en Schultz (2017), *The Seat Interference Potential as an Indicator for the Aircraft Boarding Progress* (SAE Technical Paper 2017-01-2113).
- *Tiempo de sentarse sin bloqueo*: **Triangular(mín=2, moda=3, máx=4) segundos**. Misma fuente.
- *Tiempo de guardar el carry-on (bloqueo de pasillo por equipaje)*: **Uniforme(13.9, 25) segundos**. Se usó uniforme (no triangular) porque solo hay dos valores puntuales de dos estudios distintos (Schultz 13.9 s; Qiang et al. 2014, 25 s), sin evidencia de qué valor intermedio es más probable — inventar una moda sería agregar información que no se tiene.

**Referencia para validar resultados:** tiempos totales de embarque medidos con pasajeros reales (Steffen, 2011): Back-to-Front 6:11 min, Random 4:44 min, WILMA 4:13 min, Steffen 3:36 min.

**Políticas de embarque investigadas:**

- **Back-to-Front:** se llena de atrás hacia adelante, en bloques/secciones (ej. últimas 5 filas primero), random dentro de cada bloque. Falta decidir cuántos bloques usar.
- **Random:** sin ningún orden — cada pasajero sube en cualquier momento, sin importar fila ni asiento.
- **WILMA (Window-Middle-Aisle):** por tipo de asiento en TODO el avión a la vez (no por fila): primero todos los de ventanilla, después todos los del medio, después todos los de pasillo. En este TP, al no haber asiento del medio, se reduce a: primero todos los de ventanilla, después todos los de pasillo.
- **Steffen Method:** ventanilla filas impares → ventanilla filas pares → medio filas impares → medio filas pares → pasillo filas impares → pasillo filas pares (a veces de a 2 personas en simultáneo, una por lado del pasillo). Combina la ventaja de WILMA con espaciado extra alternando pares/impares. En el experimento real de Steffen resultó 2x más rápido que Back-to-Front. En este TP (sin asiento del medio) el algoritmo se simplifica a 4 grupos en vez de 6: ventanilla impar → ventanilla par → pasillo impar → pasillo par.

Fuentes: [Steffen Boarding Method (Wikipedia)](https://en.wikipedia.org/wiki/Steffen_Boarding_Method) · [The best way to board an airplane, according to science (Popular Science)](https://www.popsci.com/technology/best-way-to-board-an-airplane-according-to-science/) · [The Math Behind United Airlines' Window To Aisle Boarding (Forbes)](https://www.forbes.com/sites/marisagarcia/2023/10/23/united-airlines-window-to-aisle-boarding-how-much-does-it-save/)

## Material de referencia disponible

- `Trabajo práctico 1 ACN 2026.pdf` — consigna oficial.
- `Prácticas/Práctica 3/p03_TP1_repaso_guias.pdf` — repaso de la cátedra sobre TP1: random walk simulado con fórmulas de error de Monte Carlo, e introducción a DES (simulación de eventos discretos).
- `Teóricas/` — Clase 2-3 (probabilidad y MC), Clase 4 (métodos Monte Carlo), Clase 5 (aleatoriedad en la computadora), Clase 6 (procesos de Poisson), Clase 7 (modelos de agentes), Clase 8-10 (procesos estocásticos simulados I-III).

## Estado

Diseño del agente, los tres tiempos aleatorios de comportamiento, y las 4 políticas de embarque, completados y justificados con fuentes (15/9/2026). Falta: definir el mecanismo del reloj de la simulación (pasos fijos vs. eventos), traducir cada política en algoritmo concreto, implementación en Python.
