import numpy as np

def simular(n=100_000, half_x=52.5, half_y=34.0, seed=1):
    rng = np.random.default_rng(seed)
    x = np.zeros(n); y = np.zeros(n)
    t = np.zeros(n, dtype=np.int64)
    activo = np.ones(n, dtype=bool)       # caminos que todavía no salieron
    por_arco = np.zeros(n, dtype=bool)

    while activo.any():
        m = activo
        k = m.sum()
        x[m] += rng.integers(0, 2, k)*2 - 1   # ±1 rápido
        y[m] += rng.integers(0, 2, k)*2 - 1
        t[m] += 1
        salio_x = np.abs(x) > half_x
        salio_y = np.abs(y) > half_y
        recien = m & (salio_x | salio_y)
        por_arco[recien & salio_x] = True     # cruzó por el eje de los arcos
        activo[recien] = False
    return t, por_arco

t, por_arco = simular()
print(f"Tiempo medio para salir: {t.mean():.1f} s (±{t.std()/np.sqrt(len(t)):.1f})")
print(f"Proporción por arco: {por_arco.mean():.4f}")