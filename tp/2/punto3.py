"""
TP2 - Punto 3: limite de 300 unidades/mes de produccion propia + tercerizacion
de hasta 200 unidades/mes a $540 por unidad.

Sobre el modelo del punto 2 se agrega la variable w_{it} (unidades tercerizadas
del producto i en el mes t, entera) y:
    balance:   s_{i,t-1} + 10 y_{it} + w_{it} - d_{it} = s_{it}
    limite:    sum_i w_{it} <= 200                    para todo t
    objetivo:  + 540 * sum w_{it}
"""

import pandas as pd
import pulp

from punto1 import SOLVER, TAMANIO_LOTE, construir_modelo, leer_demanda
from punto2 import agregar_limite_mensual

COSTO_TERCERIZADO = 540   # $ por unidad tercerizada
LIMITE_TERCERIZADO = 200  # unidades/mes entre todos los productos


def agregar_tercerizacion(m, d, costo=COSTO_TERCERIZADO, limite=LIMITE_TERCERIZADO):
    productos, T = d["productos"], d["T"]
    w = pulp.LpVariable.dicts("terc", (productos, T), lowBound=0, upBound=limite,
                              cat="Integer")
    # Las unidades tercerizadas entran al balance de stock como produccion.
    for i in productos:
        for t in T:
            m.constraints[f"bal_{i}_{t}"].addterm(w[i][t], 1)
    for t in T:
        m += pulp.lpSum(w[i][t] for i in productos) <= limite, f"limterc_{t}"
    m.setObjective(m.objective + pulp.lpSum(costo * w[i][t] for i in productos for t in T))
    d["terc"] = w
    return m


def modelo_punto3(demanda):
    m, d = construir_modelo(demanda)
    agregar_limite_mensual(m, d)
    agregar_tercerizacion(m, d)
    return m, d


def tablas(d):
    P, T, meses = d["productos"], d["T"], d["meses"]
    val = lambda v: int(round(v.value()))
    prod = pd.DataFrame([[TAMANIO_LOTE * val(d["lotes"][i][t]) for i in P] for t in T],
                        index=meses, columns=P)
    terc = pd.DataFrame([[val(d["terc"][i][t]) for i in P] for t in T],
                        index=meses, columns=P)
    stock = pd.DataFrame([[val(d["stock"][i][t]) for i in P] for t in T],
                         index=meses, columns=P)
    for df in (prod, terc, stock):
        df["Total"] = df.sum(axis=1)
    return prod, terc, stock


def resumen(prod, terc, stock):
    return pd.DataFrame({"Propia": prod["Total"], "Tercerizada": terc["Total"],
                         "Demanda": prod["Total"] + terc["Total"]
                         - stock["Total"] + stock["Total"].shift(fill_value=0),
                         "Stock": stock["Total"]})


def tabla_latex(df, archivo):
    cols = " ".join("r" for _ in df.columns)
    lineas = [f"\\begin{{tabular}}{{l{cols}}}", "\\toprule",
              "Mes & " + " & ".join(df.columns) + " \\\\", "\\midrule"]
    for mes, fila in df.iterrows():
        lineas.append(f"{mes} & " + " & ".join(str(int(v)) for v in fila) + " \\\\")
    lineas += ["\\midrule", "Total & " + " & ".join(
        str(int(df[c].sum())) if c != "Stock" else "" for c in df.columns) + " \\\\",
        "\\bottomrule", "\\end{tabular}"]
    with open(archivo, "w") as f:
        f.write("\n".join(lineas) + "\n")


def reportar(m, d, sufijo):
    estado = pulp.LpStatus[m.status]
    print(f"Estado: {estado}")
    if estado != "Optimal":
        return None
    costo = pulp.value(m.objective)
    prod, terc, stock = tablas(d)
    res = resumen(prod, terc, stock)
    print(f"Costo total optimo: $ {costo:,.0f}")
    print(f"Unidades propias: {prod['Total'].sum()}  tercerizadas: {terc['Total'].sum()}")
    print(f"Stock maximo: {stock['Total'].max()}")
    print("\nResumen mensual:")
    print(res.to_string())
    print("\nTercerizacion por producto:")
    print(terc[terc["Total"] > 0].to_string())
    tabla_latex(res, f"tabla_resumen_{sufijo}.tex")
    tabla_latex(terc[terc["Total"] > 0], f"tabla_terc_{sufijo}.tex")
    return dict(costo=costo, propia=int(prod["Total"].sum()),
                terc=int(terc["Total"].sum()), stock_max=int(stock["Total"].max()))


if __name__ == "__main__":
    m, d = modelo_punto3(leer_demanda())
    m.solve(SOLVER)
    reportar(m, d, "p3")
