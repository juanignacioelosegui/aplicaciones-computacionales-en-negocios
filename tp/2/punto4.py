"""
TP2 - Punto 4: si se terceriza un producto en un mes, se deben pedir al menos
20 unidades de ese producto en ese mes.

Se agrega una binaria u_{it} (1 si se terceriza el producto i en el mes t):
    w_{it} >= 20  * u_{it}
    w_{it} <= 200 * u_{it}
de modo que w_{it} = 0 o bien 20 <= w_{it} <= 200.
"""

import pulp

from punto1 import SOLVER, leer_demanda
from punto3 import LIMITE_TERCERIZADO, modelo_punto3, reportar

MINIMO_TERCERIZADO = 20  # unidades por producto y mes, si se terceriza


def agregar_minimo_tercerizacion(m, d, minimo=MINIMO_TERCERIZADO,
                                 maximo=LIMITE_TERCERIZADO):
    P, T, w = d["productos"], d["T"], d["terc"]
    u = pulp.LpVariable.dicts("usa_terc", (P, T), cat="Binary")
    for i in P:
        for t in T:
            m += w[i][t] >= minimo * u[i][t], f"minterc_{i}_{t}"
            m += w[i][t] <= maximo * u[i][t], f"activa_{i}_{t}"
    d["usa_terc"] = u
    return m


def modelo_punto4(demanda):
    m, d = modelo_punto3(demanda)
    agregar_minimo_tercerizacion(m, d)
    return m, d


if __name__ == "__main__":
    demanda = leer_demanda()

    m3, d3 = modelo_punto3(demanda)
    m3.solve(SOLVER)
    costo3 = pulp.value(m3.objective)

    m, d = modelo_punto4(demanda)
    m.solve(SOLVER)
    r = reportar(m, d, "p4")
    if r:
        print(f"\nCosto punto 3: $ {costo3:,.0f}")
        print(f"Costo punto 4: $ {r['costo']:,.0f}")
        print(f"Diferencia:    $ {r['costo'] - costo3:,.0f}")
