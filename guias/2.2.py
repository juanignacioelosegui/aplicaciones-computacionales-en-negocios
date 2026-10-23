"""
Guia 2 - Ejercicio 2: Volumen de la esfera unitaria en dimension N.

Se calcula el volumen de la esfera de radio 1 en dimension N
    { x en R^N : x_1^2 + ... + x_N^2 <= 1 }
por tres metodos, y se comparan en ERROR (vs. la solucion analitica)
y en TIEMPO de computo, para N = 3, 5 y 10.

Metodos:
  1) Formula analitica (valor exacto de referencia).
  2) Grilla cartesiana: se particiona cada dimension de -1 a 1 en pasos de 1/10.
  3) Monte Carlo: 10 millones de puntos uniformes en el cubo [-1,1]^N.
"""

import time
import math
import itertools
import numpy as np


# ---------------------------------------------------------------------------
# 1) FORMULA ANALITICA
# ---------------------------------------------------------------------------
# Volumen de la esfera de radio 1 en dimension N:
#
#        pi^(N/2)
#   V = -----------
#       Gamma(N/2 + 1)
#
# math.gamma generaliza el factorial a valores no enteros (necesario para N impar).
def volumen_analitico(N):
    return math.pi ** (N / 2) / math.gamma(N / 2 + 1)


# ---------------------------------------------------------------------------
# 2) GRILLA CARTESIANA
# ---------------------------------------------------------------------------
# Se arma una grilla regular de -1 a 1 con paso 0.1 (21 valores por dimension).
# Cada punto de la grilla representa un "cubito" de volumen (0.1)^N.
# Se cuentan los puntos que caen DENTRO de la esfera (suma de cuadrados <= 1)
# y se multiplica esa cantidad por el volumen del cubito.
#
# OJO: la grilla tiene 21^N puntos -> crece exponencialmente con N
#      (maldicion de la dimensionalidad). En N=10 son ~16.700 millones de
#      puntos: inviable de recorrer punto por punto. Por eso abajo se saltea.
def volumen_grilla(N, paso=0.1, limite_puntos=50_000_000):
    valores = np.arange(-1, 1 + paso / 2, paso)   # -1, -0.9, ..., 0.9, 1  (21 valores)
    n_puntos_total = len(valores) ** N

    if n_puntos_total > limite_puntos:
        # Inviable: lo reportamos como resultado, no como error.
        return None, n_puntos_total

    volumen_cubito = paso ** N
    dentro = 0
    for punto in itertools.product(valores, repeat=N):
        if sum(c * c for c in punto) <= 1:
            dentro += 1

    return dentro * volumen_cubito, n_puntos_total


# ---------------------------------------------------------------------------
# 3) MONTE CARLO
# ---------------------------------------------------------------------------
# Se tiran n_puntos puntos uniformes en el cubo [-1,1]^N (volumen del cubo = 2^N).
# La fraccion que cae dentro de la esfera, multiplicada por el volumen del cubo,
# estima el volumen de la esfera:
#
#   V_esfera ~= (puntos_dentro / puntos_totales) * 2^N
#
# Se procesa por lotes para no reventar la memoria con N grande y 10^7 puntos.
def volumen_montecarlo(N, n_puntos=10_000_000, semilla=42, lote=1_000_000):
    rng = np.random.default_rng(semilla)
    volumen_cubo = 2.0 ** N
    dentro = 0
    restantes = n_puntos

    while restantes > 0:
        m = min(lote, restantes)
        pts = rng.uniform(-1.0, 1.0, size=(m, N))     # m puntos, N coordenadas
        suma_cuadrados = np.einsum("ij,ij->i", pts, pts)  # x1^2+...+xN^2 por fila
        dentro += np.count_nonzero(suma_cuadrados <= 1.0)
        restantes -= m

    return (dentro / n_puntos) * volumen_cubo


# ---------------------------------------------------------------------------
# COMPARACION
# ---------------------------------------------------------------------------
def main():
    dimensiones = [3, 5, 10]

    print(f"{'N':>3} | {'Metodo':<12} | {'Volumen':>12} | "
          f"{'Error abs':>11} | {'Error rel':>10} | {'Tiempo (s)':>10}")
    print("-" * 78)

    for N in dimensiones:
        exacto = volumen_analitico(N)
        print(f"{N:>3} | {'Analitico':<12} | {exacto:>12.6f} | "
              f"{'-':>11} | {'-':>10} | {'-':>10}")

        # --- Grilla ---
        t0 = time.perf_counter()
        v_grilla, n_pts = volumen_grilla(N)
        t_grilla = time.perf_counter() - t0
        if v_grilla is None:
            print(f"{N:>3} | {'Grilla':<12} | {'INVIABLE':>12} | "
                  f"{'-':>11} | {'-':>10} | {'-':>10}   "
                  f"(21^{N} = {n_pts:,} puntos)")
        else:
            err_abs = abs(v_grilla - exacto)
            err_rel = err_abs / exacto
            print(f"{N:>3} | {'Grilla':<12} | {v_grilla:>12.6f} | "
                  f"{err_abs:>11.6f} | {err_rel:>9.2%} | {t_grilla:>10.3f}")

        # --- Monte Carlo ---
        t0 = time.perf_counter()
        v_mc = volumen_montecarlo(N)
        t_mc = time.perf_counter() - t0
        err_abs = abs(v_mc - exacto)
        err_rel = err_abs / exacto
        print(f"{N:>3} | {'Monte Carlo':<12} | {v_mc:>12.6f} | "
              f"{err_abs:>11.6f} | {err_rel:>9.2%} | {t_mc:>10.3f}")

        print("-" * 78)


if __name__ == "__main__":
    main()