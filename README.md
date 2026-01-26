# ✈️ FlightOnTime Predicción de retrasos de vuelos.

## 📋 Descripción
FlightOnTime es un sistema de aprendizaje automático que predice retrasos en vuelos mediante un modelo CatBoost.
Ofrece predicciones individuales en tiempo real, procesamiento por lotes mediante la importación de archivos CSV, análisis estadístico y explicabilidad basada en SHAP de las predicciones individuales.
Su arquitectura de tres niveles incluye un backend Java Spring Boot que orquesta las llamadas a un servicio de aprendizaje automático Python FastAPI, todo presentado a través de un panel interactivo Streamlit.

El proyecto combina:
- **Backend en Spring Boot** para exponer endpoints REST y formularios web con Streamlit.
- **Modelo de Machine Learning en Python (scikit-learn)** entrenado con datos históricos de vuelos.

---

## 🛠️ Tecnologías utilizadas
### Backend Services
- **Java 17+** con **Spring Boot 3.2.5 framework** - **REST API** y logica de negocio.
- **H2 Database** para persistencia (in-memory).
- **Streamlit** para el front end del proyecto.
- **OpenCSV 5.9** - para procesamiento por lotes

### ML Services
- **Python 3.10+** con **FastAPI** para servicios de ML.
- Modelo de ML **CatBoost** para predicciones.
- **SHAP** para explicar las decisiones del Modelo.
- FastAPI, Uvicorn para la API de Python.
- Pandas y Joblib para el procesamiento de los datos.
- SHAP para explicabilidad.

### Frontend
**Streamlit** - Dashboard web interactivo.
Plotly Express - Visualizacion de la data.
requests - HTTP client para llamdas a la API.

---


## 📂 Estructura del proyecto
````
Prediccion-de-Retrasos-de-Vuelos/
├── be/                          # Backend en Spring Boot
│   ├── pom.xml                  # Configuración de Maven
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/flightontime/
│   │   │   │   ├── config/
│   │   │   │   │   ├── RestTemplateConfig.java
│   │   │   │   ├── controller/
│   │   │   │   │   ├── PredictController.java
│   │   │   │   ├── dto/
│   │   │   │   │   ├── ExplainOutput.java
│   │   │   │   │   └── FlightEmail.java
│   │   │   │   │   ├── FlightInput.java
│   │   │   │   │   └── PredictionOutput.java
│   │   │   │   │   ├── StatsDto.java
│   │   │   │   ├── entity/
│   │   │   │   │   ├── H2Prediction.java
│   │   │   │   ├── exception/
│   │   │   │   │   └── GlobalExceptionHandler.java
│   │   │   │   ├── repository/
│   │   │   │   │   └── H2PredictionRepository.java
│   │   │   │   ├── service/
│   │   │   │   │   └── DsClientService.java
│   │   │   │   │   └── H2PredictionService.java
│   │   │   │   │   └── H2StatsService.java
│   │   │   │   ├── util/
│   │   │   │   │   └── CSVAnalisisVuelos.java
│   │   │   │   └── FlightOnTimeApplication.java
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       ├── application.properties
│   │   │       └── templates/
│   │   │           ├── form.html
│   │   │           └── result.html
├── ds/                          # Data Science / Machine Learning
│   ├── app/
│   │   ├── dashboard.py
│   │   ├── requiremets.txt
│   │   └── main.py
│   ├── data/
│   │   └── flight_clean.csv
│   ├── model/
│   │   └── cat_model.joblib
│   │   ├── catboost_learning_curve.png
│   │   ├── xgb_model.txt
│   ├── service/
│   │   └── predictorService.py
│   │   ├── __init__.py
│   ├── modelos_retraso.py
│   └── requirements.txt
├── entrenar.py                  
├── testmodel.py
├── notebook_flight_on_time.ipynb
├── curva_aprendizaje_catboost.png
├── Manual_de_usuario - FoT Dashboard.pdf                   
└── README.md
````

## 🔎 Explicación:
- be/ → Todo el backend en Spring Boot (controladores, DTOs, streamlit, configuración).
- ds/ → Todo lo relacionado con el modelo de ML (dataset, notebooks, scripts, modelo exportado).
- model/ → Carpeta donde se guarda el modelo entrenado (cat_model.joblib).
- README.md → Guía de uso y documentación del proyecto.


## 🚀 Cómo ejecutar

### Pre-requisitos

- Java 17+.
- Maven 3.x.
- Python 3.10+.
- Git.

