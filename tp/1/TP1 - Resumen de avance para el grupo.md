# TP1 — Simulación de embarque de avión: resumen de lo que armamos

Este documento resume el trabajo de diseño que hicimos hasta ahora para el TP1, antes de escribir una sola línea de código. La idea es que lo lean junto con la consigna original (el PDF del TP). Está escrito en modo simple, para que cualquiera del grupo lo entienda sin haber estado en la charla.

## 1. Qué tenemos que simular, en una frase

Un avión de 25 filas y 4 asientos por fila (2 de ventana, 2 de pasillo, sin asiento del medio) donde cada pasajero tiene que caminar hasta su fila y sentarse, a veces bloqueando o siendo bloqueado por otros. Tenemos que comparar 4 formas distintas de ordenar el embarque y ver cuál es más rápida, con qué variabilidad, y qué le conviene a la aerolínea en plata.

## 2. Qué tipo de modelo es este

No es "una sola cosa random que se repite" (como tirar una moneda). Es un **modelo basado en agentes**: cada pasajero es una entidad separada, con su propia lógica, y todos se mueven e interactúan al mismo tiempo (se bloquean, se esperan). El comportamiento del avión completo "emerge" de sumar 100 pasajeros corriendo cada uno su propia regla, no de una fórmula única.

## 3. Qué datos tiene que guardar cada pasajero (el "agente")

Para programar a cada pasajero necesitamos que cada uno tenga guardado:

- **Ubicación** en el avión (en qué fila está parado o sentado).
- **Destino**: su fila y lado asignado (ventana o pasillo).
- **Si tiene carry-on** o no (se sortea con probabilidad *p*, dato del problema).
- **Velocidad** de movimiento (depende de si tiene carry-on: 3 seg/fila sin carry-on, 6 seg/fila con carry-on — esto ya lo da la consigna).
- **Estado**: sentado / parado / caminando / bloqueado esperando que otro se levante.

## 4. Los 3 tiempos que la consigna nos pide inventar (y cómo los justificamos)

La consigna da las reglas de movimiento, pero deja sin definir tres tiempos. En vez de inventarlos "a ojo", buscamos papers académicos sobre boarding de aviones que ya midieron esto con pasajeros reales, y los usamos como base.

Usamos **distribuciones triangulares** cuando el estudio nos daba un mínimo, un máximo, Y un promedio (o sea, evidencia de que hay un valor "más común" dentro del rango). Usamos **uniforme** cuando solo teníamos dos números sueltos de dos estudios distintos, sin ninguna pista de cuál era más probable — en ese caso, inventar un valor "típico" sería agregar información que no tenemos.

| Qué representa | Distribución | Valores (segundos) | Fuente |
|---|---|---|---|
| Pasajero de pasillo se para y deja pasar al de ventana | Triangular | mín=9, moda=10, máx=13 | Schultz (2017), SAE Technical Paper 2017-01-2113 |
| Pasajero se sienta sin ningún bloqueo | Triangular | mín=2, moda=3, máx=4 | Schultz (2017), misma fuente |
| Pasajero guarda el carry-on y bloquea el pasillo | Uniforme | entre 13.9 y 25 | Schultz (2017) dio 13.9 s; Qiang et al. (2014), *Journal of Air Transport Management*, dieron 25 s |

**¿Qué es una distribución triangular?** Se arma con tres números: un mínimo, un máximo, y un valor "más probable" en el medio (que no tiene por qué estar justo en el centro). A diferencia de la uniforme (donde cualquier valor del rango es igual de probable), en la triangular los valores cercanos al "más probable" pesan más.

**Dato para validar resultados más adelante:** en un experimento real con pasajeros de carne y hueso, Steffen (2011) midió los tiempos totales de embarque por política: Back-to-Front 6:11 min, Random 4:44 min, WILMA 4:13 min, Steffen 3:36 min. Sirve como referencia para chequear que nuestros resultados de simulación tengan un orden de magnitud razonable.

## 5. Las 4 políticas de embarque, explicadas simple

- **Back-to-Front:** se llena el avión de atrás hacia adelante, en bloques de filas (por ejemplo, últimas 5 filas primero, después las siguientes 5, etc.), con orden random dentro de cada bloque. *(Falta decidir cuántos bloques usar — es una decisión de diseño nuestra.)*
- **Random:** no hay ningún orden. Cada pasajero sube en cualquier momento, sin importar fila ni asiento.
- **WILMA (Window-Middle-Aisle):** no es por fila — es por tipo de asiento en *todo* el avión a la vez. Primero suben todos los de ventanilla (de cualquier fila), después todos los de pasillo. (Normalmente hay un paso intermedio de "asiento del medio", pero nuestro avión no tiene asiento del medio, así que se simplifica a 2 grupos.)
- **Steffen Method:** la más elaborada. Orden: ventanilla filas impares → ventanilla filas pares → pasillo filas impares → pasillo filas pares (en nuestro avión sin asiento del medio, se reduce a 4 grupos en vez de 6). La idea es que nadie en el mismo grupo esté sentado al lado de otro del mismo grupo, así nadie se bloquea. En el experimento real de Steffen, este método fue el doble de rápido que Back-to-Front.

## 6. Qué falta para terminar el diseño (antes de programar)

1. Definir cómo avanza el "reloj" de la simulación (¿en pasos fijos de 1 segundo, o saltando directamente al próximo evento?).
2. Traducir cada una de las 4 políticas en un algoritmo concreto que genere el orden de embarque.
3. Implementar todo en Python: el motor de simulación + una visualización de los pasajeros subiendo.
4. Correr muchas simulaciones (Monte Carlo) por política y calcular tiempo esperado, desvío estándar, y el error de la estimación.
5. Ver qué pasa si *p*=0 (nadie con carry-on) o *p*=1 (todos con carry-on).
6. Investigar cuánto le cuesta a una aerolínea una demora de 30 minutos, y si conviene dejar asientos vacíos o acelerar el embarque.
7. (Bonus 30%) Explorar trade-offs o ideas de negocio propias, testeadas con el modelo.
8. Armar las 15 slides y ensayar la exposición oral de 15 minutos.

**Fecha importante:** Nicolás anuncia la fecha de presentación de cada grupo durante la semana del 21 de septiembre — o sea, la semana que viene. Conviene tener el modelo y una implementación funcionando antes de esa semana.
