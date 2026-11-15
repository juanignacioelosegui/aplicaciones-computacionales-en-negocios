"""
TP2 - Punto 2: se agrega un limite de produccion total de 300 unidades/mes.

Reutiliza el modelo del punto 1 agregando una sola familia de restricciones:
    sum_i 10 * y_{it} <= 300   para todo mes t

Uso: python punto2.py
"""

import pandas as pd
import pulp

from punto1 import (CAPACIDAD_DEPOSITO, COSTO_UNITARIO, LOTES_MAX, TAMANIO_LOTE,
                    construir_modelo, leer_demanda)

LIMITE_MENSUAL = 300  # unidades/mes entre todos los productos


def agregar_limite_mensual(m, d, limite=LIMITE_MENSUAL):
    for t in d["T"]:
        m += pulp.lpSum(d["prod"][i, t] for i in d["productos"]) <= limite, f"lim_{t}"
    return m


def cota_de_factibilidad(demanda, limite=LIMITE_MENSUAL):
    """Chequeo analitico: demanda acumulada vs. capacidad acumulada."""
    acum_dem = demanda.sum(axis=1).cumsum()
    acum_cap = pd.Series([(t + 1) * limite for t in range(len(demanda))],
                         index=demanda.index)
    faltante = acum_dem - acum_cap
    tabla = pd.DataFrame({"Demanda acum.": acum_dem.astype(int),
                          "Capacidad acum.": acum_cap,
                          "Faltante": faltante.astype(int)})
    return tabla


if __name__ == "__main__":
    demanda = leer_demanda()
    tabla = cota_de_factibilidad(demanda)
    print(tabla.to_string())
    primero = tabla[tabla["Faltante"] > 0]
    if len(primero):
        mes = primero.index[0]
        print(f"\nPrimer mes con demanda acumulada > capacidad acumulada: {mes} "
              f"(faltan {primero['Faltante'].iloc[0]} unidades)")
    print(f"Faltante al final del horizonte: {int(tabla['Faltante'].iloc[-1])} unidades")

    m, d = construir_modelo(demanda)
    agregar_limite_mensual(m, d)
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    print(f"\nEstado del modelo del punto 2: {pulp.LpStatus[m.status]}")
