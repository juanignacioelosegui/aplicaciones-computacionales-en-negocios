import numpy as np
import pandas as pd

# --- Calibración ---
df = pd.read_csv("YPF one year daily data.csv")
df = df.dropna(subset=["Close/Last"])
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
df["Close"] = df["Close/Last"].str.replace("$", "", regex=False).str.strip().astype(float)
df = df.sort_values("Date").reset_index(drop=True)

precios = df["Close"].values
S0 = precios[-1]
retornos = precios[1:] / precios[:-1] - 1
mu = retornos.mean() * 252
sigma = retornos.std(ddof=1) * np.sqrt(252)

print(f"S0={S0:.2f}  mu={mu:.4f}  sigma={sigma:.4f}")

# --- Simulación Monte Carlo ---
def simular_ypf(S0, mu, sigma, N, dias=21, dt=1/252, seed=None):
    rng = np.random.default_rng(seed)
    S = np.full(N, S0)
    for _ in range(dias):
        Z = rng.standard_normal(N)
        S = S + S*mu*dt + S*sigma*np.sqrt(dt)*Z
    return S

for N in [100, 10_000, 1_000_000]:
    ST = simular_ypf(S0, mu, sigma, N, seed=1)
    M, D = ST.mean(), ST.std(ddof=1)
    P = np.mean((S0 - ST) > 3)
    err_M = D/np.sqrt(N)
    err_P = np.sqrt(P*(1-P)/N)
    print(f"N={N:>9}: M={M:.4f}(±{err_M:.4f})  D={D:.4f}  P={P:.4f}(±{err_P:.4f})")

print(f"ret medio diario={retornos.mean():.6f}  sd diaria={retornos.std(ddof=1):.6f}")