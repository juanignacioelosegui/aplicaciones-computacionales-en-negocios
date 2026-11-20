"""
TP2 - Punto 1: modelo de lot sizing (MILP).

Minimiza el costo total de produccion sujeto a:
  - lotes de 10 unidades por producto y mes,
  - capacidad de 120 unidades/mes por producto,
  - capacidad total de deposito de 900 unidades,
  - stock inicial nulo,
  - satisfaccion de toda la demanda.

Uso: python punto1.py
"""

import pandas as pd
import pulp

ARCHIVO_DATOS = "datos.xlsx"
COSTO_UNITARIO = 370      # $ por unidad producida
TAMANIO_LOTE = 10         # unidades por lote
LOTES_MAX = 12            # 120 unidades/mes => 12 lotes
CAPACIDAD_DEPOSITO = 900  # unidades totales en stock

# HiGHS resuelve todas las instancias del TP en segundos; CBC (el solver por
# defecto de PuLP) no logra cerrar el gap en algunas del punto 5.
SOLVER = pulp.HiGHS(msg=False)


def leer_demanda(archivo=ARCHIVO_DATOS):
    df = pd.read_excel(archivo)
    df = df.set_index(df.columns[0])
    df.columns = [c.replace("Producto ", "") for c in df.columns]
    return df


def construir_modelo(demanda):
    meses = list(demanda.index)
    productos = list(demanda.columns)
    T = range(len(meses))

    m = pulp.LpProblem("lot_sizing_punto1", pulp.LpMinimize)

    # Variables: cantidad de lotes (entera) y stock al final de cada mes.
    lotes = pulp.LpVariable.dicts(
        "lotes", (productos, T), lowBound=0, upBound=LOTES_MAX, cat="Integer"
    )
    stock = pulp.LpVariable.dicts("stock", (productos, T), lowBound=0, cat="Continuous")

    # Produccion en unidades = 10 * lotes  (expresion auxiliar)
    prod = {(i, t): TAMANIO_LOTE * lotes[i][t] for i in productos for t in T}

    # Objetivo: costo total de produccion.
    m += pulp.lpSum(COSTO_UNITARIO * prod[i, t] for i in productos for t in T)

    # Balance de stock: stock_{t-1} + prod_t - demanda_t = stock_t  (stock_{-1} = 0)
    for i in productos:
        for t in T:
            anterior = stock[i][t - 1] if t > 0 else 0
            m += anterior + prod[i, t] - demanda.iloc[t][i] == stock[i][t], f"bal_{i}_{t}"

    # Capacidad del deposito: stock total al final de cada mes.
    for t in T:
        m += pulp.lpSum(stock[i][t] for i in productos) <= CAPACIDAD_DEPOSITO, f"dep_{t}"

    return m, dict(meses=meses, productos=productos, T=T, lotes=lotes, stock=stock,
                   prod=prod, demanda=demanda)


def resolver(m, d):
    m.solve(SOLVER)
    estado = pulp.LpStatus[m.status]
    print(f"Estado: {estado}")
    if estado != "Optimal":
        return None
    print(f"Costo total optimo: $ {pulp.value(m.objective):,.0f}")

    prod_v = pd.DataFrame(
        [[TAMANIO_LOTE * int(round(d["lotes"][i][t].value())) for i in d["productos"]]
         for t in d["T"]], index=d["meses"], columns=d["productos"])
    stock_v = pd.DataFrame(
        [[int(round(d["stock"][i][t].value())) for i in d["productos"]]
         for t in d["T"]], index=d["meses"], columns=d["productos"])
    prod_v["Total"] = prod_v.sum(axis=1)
    stock_v["Total"] = stock_v.sum(axis=1)

    print("\nProduccion (unidades):")
    print(prod_v.to_string())
    print("\nStock a fin de mes (unidades):")
    print(stock_v.to_string())
    print(f"\nProduccion total: {prod_v['Total'].sum()} unidades")
    print(f"Demanda total:    {int(d['demanda'].values.sum())} unidades")
    print(f"Stock maximo en deposito: {stock_v['Total'].max()} unidades")
    exportar_latex(prod_v, stock_v, pulp.value(m.objective), d)
    return prod_v, stock_v


def exportar_latex(prod_v, stock_v, costo, d):
    """Genera los fragmentos .tex que incluye informe.tex."""
    def tabla(df, archivo):
        cols = " ".join("r" for _ in df.columns)
        lineas = [f"\\begin{{tabular}}{{l{cols}}}", "\\toprule",
                  "Mes & " + " & ".join(df.columns) + " \\\\", "\\midrule"]
        for mes, fila in df.iterrows():
            lineas.append(f"{mes} & " + " & ".join(str(int(v)) for v in fila) + " \\\\")
        lineas += ["\\bottomrule", "\\end{tabular}"]
        with open(archivo, "w") as f:
            f.write("\n".join(lineas) + "\n")

    tabla(prod_v, "tabla_produccion.tex")
    tabla(stock_v, "tabla_stock.tex")
    with open("resultados.tex", "w") as f:
        f.write(f"\\newcommand{{\\costoOptimo}}{{{costo:,.0f}}}\n".replace(",", "."))
        f.write(f"\\newcommand{{\\demandaTotal}}{{{int(d['demanda'].values.sum())}}}\n")
        f.write(f"\\newcommand{{\\stockMaximo}}{{{int(stock_v['Total'].max())}}}\n")


if __name__ == "__main__":
    demanda = leer_demanda()
    modelo, datos = construir_modelo(demanda)
    resolver(modelo, datos)
