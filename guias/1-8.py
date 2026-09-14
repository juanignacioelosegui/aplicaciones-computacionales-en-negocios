import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Cargar y limpiar
df = pd.read_csv("NASDAQ100.csv")
df["observation_date"] = pd.to_datetime(df["observation_date"])
df = df.dropna(subset=["NASDAQ100"]).reset_index(drop=True)  # saca los 50 NaN
precios = df["NASDAQ100"].astype(float)

# 2. Retornos diarios: (X(t) - X(t-1)) / X(t-1)
retornos = precios.pct_change().dropna()

# 3. Histograma
plt.hist(retornos, bins=60, edgecolor="black")
plt.title("Histograma de retornos diarios del Nasdaq-100")
plt.xlabel("Retorno diario")
plt.ylabel("Frecuencia")
plt.show()

# 4. Estadísticas
print("Media:", retornos.mean())
print("Desvío estándar:", retornos.std())
print("Ratio desvío/media:", retornos.std() / retornos.mean())

# 5. Correlación entre días consecutivos
print("Autocorrelación lag-1:", retornos.autocorr(lag=1))
