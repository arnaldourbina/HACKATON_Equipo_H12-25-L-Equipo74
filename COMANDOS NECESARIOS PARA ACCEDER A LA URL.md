**🚀 Guía para generar la carpeta target**



**1. Clonar el repositorio**



git clone https://github.com/arnaldourbina/HACKATON\_Equipo\_H12-25-L-Equipo74.git

cd HACKATON\_Equipo\_H12-25-L-Equipo74/BackEnd/Prediccion\\ de\\ Retrasos\\ de\\ Vuelos/be



**2. Verificar dependencias**

**- Debes tener instalado Java 17+ (o la versión que uses).**

**- Debes tener Maven configurado en su sistema (mvn -v para comprobar).**



**3. Compilar el proyecto**



mvn clean install



**- 👉 Esto genera la carpeta target/ automáticamente en tu máquina, con los .class y el .jar.**



**4. Ejecutar la API Si es un proyecto Spring Boot:**



mvn spring-boot:run



**- O bien:**



java -jar target/nombre-del-jar-generado.jar



**5. Acceder a la API**



**- Por defecto estará en:**



**http://localhost:8080**



**- Si usas FastAPI en paralelo, sería:**



http://localhost:8000



**- Si tienes Swagger/OpenAPI, puede entrar a:**



http://localhost:8080/swagger-ui.html





**- o**



http://localhost:8000/docs

----------------------------------------------------------

🚀 **Guía para generar la carpeta target y model**

**- Java API:**



mvn clean install

mvn spring-boot:run



**- → Genera su propio target/.**

**------------------------------------------------------**

**- Modelo ML:**



python train\_model.py



**- → Genera su propio .joblib en models/.**

--------------------------------------------------------------





**----------------------------------------------------------------------**







**CUANDO SE CIERRA LA API Y SE INGRESA NUEVAMENTE**



**USAR BASH**



**\_ Cargar los directorios:**



cd ~/Desktop/ONEORACLE/HACKATHON/BackEnd/Prediccion\\ de\\ Retrasos\\ de\\ Vuelos









**🔧 Pasos concretos:**



**- Instalar y crear un entorno virtual. Una vez descargado e instalado:**



python3.10 -m venv venv310

source venv310/Scripts/activate   # en Git Bash o PowerShell



**- Se está creando un entorno virtual llamado venv310.**

**- Esto se hace una sola vez en la carpeta del proyecto.**

**- Dentro de esa carpeta se guardan los binarios de Python y las librerías que instales.**





**- Instalar las dependencias necesarias con:**



python -m pip install --upgrade pip

python -m pip install catboost fastapi uvicorn joblib scikit-learn pandas numpy



**- Verificar que se instalaron:**



python -m pip list



**- Allí deberías ver catboost, fastapi, uvicorn, etc.**



**- Activa el entorno virtual (ya lo tienes con (venv310)).**

**- Instala CatBoost dentro de ese entorno:**



python -m pip install catboost



**- 👉 Recuerda: en Git Bash usa python -m pip en lugar de pip.**



**- Verifica que se instaló correctamente:**



python -m pip list | grep catboost



**- Deberías ver algo como catboost 1.2.3 (o la versión más reciente).**



**Puedes instalar todo de una vez con:**



python -m pip install catboost xgboost lightgbm scikit-learn pandas numpy joblib fastapi uvicorn



**\_ Luego entrenar:**



python entrenar.py



python test\_model.py





**- Vuelve a correr el servicio:**





python -m uvicorn ds.service.predictor\_service:app --reload --host 0.0.0.0 --port 5000



**\_ Colocar la URL en la página WEB:**



http://127.0.0.1:5000/docs

