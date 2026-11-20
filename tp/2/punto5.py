"""
TP2 - Punto 5: minima capacidad del deposito que hace factible el problema.

En lugar de una busqueda binaria sobre D, D pasa a ser una variable de decision:
    sum_i s_{it} <= D   para todo t,     min D
El optimo D* es exactamente la menor capacidad factible. Luego, fijando D = D*,
se minimiza el costo (optimizacion lexicografica) para obtener el plan.

Se resuelve sobre el modelo completo (punto 4) y, como referencia, sobre los de
los puntos 1 y 3. Para el punto 1 el valor se verifica ademas con un calculo
analitico del stock minimo por producto.
"""

import pandas as pd
import pulp

from punto1 import SOLVER, construir_modelo, leer_demanda
from punto3 import modelo_punto3, reportar
from punto4 import modelo_punto4


def optimo(m):
    """True si el solver probo optimalidad (no solo una solucion factible)."""
    return m.status == pulp.LpStatusOptimal and m.sol_status == pulp.LpSolutionOptimal


def capacidad_variable(m, d):
    """Reemplaza el lado derecho 900 de las restricciones de deposito por D."""
    D = pulp.LpVariable("cap_deposito", lowBound=0)
    for t in d["T"]:
        c = m.constraints[f"dep_{t}"]
        c.addterm(D, -1)       # sum s - 900 <= 0  ->  sum s - D - 900 <= 0
        c.constant = 0         # ->  sum s - D <= 0
    d["D"] = D
    return D


def minima_capacidad(constructor, demanda):
    m, d = constructor(demanda)
    costo = m.objective
    D = capacidad_variable(m, d)

    # Etapa 1: minimizar D.
    m.setObjective(D)
    m.solve(SOLVER)
    if not optimo(m):
        return None
    d_min = round(D.value())

    # Etapa 2: con D fijo en su minimo, minimizar el costo.
    m += D <= d_min, "fija_D"
    m.setObjective(costo)
    m.solve(SOLVER)
    assert optimo(m)
    return d_min, pulp.value(m.objective), m, d


def costo_con_deposito(constructor, demanda, cap):
    m, d = constructor(demanda)
    for t in d["T"]:
        m.constraints[f"dep_{t}"].constant = -cap
    m.solve(SOLVER)
    if m.status == pulp.LpStatusInfeasible:
        return None
    assert optimo(m)
    return pulp.value(m.objective)


def stock_minimo_punto1(demanda, cap=120, lote=10):
    """Stock minimo puntual por producto en el modelo del punto 1.

    Sin limite mensual conjunto, los productos son independientes. Hacia atras:
    el stock al cierre de t-1 debe cubrir lo que no se puede producir en t,
    max(0, s_t + d_t - 120), redondeado hacia arriba al residuo modulo 10 que
    impone la lotificacion (s_t = -demanda acumulada mod 10). Esa trayectoria
    minima es alcanzable a la vez para todos los productos, asi que
    D* = max_t sum_i m_it.
    """
    total = pd.Series(0, index=demanda.index)
    for i in demanda.columns:
        d = [int(v) for v in demanda[i]]
        m, sig = [0] * len(d), 0
        for t in range(len(d) - 1, -1, -1):
            m[t] = sig
            sig = max(0, sig + d[t] - cap)
            while (sig + sum(d[:t])) % lote:
                sig += 1
        assert sig == 0
        total += m
    return total


if __name__ == "__main__":
    demanda = leer_demanda()
    fmt = lambda x: f"{x:,.0f}".replace(",", ".")
    modelos = [("Punto 1 (sin limite mensual)", construir_modelo, "uno"),
               ("Punto 3 (300 propias + 200 terc.)", modelo_punto3, "tres"),
               ("Punto 4 (con minimo de 20 terc.)", modelo_punto4, "cuatro")]
    lineas = []
    for nombre, constructor, clave in modelos:
        res = minima_capacidad(constructor, demanda)
        if res is None:
            print(f"{nombre}: infactible para cualquier capacidad")
            continue
        d_min, costo, m, d = res
        costo900 = costo_con_deposito(constructor, demanda, 900)
        infact = costo_con_deposito(constructor, demanda, d_min - 5) is None
        print(f"\n{nombre}: D* = {d_min} unidades | costo con D*: $ {costo:,.0f} | "
              f"costo con D=900: $ {costo900:,.0f} | D*-5 infactible: {infact}")
        lineas += [f"\\newcommand{{\\dmin{clave}}}{{{d_min}}}",
                   f"\\newcommand{{\\costoDmin{clave}}}{{{fmt(costo)}}}",
                   f"\\newcommand{{\\costoNovecientos{clave}}}{{{fmt(costo900)}}}"]
        if clave == "cuatro":
            print("Plan con D = D*:")
            reportar(m, d, "p5")

    tot1 = stock_minimo_punto1(demanda)
    print(f"\nPunto 1 (verificacion analitica): D* = {tot1.max()} (en {tot1.idxmax()})")
    lineas.append(f"\\newcommand{{\\mesdminuno}}{{{tot1.idxmax()}}}")

    # Costo del modelo del punto 4 segun la capacidad del deposito.
    print("\nCosto del modelo del punto 4 segun la capacidad del deposito:")
    curva = []
    for cap in [700, 705, 750, 800, 850, 900, 1000, 1100, 1200]:
        c = costo_con_deposito(modelo_punto4, demanda, cap)
        curva.append(f"{cap} & " + ("infactible" if c is None else f"\\${fmt(c)}") + " \\\\")
        print(f"  D = {cap:5d}: " + ("infactible" if c is None else f"$ {c:,.0f}"))
    with open("tabla_curva_p5.tex", "w", encoding="utf-8") as f:
        f.write("\\begin{tabular}{rr}\n\\toprule\nCapacidad $D$ & Costo óptimo \\\\\n"
                "\\midrule\n" + "\n".join(curva) + "\n\\bottomrule\n\\end{tabular}\n")

    with open("resultados_p5.tex", "w") as f:
        f.write("\n".join(lineas) + "\n")
