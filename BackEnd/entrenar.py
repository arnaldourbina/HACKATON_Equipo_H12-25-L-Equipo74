import pandas as pd
from ds.modelos_retraso import entrenar_modelos

datos = pd.read_csv("ds/data/flight_clean.csv", low_memory=False)


xgb, cat = entrenar_modelos(datos)