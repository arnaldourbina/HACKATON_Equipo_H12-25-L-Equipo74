import pandas as pd
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
from ds.modelos_retraso import entrenar_modelos

# ---------------------------
# 1. Cargar datos
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "ds" / "data"   # Ajuste: apunta a ds/data
MODEL_DIR = BASE_DIR / "ds" / "model"

datos = pd.read_csv(DATA_DIR / "flight_clean.csv")

print("Columnas normalizadas:", list(datos.columns))

# ---------------------------
# 2. Entrenar modelos
# ---------------------------
xgb_pipeline, cat_model = entrenar_modelos(datos)

# ---------------------------
# 3. Guardar modelos
# ---------------------------
MODEL_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(xgb_pipeline, MODEL_DIR / "xgb_model.joblib")
joblib.dump(cat_model, MODEL_DIR / "cat_model.joblib")

print("✅ Modelos guardados en:", MODEL_DIR)

# ---------------------------
# 4. Curva de aprendizaje CatBoost
# ---------------------------
evals_result = cat_model.get_evals_result()

if "learn" in evals_result and "Logloss" in evals_result["learn"]:
    train_error = evals_result["learn"]["Logloss"]
    test_error = evals_result["validation"]["Logloss"]

    plt.figure(figsize=(8, 5))
    plt.plot(train_error, label="Train Logloss")
    plt.plot(test_error, label="Test Logloss")
    plt.xlabel("Iteraciones")
    plt.ylabel("Logloss")
    plt.legend()
    plt.title("Curva de aprendizaje CatBoost")
    plt.tight_layout()
    plt.show()

    # Guardar gráfico como PNG
    plt.savefig(MODEL_DIR / "catboost_learning_curve.png")
    print("📊 Curva de aprendizaje guardada en:", MODEL_DIR / "catboost_learning_curve.png")
else:
    print("⚠️ No se encontraron resultados de evaluación en CatBoost.")