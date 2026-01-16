from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from datetime import datetime
from typing import List
from collections import deque

app = FastAPI(title="FlightOnTime DS Service", version="0.1.0")

class FlightInput(BaseModel):
    aerolinea: str = Field(..., min_length=1)
    origen: str = Field(..., min_length=3, max_length=4)
    destino: str = Field(..., min_length=3, max_length=4)
    fecha_partida: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
    distancia_km: float = Field(..., gt=0)

class PredictionOutput(BaseModel):
    prevision: str
    probabilidad: float

class BatchInput(BaseModel):
    vuelos: List[FlightInput]

# Cargar modelo al iniciar
model = joblib.load("model/flight_delay_model.joblib")

# Memoria simple para /stats
last_predictions = deque(maxlen=500)

def build_features(fi: FlightInput) -> pd.DataFrame:
    try:
        fecha = datetime.fromisoformat(fi.fecha_partida)
    except ValueError:
        raise HTTPException(status_code=400, detail="fecha_partida inválida, use formato ISO: YYYY-MM-DDThh:mm:ss")
    hora = fecha.hour
    dia_semana = fecha.weekday()
    X = pd.DataFrame([{
        'aerolinea': fi.aerolinea,
        'origen': fi.origen,
        'destino': fi.destino,
        'hora': hora,
        'dia_semana': dia_semana,
        'distancia_km': fi.distancia_km
    }])
    return X

@app.post("/predict", response_model=PredictionOutput)
def predict(fi: FlightInput):
    X = build_features(fi)
    proba = float(model.predict_proba(X)[0, 1])
    umbral = 0.7912   # Umbral óptimo definido en entrenamiento
    pred = "Retrasado" if proba >= umbral else "Puntual"
    last_predictions.append({'ts': datetime.utcnow(), 'pred': pred})
    return {"prevision": pred, "probabilidad": round(proba, 4)}

@app.get("/stats")
def stats():
    total = len(last_predictions)
    if total == 0:
        return {"total": 0, "porcentaje_retrasado": 0.0}
    retrasados = sum(1 for p in last_predictions if p['pred'] == "Retrasado")
    return {"total": total, "porcentaje_retrasado": round(retrasados / total, 4)}

@app.post("/batch")
def batch_predict(batch: BatchInput):
    outputs = []
    umbral = 0.7912   # Usar el mismo umbral en batch
    for fi in batch.vuelos:
        X = build_features(fi)
        proba = float(model.predict_proba(X)[0, 1])
        pred = "Retrasado" if proba >= umbral else "Puntual"
        outputs.append({"prevision": pred, "probabilidad": round(proba, 4)})
    return {"resultados": outputs}