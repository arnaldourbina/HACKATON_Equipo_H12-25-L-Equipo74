  import streamlit as st
import requests

st.title(✈️ FlightOnTime Demo")

# Campos de entrada
numero_vuelo = st.text_input("Número de vuelo (ejemplo: AZ123)")
aerolinea = st.text_input("Aerolínea (ejemplo: AZ)")
origen = st.text_input("Origen (ejemplo: GIG)")
destino = st.text_input("Destino (ejemplo: GRU)")
fecha = st.text_input("Fecha partida (YYYY-MM-DDTHH:MM:SS)", "2025-11-10T14:30:00")
distancia = st.number_input("Distancia (km)", min_value=1, value=350)

# Botón de consulta
if st.button("Consultar retraso"):
    body = {
        "numeroVuelo": numero_vuelo,
        "aerolinea": aerolinea,
        "origen": origen,
        "destino": destino,
        "fecha_partida": fecha,
        "distancia_km": distancia
    }
    try:
        resp = requests.post("http://localhost:8080/predict", json=body)
        if resp.status_code == 200:
            resultado = resp.json()

            # Mostrar resultado de forma amigable
            st.success("✅ Predicción recibida")
            st.write(f"✈️ Vuelo: {resultado['numeroVuelo']} ({resultado['aerolinea']})")
            st.write(f"📍 Ruta: {resultado['origen']} → {resultado['destino']}")
            st.write(f"🗓️ Fecha partida: {resultado['fecha_partida']}")
            st.write(f"📏 Distancia: {resultado['distancia_km']} km")

            # Mostrar estado de predicción
            if resultado.get('prediccion', 0) == 1:
                st.error("⚠️ Su vuelo tiene alta probabilidad de retraso")
            else:
                st.success("🟢 Vuelo previsto a tiempo")

            # Mostrar estado textual
            st.info(f"Estado: {resultado['status']}")

        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"No se pudo conectar al backend: {e}")