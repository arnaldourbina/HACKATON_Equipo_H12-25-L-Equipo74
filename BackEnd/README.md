**Notebook_flight_on_time.ipynb**
# ✈️ FlightOnTime API

## 📌 Descripción
FlightOnTime es una aplicación que permite **predecir retrasos de vuelos** a partir de datos como aerolínea, origen, destino, fecha de partida y distancia.  
El proyecto combina:
- **Backend en Spring Boot** para exponer endpoints REST y formularios web con Thymeleaf.
- **Modelo de Machine Learning en Python (scikit-learn)** entrenado con datos históricos de vuelos.

---

## 🛠️ Tecnologías utilizadas
- **Java 17** + **Spring Boot 3.3.1**
- **Thymeleaf** para vistas HTML
- **Maven** para gestión de dependencias
- **Python 3.x** + **scikit-learn**, **pandas**, **numpy**, **catboost**
- **Joblib** para exportar el modelo entrenado
- **Git LFS** para manejar datasets grandes

---


## 📂 Estructura del proyecto
````
Prediccion-de-Retrasos-de-Vuelos/
├── be/                          # Backend en Spring Boot
│   ├── pom.xml                  # Configuración de Maven
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/flightontime/
│   │   │   │   ├── controller/
│   │   │   │   │   ├── @RestController.java
│   │   │   │   │   ├── PredictController.java
│   │   │   │   │   ├── StatsController.java
│   │   │   │   │   └── WebController.java
│   │   │   │   ├── dto/
│   │   │   │   │   ├── FlightInput.java
│   │   │   │   │   └── PredictionOutput.java
│   │   │   │   ├── exception/
│   │   │   │   │   └── GlobalExceptionHandler.java
│   │   │   │   ├── service/
│   │   │   │   │   └── DsClient.java
│   │   │   │   └── FlightOnTimeApplication.java
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       └── templates/
│   │   │           ├── form.html
│   │   │           └── result.html
│   └── target/
│       ├── classes/
│       │   ├── application.yml
│       │   ├── com/flightontime/
│       │   │   ├── controller/
|       |   |   |   |__ @RestController.class 
│       │   │   │   ├── PredictController.class
│       │   │   │   ├── StatsController.class
│       │   │   │   └── WebController.class
│       │   │   ├── dto/
│       │   │   │   ├── FlightInput.class
│       │   │   │   └── PredictionOutput.class
│       │   │   ├── exception/
│       │   │   │   └── GlobalExceptionHandler.class
│       │   │   ├── service/
│       │   │   │   └── DsClient.class
│       │   │   └── FlightOnTimeApplication.class
│       │   └── templates/
│       │       ├── form.html
│       │       └── result.html
│       ├── generated-sources/
│       │   └── annotations/
│       └── maven-status/
│           └── maven-compiler-plugin/
│               └── compile/
│                   └── default-compile/
│                       ├── createdFiles.lst
│                       └── inputFiles.lst
├── ds/                          # Data Science / Machine Learning
│   ├── app/
│   │   ├── dashboard.py
│   │   ├
│   │   └── main.py
│   ├── data/
│   │   └── flights2015.csv
│   ├── model/
│   │   └── flight_delay_model.joblib
│   ├── notebook_flight_on_time.ipynb
│   └── requirements.txt
├── README.md                    # Documentación del proyecto
└── .gitignore                   # Archivos ignorados por Git
````

## 🔎 Explicación:
- be/ → Todo el backend en Spring Boot (controladores, DTOs, vistas Thymeleaf, configuración).
  - ds/ → Todo lo relacionado con el modelo de ML (dataset, notebooks, scripts, modelo exportado).
- templates/ → Vistas HTML (form.html y result.html).
- model/ → Carpeta donde se guarda el modelo entrenado (flight_delay_model.joblib).
- README.md → Guía de uso y documentación del proyecto.


## 🚀 Cómo ejecutar

### 1. Entrenar el modelo en Python

```bash
cd ds
pip install -r requirements.txt
````

**2. Entrenar el modelo
python modelos_retraso.py

**Esto genera el archivo:**
model/flight_delay_model.joblib

**3. Ejecutar el backend**
cd be
mvnd spring-boot:run

**El servidor se levanta en:**

http://127.0.0.1:5000/docs

**📑 Endpoints**
**REST API**
**- POST /predict**
Recibe un JSON con los datos del vuelo y devuelve la predicción.

{
  "aerolinea": "LATAM",
  "origen": "SCL",
  "destino": "JFK",
  "fecha_partida": "2026-01-10T15:00:00",
  "distancia_km": 8200
}

- Respuesta:
{
  "prevision": "Retrasado",
  "probabilidad": 0.821,
  "features": {
    "aerolinea": "LATAM",
    "origen": "SCL",
    "destino": "JFK",
    "distancia_km": 8200,
    "dia_semana": 6
  }
}

**Interfaz Web**
- GET /form → muestra formulario HTML.
- POST /form → procesa datos y muestra resultado en result.html.

**📊 Modelo de Machine Learning**
**- Features utilizadas:**
> - Aerolínea
> - Origen
> - Destino
> - Hora de partida
> - Día de la semana
> - Distancia (km)
**- Target:** retrasado (0 puntual, 1 retrasado)
**- Algoritmo:** Logistic Regression con OneHotEncoder para variables categóricas.
**- Métricas:** Accuracy, Precision, Recall, F1.

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

 Este README da una guía para entrenar el modelo, correr el backend y usar tanto la API REST como el formulario web.  


**📜 Licencia**
Este proyecto se distribuye bajo la licencia MIT.





