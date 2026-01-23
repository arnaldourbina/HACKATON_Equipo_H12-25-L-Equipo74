from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import shap
import uvicorn
from pathlib import Path
# ---------------------------
# 1. Definir app
# ---------------------------
app = FastAPI()

# ---------------------------
# 2. Definir input simplificado
# ---------------------------
class FlightInput(BaseModel):
    aerolinea: str
    origen: str
    destino: str
    fecha_partida: str
    distancia_km: float

# ---------------------------
# 3. Cargar modelo CatBoost
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

model = joblib.load(MODEL_DIR / "cat_model.joblib")

# Cargar datos de fondo para SHAP explainer
explainer = shap.TreeExplainer(model, feature_perturbation="tree_path_dependent")

@app.get("/")
def root():
    return {"message": "API FlightOnTime funcionando"}

# ---------------------------
# 4. Endpoint de predicción
# ---------------------------
@app.post("/predict")
def predict(flight: FlightInput):
    fecha = pd.to_datetime(flight.fecha_partida)
    hora_llegada = fecha.hour
    llegada_programa = fecha.hour

    # Construir DataFrame de entrada para el modelo
    df = pd.DataFrame({
        "AEROLINEA": [flight.aerolinea],
        "AEROPUERTO_ORIGEN": [flight.origen],
        "AEROPUERTO_DESTINO": [flight.destino],
        "DISTANCIA": [flight.distancia_km],
        "ANO": [fecha.year],
        "MES": [fecha.month],
        "DIA": [fecha.day],
        "ES_FIN_DE_SEMANA": [1 if fecha.weekday() in [5,6] else 0],
        "TEMPORADA": ["Verano" if fecha.month in [12,1,2] else
                      "Otoño" if fecha.month in [3,4,5] else
                      "Invierno" if fecha.month in [6,7,8] else
                      "Primavera"],
        "HORA_LLEGADA": [hora_llegada],
        "FRANJA_HORARIA_LLEGADA": [
            "Madrugada" if 0 <= hora_llegada < 6 else
            "Mañana" if 6 <= hora_llegada < 12 else
            "Tarde" if 12 <= hora_llegada < 18 else
            "Noche"
        ],
        "LLEGADA_PROGRAMA": [llegada_programa],
        "FRANJA_LLEGADA_PROGRAMA": [
            "Madrugada" if 0 <= llegada_programa < 6 else
            "Mañana" if 6 <= llegada_programa < 12 else
            "Tarde" if 12 <= llegada_programa < 18 else
            "Noche"
        ]
    })

    proba = model.predict_proba(df)[:, 1][0]

    umbral = 0.30
    prevision = "Retrasado" if proba >= umbral else "Puntual"

    return {
        "prevision": prevision,
        "probabilidad": round(float(proba), 2)
    }

@app.post("/explain")
def explain(flight: FlightInput):
    fecha = pd.to_datetime(flight.fecha_partida)
    hora_llegada = fecha.hour
    llegada_programa = fecha.hour

    df = pd.DataFrame({ 
        "AEROLINEA": [flight.aerolinea],
        "AEROPUERTO_ORIGEN": [flight.origen],
        "AEROPUERTO_DESTINO": [flight.destino],
        "DISTANCIA": [flight.distancia_km],
        "ANO": [fecha.year],
        "MES": [fecha.month],
        "DIA": [fecha.day],
        "ES_FIN_DE_SEMANA": [1 if fecha.weekday() in [5,6] else 0],
        "TEMPORADA": ["Verano" if fecha.month in [12,1,2] else
                      "Otoño" if fecha.month in [3,4,5] else
                      "Invierno" if fecha.month in [6,7,8] else "Primavera"],
        "HORA_LLEGADA": [hora_llegada],
        "FRANJA_HORARIA_LLEGADA": [
            "Madrugada" if 0 <= hora_llegada < 6 else
            "Mañana" if 6 <= hora_llegada < 12 else
            "Tarde" if 12 <= hora_llegada < 18 else "Noche"
        ],
        "LLEGADA_PROGRAMA": [llegada_programa],
        "FRANJA_LLEGADA_PROGRAMA": [
            "Madrugada" if 0 <= llegada_programa < 6 else
            "Mañana" if 6 <= llegada_programa < 12 else
            "Tarde" if 12 <= llegada_programa < 18 else "Noche"
        ]
    })

    categorical_features = [
        "AEROLINEA","AEROPUERTO_ORIGEN","AEROPUERTO_DESTINO",
        "MES","DIA","TEMPORADA","FRANJA_HORARIA_LLEGADA","FRANJA_LLEGADA_PROGRAMA"
    ]
    
    # Limpieza si aplica
    for col in categorical_features:
        df[col] = df[col].astype(str).fillna("missing")
    numeric_features = ["DISTANCIA","ANO","ES_FIN_DE_SEMANA","HORA_LLEGADA","LLEGADA_PROGRAMA"]
    for col in numeric_features:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df[col].mean())

    valores_shap = explainer.shap_values(df)
    proba = model.predict_proba(df)[:, 1][0]

    return {
        "shap_values": valores_shap[0].tolist(), 
        "base_value": float(explainer.expected_value),
        "features": df.columns.tolist(),
        "feature_values": df.iloc[0].astype(object).to_dict(),
        "probabilidad": round(float(proba), 4)
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)