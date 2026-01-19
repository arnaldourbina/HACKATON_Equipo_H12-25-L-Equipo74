import joblib
import pandas as pd

# ---------------------------
# 1. Cargar el modelo CatBoost entrenado
# ---------------------------
model = joblib.load("ds/model/cat_model.joblib")

print("✅ Modelo cargado:", type(model))

# ---------------------------
# 2. Crear un ejemplo ficticio con las mismas columnas que el entrenamiento
# ---------------------------
ejemplo = pd.DataFrame({
    "AEROLINEA": ["AA"],
    "AEROPUERTO_ORIGEN": ["LAX"],
    "AEROPUERTO_DESTINO": ["PBI"],
    "DISTANCIA": [3000],
    "ANO": [2015],
    "MES": [1],
    "DIA": [1],
    "ES_FIN_DE_SEMANA": [0],
    "TEMPORADA": ["Verano"],
    "HORA_LLEGADA": [14],
    "FRANJA_HORARIA_LLEGADA": ["Tarde"],
    "LLEGADA_PROGRAMA": [14],
    "FRANJA_LLEGADA_PROGRAMA": ["Tarde"]
})

# ---------------------------
# 3. Predicción con umbral fijo
# ---------------------------
proba = model.predict_proba(ejemplo)[:, 1][0]
umbral = 0.7912
prevision = "Retrasado" if proba >= umbral else "Puntual"

print("Previsión:", prevision)
print("Probabilidad:", round(float(proba), 2))