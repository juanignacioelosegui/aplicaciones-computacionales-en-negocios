"""
TP2 - Ejecuta los modelos Zimpl con SCIP y genera los fragmentos .tex del informe.

Toda la optimizacion la hace SCIP sobre los modelos puntoN.zpl. Este script
solo lanza SCIP, lee los archivos de solucion que escribe y arma las tablas.
No usa ninguna biblioteca externa (solo la biblioteca estandar de Python).

Uso:  python correr.py
El ejecutable de SCIP se toma de la variable de entorno SCIP, o de `scip` en el
PATH, o de la instalacion por defecto de la SCIP Optimization Suite.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

DIR = Path(__file__).resolve().parent
SALIDAS = DIR / "salidas"          # logs, soluciones y settings de cada corrida

MESES = [f"{m}/{a}" for a in (27, 28) for m in
         ("Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")]
PRODUCTOS = ["A", "B", "C", "D", "E"]
LOTE = 10


def ejecutable_scip():
    candidatos = [os.environ.get("SCIP"), shutil.which("scip"),
                  str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" /
                      "SCIPOptSuite" / "scipoptsuite-10.1.0-win-x64" / "bin" / "scip.exe")]
    for c in candidatos:
        if c and Path(c).exists():
            return c
    raise SystemExit("No se encontro SCIP. Definir la variable de entorno SCIP.")


SCIP = ejecutable_scip()


# --------------------------------------------------------------------------
# Ejecucion de SCIP
# --------------------------------------------------------------------------

def resolver(modelo, nombre, **params):
    """Resuelve `modelo` (.zpl) con SCIP. `params` sobreescribe parametros del
    modelo (opcion -D de Zimpl). Devuelve (estado, objetivo, valores)."""
    SALIDAS.mkdir(exist_ok=True)
    sol = SALIDAS / f"{nombre}.sol"
    log = SALIDAS / f"{nombre}.log"
    ajustes = SALIDAS / f"{nombre}.set"
    defs = " ".join(f"-D {k}={v}" for k, v in params.items()) or "-"
    ajustes.write_text(f'reading/zplreader/parameters = "{defs}"\n'
                       f"limits/time = 600\n")
    if sol.exists():
        sol.unlink()

    rel = lambda p: p.relative_to(DIR).as_posix()
    comandos = f"read {modelo} optimize write solution {rel(sol)} quit"
    salida = subprocess.run([SCIP, "-s", rel(ajustes), "-l", rel(log), "-c", comandos],
                            cwd=DIR, capture_output=True, text=True)
    texto = salida.stdout + salida.stderr
    m = re.search(r"SCIP Status\s*:\s*problem is solved \[(.*?)\]", texto)
    if salida.returncode != 0 or not m:
        raise RuntimeError(f"SCIP fallo en {nombre}:\n{texto[-3000:]}")
    estado = m.group(1)
    if estado != "optimal solution found":
        return estado, None, {}
    return estado, *leer_solucion(sol)


def leer_solucion(archivo):
    objetivo, valores = None, {}
    for linea in Path(archivo).read_text().splitlines():
        if linea.startswith("objective value:"):
            objetivo = float(linea.split(":")[1])
        elif linea and not linea.startswith("solution status"):
            nombre, valor = linea.split()[:2]
            valores[nombre] = float(valor)
    return objetivo, valores


def matriz(valores, var, escala=1):
    """valores['y$A#3'] -> tabla[mes][producto] (los ceros no se escriben)."""
    return [[round(escala * valores.get(f"{var}${p}#{t}", 0)) for p in PRODUCTOS]
            for t in range(1, 25)]


# --------------------------------------------------------------------------
# Salida LaTeX
# --------------------------------------------------------------------------

def miles(x):
    return f"{x:,.0f}".replace(",", ".")


def macro(nombre, valor):
    return f"\\newcommand{{\\{nombre}}}{{{valor}}}"


def tabla_tercerizacion(valores):
    """Tabla (tabular) de unidades tercerizadas por mes y producto."""
    filas = [(MESES[t], f + [sum(f)]) for t, f in enumerate(matriz(valores, "w"))
             if sum(f) > 0]
    total = [sum(f[j] for _, f in filas) for j in range(len(PRODUCTOS) + 1)]
    lineas = ["\\begin{tabular}{l" + "r" * (len(PRODUCTOS) + 1) + "}", "\\toprule",
              "Mes & " + " & ".join(PRODUCTOS) + " & Total \\\\", "\\midrule"]
    lineas += [f"{mes} & " + " & ".join(map(str, f)) + " \\\\" for mes, f in filas]
    lineas += ["\\midrule", "Total & " + " & ".join(map(str, total)) + " \\\\",
               "\\bottomrule", "\\end{tabular}"]
    return "\n".join(lineas)


def totales(valores):
    prop = sum(map(sum, matriz(valores, "y", LOTE)))
    terc = sum(map(sum, matriz(valores, "w")))
    return prop, terc


def demanda_total():
    total = 0
    for linea in (DIR / "demanda.txt").read_text().splitlines():
        if linea.strip() and not linea.startswith("#"):
            total += int(linea.split()[2])
    return total


# --------------------------------------------------------------------------
# Puntos del TP
# --------------------------------------------------------------------------

def punto1():
    estado, costo, v = resolver("punto1.zpl", "punto1")
    stock = max(map(sum, matriz(v, "s")))
    print(f"Punto 1: {estado} | costo = $ {miles(costo)} | stock maximo = {stock}")
    return [macro("costoOptimo", miles(costo)),
            macro("demandaTotal", demanda_total()),
            macro("stockMaximo", stock)]


def punto2():
    estado, _, _ = resolver("punto2.zpl", "punto2")
    print(f"Punto 2: {estado}")
    return []


def punto3y4():
    lineas = []
    for n, clave in ((3, "Tres"), (4, "Cuatro")):
        estado, costo, v = resolver(f"punto{n}.zpl", f"punto{n}")
        prop, terc = totales(v)
        print(f"Punto {n}: {estado} | costo = $ {miles(costo)} | "
              f"propias = {prop} | tercerizadas = {terc}")
        lineas += [macro(f"costoPunto{clave}", miles(costo)),
                   macro(f"propiasPunto{clave}", prop),
                   macro(f"tercPunto{clave}", terc)]
        if n == 4:
            lineas.append(macro("tablaTercCuatro", tabla_tercerizacion(v)))
    return lineas


# Variantes: parametros de punto5.zpl (etapa 1) que reproducen las
# restricciones de cada punto, y modelo de ese punto (etapa 2).
VARIANTES = {
    "uno":    (dict(W=0, limProp=600), "punto1.zpl"),  # sin terc. ni limite conjunto
    "tres":   (dict(minTerc=0),        "punto3.zpl"),  # sin minimo de 20 tercerizadas
    "cuatro": (dict(),                 "punto4.zpl"),  # modelo completo
}


def costo_con_deposito(clave, cap):
    """Etapa 2: costo minimo del modelo del punto con deposito = cap."""
    modelo = VARIANTES[clave][1]
    _, costo, v = resolver(modelo, f"punto5_{clave}_D{cap}", capDep=cap)
    return costo, v


def punto5():
    lineas = []
    for clave, (params, _) in VARIANTES.items():
        # Etapa 1: minimizar la capacidad del deposito.
        _, dmin, _ = resolver("punto5.zpl", f"punto5_{clave}_etapa1", **params)
        dmin = round(dmin)
        # Etapa 2: con deposito = Dep*, minimizar el costo.
        costo, _ = costo_con_deposito(clave, dmin)
        costo900, _ = costo_con_deposito(clave, 900)
        infact = costo_con_deposito(clave, dmin - 5)[0] is None
        print(f"Punto 5 ({clave}): Dep* = {dmin} | costo con Dep*: $ {miles(costo)} | "
              f"costo con 900: $ {miles(costo900)} | Dep*-5 infactible: {infact}")
        lineas += [macro(f"dmin{clave}", dmin),
                   macro(f"costoDmin{clave}", miles(costo)),
                   macro(f"costoNovecientos{clave}", miles(costo900))]

    print("Costo del modelo del punto 4 segun la capacidad del deposito:")
    curva = []
    for cap in [700, 705, 750, 800, 850, 900, 1000, 1100, 1200]:
        c, _ = costo_con_deposito("cuatro", cap)
        texto = "infactible" if c is None else f"\\${miles(c)}"
        curva.append(f"{cap} & {texto} \\\\")
        print(f"  Dep = {cap:5d}: {texto.replace(chr(92), '')}")
    tabla = ("\\begin{tabular}{rr}\n\\toprule\nCapacidad $D$ & Costo óptimo \\\\\n"
             "\\midrule\n" + "\n".join(curva) + "\n\\bottomrule\n\\end{tabular}")
    lineas.append(macro("tablaCurvaCinco", tabla))
    return lineas


if __name__ == "__main__":
    print(f"SCIP: {SCIP}\n")
    lineas = ["% Generado por correr.py a partir de las soluciones de SCIP. No editar.",
              *punto1(), *punto2(), *punto3y4(), *punto5()]
    (DIR / "resultados.tex").write_text("\n".join(lineas) + "\n", encoding="utf-8")