**Clonar el repositorio**
```bash
git clone https://github.com/arnaldourbina/HACKATON_Equipo_H12-25-L-Equipo74.git  
cd HACKATON_Equipo_H12-25-L-Equipo74/BackEnd/Prediccion\ de\ Retrasos\ de\ Vuelos
````

**Compilar y ejecutar JAVA**
```bash
cd be  
mvn clean install  
mvn spring-boot:run
````

**Setup y activación ambiente python**
```bash
cd ../ds  
python -m venv venv 
.\venv\Scripts\activate  
pip install catboost xgboost fastapi uvicorn joblib scikit-learn pandas numpy shap streamlit requests plotly pydantic matplotlib seaborn
````

**Entrenar el modelo**

```bash
cd "Prediccion de Retrasos de Vuelos"
python entrenar.py
````

**Esto genera el archivo:**

model/cat_model.joblib

**Ejecutar el backend**

```bash
cd be
mvn clean compile
mvn spring-boot:run
````

**El servidor se levanta en:**

- **http://localhost:8080/api/predict**

**Ejecutar FastAPI en Python**
```bash
cd ../ds
python app/main.py
````

**Ejecutar Dashboard streamlit**
```bash
../ds/app
streamlit run dashboard.py
````
**El servidor se levanta en:**

- **http://localhost:8501**

## 📑 EndPoints
API Endpoints y Web Services
Java Backend (Port 8080)
POST /api/predict - SPrediccion de vuelo.
POST /api/predict/batch - prediccion en lote de archivos CSV.
GET /api/stats - Obtiene estadisticas de los vuelos.
GET /api/history - Obtiene el historial de los vuelos.
Python ML Service (Port 5000)
POST /predict - Prediccion de vuelos del modelo de ML.
POST /explain - Explicacion SHAP de la decisión del modelo de ML.
Streamlit Dashboard (Port 8501)
Frontend interactivo para predicciones, prediccion en lotes, estadisticas y explicaciones SHAP.

**📑 Endpoints**

{
  "aerolinea": "AA",
  "origen": "IAG",
  "destino": "FLL",
  "fecha_partida": "2020-02-01T04:30:00",
  "distancia_km": 8550
}

{
  "aerolinea": "MQ",
  "origen": "ONT",
  "destino": "PHX",
  "fecha_partida": "2026-01-22T05:30:00",
  "distancia_km": 4430
}

{
    "aerolinea": "LA",
    "origen": "SCL",
    "destino": "JFK",
    "fecha_partida": "2026-01-12T15:00:00",
    "distancia_km": 8200
}

{
  "aerolinea": "LATAM",
  "origen": "DFW",
  "destino": "STL",
  "fecha_partida": "2026-6-15T4:50:00",
  "distancia_km": 885
}

Respuesta: {
  "prevision": "Puntual/Retrasado",
  "probabilidad": 0.xxx
}


**📊 Modelo de Machine Learning**
**- Features utilizadas:**

  > - Aerolínea
  > - Origen
  > - Destino
  > - Fecha y Hora de partida
  > - Distancia (km)

**- Target:** retrasado (0 puntual, 1 retrasado)

**- Algoritmo:** Catboost.

**- Métricas:** Accuracy, Precision, Recall, F1.

**Modelo entrenado:**
- Precisión (Precision) ≈ 0.76 → de todos los vuelos que el modelo predijo como “Grave”, el 76% realmente lo son.
- Recall (Sensibilidad) ≈ 0.77 → el modelo detecta correctamente el 77% de los vuelos con retraso grave.
- F1-score ≈ 0.76 → equilibrio entre precisión y recall.
- ROC-AUC ≈ 0.97 → excelente capacidad de discriminación global entre vuelos puntuales y retrasados.

**⚠️ Notas**

- Los datasets grandes están versionados con Git LFS.
Asegúrate de ejecutar:

git lfs install
git lfs pull

**🤝 Contribución**

- Haz un fork del repositorio.
- Crea una rama (feature/nueva-funcionalidad).
- Haz commit de tus cambios.
- Haz push a la rama.
- Abre un Pull Request.

**🌙 En resumen:**

El sistema se basa en una arquitectura de microservicios con persistencia selectiva de datos: 
las predicciones individuales se almacenan en la base de datos H2, mientras que los resultados por lotes se devuelven en forma de archivos CSV descargables. 
La arquitectura admite operaciones sincrónicas y asincrónicas, con gestión de errores y configuración adecuada de los tiempos de expiración.


**📜 Licencia**
Este proyecto se distribuye bajo la licencia MIT.

**HACKATON_Equipo_H12-25-L-Equipo74**




