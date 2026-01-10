from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path
from datetime import datetime

app = FastAPI(title="Predicción de Retrasos de Vuelos", version="1.0.0")

# ---------------------------
# Rutas de los modelos
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
XGB_PATH = BASE_DIR / "model" / "xgb_model.joblib"
CAT_PATH = BASE_DIR / "model" / "cat_model.joblib"

# ---------------------------
# Cargar ambos modelos
# ---------------------------
xgb_model = joblib.load(XGB_PATH)
cat_model = joblib.load(CAT_PATH)

# ---------------------------
# Modelo de entrada
# ---------------------------
class FlightInput(BaseModel):
    aerolinea: str
    origen: str
    destino: str
    fecha_partida: str
    distancia_km: float

# ---------------------------
# Endpoint raíz (opcional)
# ---------------------------
@app.get("/")
def root():
    return {"message": "API de predicción de retrasos funcionando"}

# ---------------------------
# Endpoint de predicción
# ---------------------------
@app.post("/predict")
def predict(flight: FlightInput):
    # ---------------------------
    # 1. Mapear aerolínea a retraso
    # ---------------------------
    aerolinea_map = {"AZ": 0.2, "LA": 0.3, "JJ": 0.25}
    retraso_aerolinea = aerolinea_map.get(flight.aerolinea, 0.1)

    # ---------------------------
    # 2. Mapear aeropuertos a retraso del sistema
    # ---------------------------
    aeropuerto_map = {"GRU": 0.3, "GIG": 0.25, "SCL": 0.2}
    retraso_sistema = aeropuerto_map.get(flight.origen, 0.1) + aeropuerto_map.get(flight.destino, 0.1)

    # ---------------------------
    # 3. Procesar fecha/hora
    # ---------------------------
    fecha = datetime.fromisoformat(flight.fecha_partida)
    es_madrugada = 1 if fecha.hour < 6 else 0
    retraso_avion_tardio = 0.2 if es_madrugada else 0.4

    # ---------------------------
    # 4. Distancia como proxy de clima
    # ---------------------------
    retraso_clima = 0.3 if flight.distancia_km > 1000 else 0.1

    # ---------------------------
    # 5. Construir features como espera el modelo
    # ---------------------------
    features = np.array([[retraso_avion_tardio,
                          retraso_aerolinea,
                          retraso_sistema,
                          retraso_clima]])

    # ---------------------------
    # 6. Ensemble de modelos
    # ---------------------------
    proba_xgb = xgb_model.predict_proba(features)[:, 1]
    proba_cat = cat_model.predict_proba(features)[:, 1]
    proba_ensemble = (proba_xgb + proba_cat) / 2

    # ---------------------------
    # 7. Resultado final
    # ---------------------------
    probabilidad = round(float(proba_ensemble[0]), 2)
    prevision = "Retrasado" if probabilidad > 0.6 else "A tiempo"

    return {"prevision": prevision, "probabilidad": probabilidad}