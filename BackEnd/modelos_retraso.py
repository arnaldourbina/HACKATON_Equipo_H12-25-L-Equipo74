# modelos_retraso.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from joblib import dump, load
import os

# ---------------------------
# 1. Entrenamiento de modelos
# ---------------------------
def entrenar_modelos(datos):
    # Preparacion de datos
    X = datos[['RETRASO_AVION_TARDIO','RETRASO_AEROLINEA',
               'RETRASO_SISTEMA_AEREO','RETRASO_CLIMA']]
    y = datos['RETRASO_GRAVE']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Entrenamiento XGBoost
    xgb = XGBClassifier(scale_pos_weight=8.1,
                        eval_metric="logloss",
                        random_state=42)
    xgb.fit(X_train, y_train)

    # Entrenamiento CatBoost
    cat = CatBoostClassifier(iterations=500,
                             learning_rate=0.1,
                             depth=6,
                             loss_function='Logloss',
                             random_seed=42,
                             verbose=0)
    cat.fit(X_train, y_train)

    # Ensemble
    proba_xgb = xgb.predict_proba(X_test)[:,1]
    proba_cat = cat.predict_proba(X_test)[:,1]
    proba_ensemble = (proba_xgb + proba_cat) / 2

    # Evaluacion
    y_pred_final = (proba_ensemble >= 0.6).astype(int)
    cm = confusion_matrix(y_test, y_pred_final)

    print("Reporte final con umbral 0.6:")
    print(classification_report(y_test, y_pred_final))

    # Crear carpeta ds/model si no existe
    os.makedirs("ds/model", exist_ok=True)

    # Visualizacion
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Prediccion")
    plt.ylabel("Real")
    plt.savefig("ds/model/confusion_matrix.png")

    # Guardar modelos en ds/model
    dump(xgb, "ds/model/xgb_model.joblib")
    dump(cat, "ds/model/cat_model.joblib")

    return xgb, cat

# ---------------------------
# 2. Cargar modelos guardados
# ---------------------------
def cargar_modelo(ruta):
    return load(ruta)

# ---------------------------
# 3. Prediccion con nuevos datos
# ---------------------------
def predecir_retraso(modelo, nuevo_dato):
    return modelo.predict(nuevo_dato)