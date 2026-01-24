from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import uvicorn
import numpy as np
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from catboost import Pool
from scipy.special import expit

# ---------------------------
# 1. Definir app
# ---------------------------
load_dotenv()
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

class FlightEmail(BaseModel):
    to_email: str
    vuelo_data: dict
    probabilidad: float

# ---------------------------
# 3. Cargar modelo CatBoost
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"

model = joblib.load(MODEL_DIR / "cat_model.joblib")

def enviar_alerta_retraso(to_email: str, vuelo_data: dict, probabilidad: float):
    
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    
    if not sender_email or not sender_password:
        return {"error": "Config email no disponible"}
    
    html_content = f"""
    <html>
    <body style="font-family: Arial; max-width: 600px; margin: 0; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center;">
            <h1 style="color: white; margin: 0;">🚨 Alerta FlightOnTime</h1>
        </div>
        <div style="padding: 20px;">
            <h2 style="color: #d32f2f;">🛑 Vuelo con Riesgo de Retraso Mayor a 30 minutos.</h2>
            <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                <tr style="background: #f5f5f5;"><td style="padding: 12px;"><strong>Aerolínea:</strong></td><td style="padding: 12px;">{vuelo_data['aerolinea']}</td></tr>
                <tr><td style="padding: 12px;"><strong>Ruta:</strong></td><td style="padding: 12px;">{vuelo_data['origen']} → {vuelo_data['destino']}</td></tr>
                <tr style="background: #ff6b6b;"><td style="padding: 12px;"><strong>Probabilidad Retraso:</strong></td><td style="padding: 12px;"><strong style="color: #d32f2f; font-size: 24px;">{probabilidad:.1%}</strong></td></tr>
            </table>
            <p><em>Recomendación: Llega con tiempo de antelación, considera vuelo alternativo o comunicate con tu aerolínea para mas detalles.</em></p>
            <hr style="border: 1px solid #eee;">
            <small>FlightOnTime - Hackathon ONE II | H12-25-L-Equipo74</small>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"🚨 {vuelo_data['aerolinea']} {vuelo_data['origen']}→{vuelo_data['destino']} - Riesgo Retraso {probabilidad:.0%}"
        
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return {"status": "Email enviado ✅"}
    except Exception as e:
        return {"error": str(e)}

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
    llegada_programada = fecha.hour

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
        "LLEGADA_PROGRAMA": [llegada_programada],
        "FRANJA_LLEGADA_PROGRAMA": [
            "Madrugada" if 0 <= llegada_programada < 6 else
            "Mañana" if 6 <= llegada_programada < 12 else
            "Tarde" if 12 <= llegada_programada < 18 else
            "Noche"
        ]
    })

    categorical_features = [
        "AEROLINEA","AEROPUERTO_ORIGEN","AEROPUERTO_DESTINO",
        "MES","DIA","TEMPORADA","FRANJA_HORARIA_LLEGADA","FRANJA_LLEGADA_PROGRAMA"
    ]
    numeric_features = ["DISTANCIA","ANO","ES_FIN_DE_SEMANA","HORA_LLEGADA","LLEGADA_PROGRAMA"]

    for col in categorical_features:
        df[col] = df[col].astype(str).fillna("missing")

    for col in numeric_features:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df[col].mean())

    categorical_indices = [0, 1, 2, 5, 6, 8, 10, 12]

    pool = Pool(
        df.values.astype(object),
        cat_features=categorical_indices
    )

    proba = model.predict_proba(pool)[:, 1][0]

    umbral = 0.30
    prevision = "Retrasado" if proba >= umbral else "Puntual"

    print("=== INPUT DF PREDICT ===", df.to_dict(orient="records")[0])
    print("Proba PREDICT:", proba)

    return {
        "prevision": prevision,
        "probabilidad": round(float(proba), 2)
    }

@app.post("/send-alert")
def enviar_alerta_vuelo(alert: FlightEmail):
    result = enviar_alerta_retraso(alert.to_email, alert.vuelo_data, alert.probabilidad)
    if "error" in result:
        raise HTTPException(500, result["error"])
    return result

@app.post("/explain")
def explain(flight: FlightInput):
    fecha = pd.to_datetime(flight.fecha_partida)
    hora_llegada = fecha.hour
    llegada_programada = fecha.hour

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
        "LLEGADA_PROGRAMA": [llegada_programada],
        "FRANJA_LLEGADA_PROGRAMA": [
            "Madrugada" if 0 <= llegada_programada < 6 else
            "Mañana" if 6 <= llegada_programada < 12 else
            "Tarde" if 12 <= llegada_programada < 18 else "Noche"
        ]
    })

    categorical_indices = [0, 1, 2, 5, 6, 8, 10, 12]

    categorical_features = [
    "AEROLINEA","AEROPUERTO_ORIGEN","AEROPUERTO_DESTINO",
    "MES","DIA","TEMPORADA","FRANJA_HORARIA_LLEGADA","FRANJA_LLEGADA_PROGRAMA"
    ]
    numeric_features = ["DISTANCIA","ANO","ES_FIN_DE_SEMANA","HORA_LLEGADA","LLEGADA_PROGRAMA"]

    for col in categorical_features:
        df[col] = df[col].astype(str).fillna("missing")

    for col in numeric_features:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df[col].mean())

    pool = Pool(
        df.values.astype(object),
        cat_features=categorical_indices
    )

    proba = model.predict_proba(pool)[:, 1][0]

    shap_values_full = model.get_feature_importance(
        pool, type='ShapValues', thread_count=-1
    )
    shap_values = shap_values_full[0, :-1]
    base_value = shap_values_full[0, -1]
    raw_pred = base_value + shap_values.sum()

    proba_from_shap = float(expit(raw_pred))
    
    return {
        "shap_values": shap_values.tolist(),
        "base_value": float(base_value),
        "features": df.columns.tolist(),
        "feature_values": df.to_dict(orient="records")[0],
        "probabilidad": round(float(proba), 4),
        "probabilidad_shap": round(proba_from_shap, 4), 
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)