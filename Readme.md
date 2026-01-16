# Modelo de Respaldo para Predicción de Retrasos en Vuelos ✈️

## 📌 Descripción general
Este notebook tiene como objetivo **desarrollar y evaluar un modelo alternativo** que pueda ser utilizado como **respaldo** en caso de que el modelo principal de predicción falle o no esté disponible.

El enfoque está orientado a garantizar **robustez y continuidad operativa** en la predicción de retrasos de salida de vuelos.

---

## 🎯 Objetivo
- Construir un modelo secundario confiable para la **predicción de retrasos en vuelos**.
- Comparar distintas **técnicas de predicción supervisada**.
- Evaluar el impacto de **diferentes conjuntos de variables** sobre el desempeño del modelo.
- Analizar métricas clave como **Recall, Precision, F1-score y Accuracy**, con especial foco en la clase minoritaria (vuelos retrasados).

---

## 🧪 Metodología
En este notebook se realizan:
- Pruebas con distintos **algoritmos de Machine Learning**.
- Selección y validación de **features operacionales y temporales**.
- Manejo de **datasets desbalanceados**.
- Ajuste de **umbrales de decisión** para optimizar métricas relevantes al negocio.
- Evaluación comparativa entre modelos.

---

## 🛠️ Tecnologías utilizadas
- **Python**
- **Google Colab**
- **Pandas / NumPy** – Manipulación y análisis de datos
- **Scikit-learn** – Preprocesamiento y métricas
- **CatBoost / XGBoost / LightGBM** – Modelos de boosting
- **Imbalanced-learn** – Técnicas para manejo de desbalance de clases
- **Matplotlib / Seaborn** – Visualización de resultados

---

## 📊 Resultados esperados
- Un modelo alternativo **estable y reproducible**.
- Buen desempeño en la detección de vuelos con retraso.
- Métricas equilibradas que prioricen **recall y F1-score**.
- Base sólida para futuras mejoras (features históricas, datos externos, etc.).

---

## 🚀 Próximos pasos
- Incorporación de **features históricas**.
- Integración de **datos externos** (clima, congestión aeroportuaria).
- Evaluación en escenarios productivos.
- Comparación continua contra el modelo principal.

---

## 📁 Uso
Este notebook está pensado como:
- Soporte técnico
- Herramienta de validación
- Alternativa operativa en pipelines de predicción

---
