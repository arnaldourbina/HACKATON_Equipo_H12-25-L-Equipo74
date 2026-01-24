import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
from collections import deque
import time
from datetime import datetime, date

# Config
API_URL = "http://localhost:8080/api/predict"
FASTAPI_URL = "http://localhost:5000"
RECENTS_MAX = 20

with open("styles.css", "r") as css_file:
    css_content = css_file.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="FlightOnTime Dashboard", layout="wide")

if 'recent_predictions' not in st.session_state:
    st.session_state.recent_predictions = deque(maxlen=RECENTS_MAX)

st.title("🛫 FlightOnTime - Predicción Retrasos")
st.markdown("Dashboard en tiempo real para predicción de retrasos de vuelos")

# Sidebar - CHECKBOXES
st.sidebar.header("🔮 Nueva Predicción")

# Checkbox Aerolíneas
st.sidebar.subheader("Aerolíneas")
aerolineas_options = ['AS', 'AA', 'LA', 'US', 'DL', 'NK', 'UA', 'HA', 'B6', 'OO', 'EV', 'MQ',
       'F9', 'WN', 'VX', 'LATAM']
aerolinea_seleccionada = st.sidebar.selectbox(
    "Selecciona una aerloínea", 
    aerolineas_options
)
# Checkbox Aeropuertos Origen
st.sidebar.subheader("Origen")
orígenes_options = ['ANC', 'LAX', 'SFO', 'SEA', 'LAS', 'DEN', 'SLC', 'PDX', 'FAI',
       'MSP', 'PHX', 'SJU', 'PBG', 'IAG', 'PSE', 'BQN', 'ORD', 'GEG',
       'HNL', 'ONT', 'MCO', 'BOS', 'HIB', 'ABR', 'MAF', 'DFW', 'MKE',
       'IAH', 'BNA', 'BRO', 'VPS', 'BOI', 'BJI', 'SGF', 'PHL', 'SBN',
       'RDD', 'EUG', 'IAD', 'BUF', 'PWM', 'JFK', 'CRP', 'PIA', 'FAT',
       'SMF', 'AUS', 'MCI', 'ATL', 'JAX', 'MFR', 'IDA', 'MSN', 'DCA',
       'SAT', 'CHS', 'SBA', 'SMX', 'IND', 'CLE', 'GSP', 'BDL', 'ABI',
       'RIC', 'BFL', 'OMA', 'RDM', 'FLL', 'CID', 'TPA', 'SYR', 'ROC',
       'TYR', 'LAN', 'XNA', 'GSO', 'EWR', 'PBI', 'RSW', 'OAK', 'PVD',
       'RNO', 'PIT', 'ABQ', 'MIA', 'BWI', 'LGA', 'TUL', 'LIT', 'MSY',
       'OKC', 'ATW', 'PNS', 'MEM', 'TYS', 'MHT', 'SAV', 'CLT', 'GRB',
       'ABE', 'JAN', 'OAJ', 'FAR', 'ERI', 'LEX', 'CWA', 'MSO', 'TTN',
       'AMA', 'CLL', 'HOU', 'JLN', 'MLI', 'RDU', 'CVG', 'MHK', 'MOB',
       'TLH', 'BHM', 'CAE', 'TXK', 'ACY', 'DTW', 'RAP', 'TUS', 'EAU',
       'DLH', 'FSD', 'INL', 'CMX', 'SPI', 'CLD', 'COD', 'CMH', 'LRD',
       'PSC', 'CPR', 'ACV', 'DAL', 'PAH', 'MRY', 'ESC', 'ISN', 'PSP',
       'MFE', 'STL', 'BTV', 'FSM', 'AEX', 'SPS', 'ACT', 'SJT', 'MTJ',
       'GCC', 'OGG', 'SJC', 'GUC', 'ORF', 'MOT', 'MLU', 'KOA', 'SAN',
       'LAW', 'PIB', 'MGM', 'SBP', 'COS', 'LAR', 'DRO', 'BIS', 'ITO',
       'BTR', 'GRI', 'HLN', 'BZN', 'MDW', 'MDT', 'SCE', 'LIH', 'TWF',
       'BPT', 'GPT', 'STC', 'HPN', 'MLB', 'PLN', 'CIU', 'CAK', 'DSM',
       'BLI', 'SHV', 'ROW', 'FWA', 'SNA', 'ALB', 'HOB', 'LNK', 'CMI',
       'COU', 'GTF', 'EKO', 'LGB', 'AVL', 'HSV', 'SAF', 'GRR', 'SUX',
       'LFT', 'HYS', 'ELP', 'DVL', 'ISP', 'BUR', 'DAB', 'DAY', 'GRK',
       'GJT', 'BMI', 'LBE', 'ASE', 'RKS', 'GUM', 'TVC', 'ALO', 'IMT',
       'LCH', 'JNU', 'JAC', 'MEI', 'DBQ', 'GCK', 'GNV', 'BRD', 'DIK',
       'SDF', 'LBB', 'AVP', 'BTM', 'ELM', 'PIH', 'ICT', 'SUN', 'LWS',
       'VEL', 'STT', 'YUM', 'FLG', 'FCA', 'HDN', 'JMS', 'ROA', 'CHA',
       'EYW', 'MYR', 'CRW', 'MQT', 'CHO', 'ECP', 'EVV', 'EGE', 'MBS',
       'GFK', 'TOL', 'BIL', 'OTZ', 'KTN', 'STX', 'ILM', 'PUB', 'RHI',
       'CDC', 'HRL', 'SCC', 'FNT', 'LSE', 'MMH', 'APN', 'AGS', 'CEC',
       'DHN', 'WRG', 'PHF', 'CNY', 'BRW', 'GGG', 'AZO', 'SRQ', 'ORH',
       'TRI', 'VLD', 'SIT', 'BQK', 'PSG', 'FAY', 'MKG', 'CSG', 'EWN',
       'OME', 'SGU', 'RST', 'GTR', 'BET', 'ABY', 'SWF', 'ILG', 'ADK',
       'UST', 'YAK', 'CDV', 'OTH', 'ADQ', 'PPG', 'BGM', 'BGR', 'ITH',
       'ACK', 'MVY', 'WYS', 'DLG', 'AKN', 'GST', 'HYA', 'SCL']
origen = st.sidebar.selectbox("Aeropuertos origen", orígenes_options)

# Checkbox Aeropuertos Destino
st.sidebar.subheader("Destino")
destinos_options = ['SEA', 'PBI', 'CLT', 'MIA', 'ANC', 'MSP', 'DFW', 'ATL', 'IAH',
       'PDX', 'MCI', 'FLL', 'ORD', 'HNL', 'PHX', 'EWR', 'JFK', 'MCO',
       'BOS', 'BDL', 'ITO', 'SFO', 'KOA', 'OGG', 'MYR', 'DTW', 'LIH',
       'DEN', 'SJU', 'LAX', 'BWI', 'IAD', 'BQN', 'BUF', 'LGA', 'HOU',
       'SLC', 'PHL', 'SJC', 'OAK', 'LGB', 'TPA', 'DCA', 'TTN', 'BTR',
       'LAS', 'RSW', 'BRD', 'STL', 'RKS', 'MBS', 'SNA', 'MEI', 'MDW',
       'SAN', 'RIC', 'AUS', 'OTZ', 'PIT', 'JAX', 'MSY', 'ONT', 'PSP',
       'BUR', 'DAL', 'CVG', 'SMF', 'RDU', 'JMS', 'BNA', 'DSM', 'MAF',
       'BOI', 'ELP', 'TUS', 'SCC', 'HPN', 'STT', 'MDT', 'RHI', 'SBP',
       'MKE', 'JNU', 'CMH', 'CLD', 'KTN', 'CAK', 'CRP', 'CLE', 'GPT',
       'SHV', 'TYS', 'IND', 'LIT', 'SAT', 'SRQ', 'TUL', 'GRK', 'PNS',
       'BTV', 'CHS', 'DAY', 'OKC', 'SAV', 'XNA', 'COS', 'GJT', 'BZN',
       'PUB', 'HRL', 'HDN', 'MEM', 'GEG', 'ORH', 'SYR', 'GSO', 'VPS',
       'LAW', 'ACY', 'LBB', 'JAC', 'BIL', 'EUG', 'ASE', 'TVC', 'MTJ',
       'CAE', 'PVD', 'HSV', 'CDC', 'YUM', 'ABQ', 'TLH', 'MLI', 'AMA',
       'EGE', 'MOB', 'JAN', 'FWA', 'MSN', 'BIS', 'MFR', 'APN', 'BHM',
       'OMA', 'LFT', 'GRR', 'MMH', 'CEC', 'SBA', 'RNO', 'CLL', 'LEX',
       'LAN', 'DLH', 'SDF', 'FAT', 'SPS', 'SGF', 'CID', 'FSM', 'MGM',
       'MFE', 'AVP', 'SJT', 'ROA', 'LRD', 'MRY', 'AGS', 'ROC', 'AEX',
       'ISN', 'MLB', 'ORF', 'ICT', 'ECP', 'PIA', 'BPT', 'ACT', 'EYW',
       'FSD', 'MLU', 'CHA', 'WRG', 'FNT', 'DIK', 'MHK', 'CNY', 'BRW',
       'GRB', 'ATW', 'SAF', 'TYR', 'MKG', 'FLG', 'FCA', 'BTM', 'EVV',
       'DRO', 'LNK', 'DBQ', 'FAR', 'OME', 'GSP', 'GUC', 'MSO', 'TXK',
       'MOT', 'RAP', 'ISP', 'PWM', 'GGG', 'SBN', 'BFL', 'MHT', 'ROW',
       'SIT', 'CMX', 'FAY', 'ILM', 'CMI', 'ALB', 'ABI', 'GTF', 'BMI',
       'COU', 'HOB', 'GNV', 'SUN', 'SPI', 'PSG', 'BRO', 'AVL', 'TOL',
       'SGU', 'GCC', 'HLN', 'CPR', 'PIH', 'BET', 'VEL', 'RDM', 'HYS',
       'PSC', 'COD', 'INL', 'FAI', 'EKO', 'BJI', 'IDA', 'IMT', 'RST',
       'HIB', 'ABR', 'STC', 'ACV', 'ESC', 'CIU', 'SWF', 'DAB', 'TRI',
       'AZO', 'CRW', 'STX', 'GRI', 'CHO', 'GCK', 'PLN', 'LSE', 'SMX',
       'RDD', 'PHF', 'LCH', 'GTR', 'LAR', 'ERI', 'PAH', 'EAU', 'LBE',
       'BLI', 'DVL', 'CWA', 'ILG', 'OAJ', 'ABE', 'ALO', 'ABY', 'DHN',
       'TWF', 'ADK', 'ELM', 'VLD', 'PIB', 'SUX', 'GUM', 'SCE', 'UST',
       'BQK', 'JLN', 'LWS', 'MQT', 'EWN', 'CSG', 'PBG', 'PSE', 'IAG',
       'YAK', 'CDV', 'OTH', 'ADQ', 'PPG', 'GFK', 'BGM', 'BGR', 'ITH',
       'ACK', 'MVY', 'WYS', 'DLG', 'AKN', 'GST', 'HYA', 'SCL']
destino = st.sidebar.selectbox("Aeropuertos destino", destinos_options)

# Fecha/Hora
col1, col2 = st.sidebar.columns(2)
hoy = date.today()
fecha_partida = st.sidebar.date_input(
    "Fecha partida", 
    value=hoy,
    max_value=hoy
)
hora_partida_str = st.sidebar.text_input("Hora partida (HH:MM:SS)", value="12:00:00", max_chars=8)
hora_partida = datetime.strptime(hora_partida_str, "%H:%M:%S").time()

# Distancia
distancia_km = st.sidebar.number_input(
    "Distancia (km)", 
    min_value=90, 
    max_value=999999, 
    value=4000, 
    step=50,
    help="Ingresa la distancia entre aeropuertos"
)

email_usuario = st.sidebar.text_input(
    "📧 Email para alertas (opcional)", 
    placeholder="tucorreo@gmail.com",
    help="Ingresa tu correo y recibe una notificación si el retraso es mayor a 30min"
)

# Predict
if st.sidebar.button("Predecir Retraso", type="primary", width='stretch'):
    fecha_iso = f"{fecha_partida}T{hora_partida.strftime('%H:%M:%S')}"
    
    payload = {
        "aerolinea": aerolinea_seleccionada,
        "origen": origen,
        "destino": destino,
        "fecha_partida": fecha_iso,
        "distancia_km": distancia_km
    }

    with st.container():
        progress_container = st.container()
        status_container = st.container()
        
        progress_bar = progress_container.progress(0)
        status_text = status_container.empty()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2: 
            st.markdown("### 🚀 **Prediciendo...**")
            st.markdown("**" + aerolinea_seleccionada + " " + origen + "→" + destino + "**")
        
        status_text.info("🔗 Conectando backend Java...")
        progress_bar.progress(25)
        time.sleep(1.5)
        
        status_text.info("🧠 Cargando modelo ML...")
        progress_bar.progress(50)
        time.sleep(1.5)
        
        status_text.info("⚡ Calculando riesgo retraso...")
        progress_bar.progress(85)

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        progress_bar.progress(100)
        status_text.success("✅ **¡Predicción lista!**")
        time.sleep(0.8)

        if result['prevision'] == 'Puntual':
            st.balloons()
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.success(f"🟢 **¡Vuelo PUNTUAL!** 🎉\n Probabilidad de puntualidad: {result['probabilidad']:.1%}")
        else:
            st.snow()            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.error(f"🔴 **¡Vuelo RETRASADO!** ⚠️\n Probabilidad de retraso: {result['probabilidad']:.1%}")

        st.session_state.recent_predictions.appendleft({
            'timestamp': time.strftime('%H:%M:%S'),
            'aerolinea': aerolinea_seleccionada,
            'origen_destino': f"{origen}-{destino}",
            'prevision': result['prevision'],
            'probabilidad': result['probabilidad']
        })
        
        st.sidebar.markdown("### **Resultado**")
        st.sidebar.metric("Predicción", result['prevision'], delta=None)
        st.sidebar.metric("Prob. Retraso", f"{result['probabilidad']:.1%}", delta=None)

        if result['probabilidad'] > 0.30 and email_usuario:
            with st.spinner("📤 Enviando alerta por email..."):
                alert_payload = {
                    "to_email": email_usuario,
                    "vuelo_data": {
                        "aerolinea": aerolinea_seleccionada,
                        "origen": origen,
                        "destino": destino,
                        "fecha_partida": fecha_iso,
                        "distancia_km": distancia_km
                    },
                    "probabilidad": result['probabilidad']
                }
                
                alert_response = requests.post(
                    f"{FASTAPI_URL}/send-alert", 
                    json=alert_payload, 
                    timeout=10
                )
                
                if alert_response.status_code == 200:
                    st.balloons()
                    st.success(f"✅ ¡Alerta enviada a {email_usuario}! 📧")
                else:
                    st.warning("⚠️ Error al enviar el email")
        else:
            if result['probabilidad'] <= 0.30:
                st.info("Probabilidad de retraso baja, no es necesario enviar una alerta.")
            
    
    except Exception as e:
        progress_bar.empty()
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.error(f"❌ **Error predicción**: No se logro establecer conexión con el servidor.")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"**Error API**: {str(e)}")
    time.sleep(5)
    st.rerun()

# Sidebar - Funcion Batch Predict.
st.sidebar.markdown("---")
st.sidebar.header("⚡ **Predicción en lote**")


uploaded_file = st.sidebar.file_uploader(
    "Sube el archivo CSV que contiene los Vuelos", 
    type="csv",
    help="El archivo DEBE ser -> aerolinea,origen,destino,fecha_partida,distancia_km en formato csv."
)
if uploaded_file is not None:
    df_preview = pd.read_csv(uploaded_file)
    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.button("**Vista Previa**", type="secondary"):
            st.sidebar.dataframe(df_preview.head(), width='stretch')
    with col_btn2:
        if st.button("**Predecir Lote**", type="primary"):
            with st.spinner("Procesando lote..."):
                try:
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                    response = requests.post(
                        f"{API_URL}/batch",
                        files=files,
                        timeout=30
                    )
                    response.raise_for_status()

                    st.sidebar.download_button(
                        label="📥 **Descargar Predicciones**",
                        data=response.content,
                        file_name=f"archivo_con_{len(df_preview)}_vuelos_predichos.csv",
                        mime="text/csv",
                        width='stretch'
                    )
                    st.sidebar.success(f"**¡{len(df_preview)} predicciones listas!**")
                except Exception as e:
                    st.error(f"Error batch: {str(e)}")
st.sidebar.markdown("---")

# Main Dashboard
col_a, col_b = st.columns([2, 1])

with col_a:
    st.header("Historial de Predicciones")
    if st.button("Actualizar tabla", key="load_history"):
        try:
            response = requests.get("http://localhost:8080/api/history", timeout=5)
            response.raise_for_status()
            h2_data = response.json()
            
            # Convierte a df
            df = pd.DataFrame(h2_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['origen_destino'] = df['origen'] + '→' + df['destino']
            df['probabilidad'] = df['probabilidad'].astype(float)
            
            st.session_state.h2_history = df.to_dict('records')
            st.success(f"✅ {len(df)} predicciones cargadas desde H2!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error en la base de datos: No se logró establecer conexión con el servidor.")
    
    df = pd.DataFrame(st.session_state.get('h2_history', st.session_state.get('recent_predictions', [])))
    
    if not df.empty:
        st.dataframe(
            df[['timestamp', 'aerolinea', 'origen_destino', 'prevision', 'probabilidad']]
            .style.format({'probabilidad': '{:.1%}'}),
            width='stretch'
        )
        
        df_plot = df.tail(20).copy()
        df_plot['reciente'] = range(len(df_plot)-1, -1, -1)
        df_plot['tiempo_rel'] = df_plot['reciente'].apply(lambda x: f"Hace {x} pred.")
        
        fig = px.bar(
            df_plot, x='tiempo_rel', y='probabilidad', color='prevision',
            hover_data=['aerolinea', 'origen_destino'],
            title="Grafico interactivo de predicciones",
            labels={'probabilidad': '% Riesgo'},
            color_discrete_map={'Retraso': "#df2424", 'Puntual': "#0fce5f"},
            height=300
        )
        fig.update_xaxes(title="Reciente ←")
        st.plotly_chart(fig, width='stretch')
        
        retrasos_pct = (df['prevision'] == 'Retraso').mean() * 100

with col_b:
        st.header("Metricas de predicciones hoy")
        if st.button("Actualizar metricas", key="Actualiza_metricas"):
            try:
                response = requests.get("http://localhost:8080/api/stats")
                stats_data = response.json()
                
                st.session_state.stats_data = stats_data
                
                st.success("Estadisticas actualizadas desde la base de datos!")
                st.rerun()
            except requests.exceptions.RequestException as e:
                st.session_state.stats_data = None
                st.error(f"Servicio Inaccesible: No se logró establecer conexión con el servidor.")
            except Exception as e:
                st.session_state.stats_data = None
                st.error(f"Error: {str(e)}")

        if hasattr(st.session_state, 'stats_data') and st.session_state.stats_data:
            stats = st.session_state.stats_data

            col1, col2 = st.columns(2)
            col1.metric("Retrasos", stats['retrasados'])
            col2.metric("Puntuales", stats['totalPredicciones'] - stats['retrasados'])

            st.metric("Tasa Retraso", f"{stats['porcentajeRetraso']:.1f}%")
            st.metric("Total Predicciones Hoy", stats['totalPredicciones'])
            st.caption(f"Top: {stats['aerolineaTop']}")
        else:
            col1, col2 = st.columns(2)
            col1.metric("Retrasos", 0)
            col2.metric("Puntuales", 0)
            st.metric("Tasa Retraso", "0.0%")
            st.info("Click **Actualizar** para obtener estadísticas desde la base de datos")

st.markdown("---")
st.subheader("Explicacion de predicciones individuales:")
        
seleccion = st.selectbox(
        "Selecciona un vuelo para obtener sus metricas de explicación:",
        st.session_state.get('h2_history', []),
        format_func=lambda x: f"{x['timestamp']} | {x['aerolinea']} {x['origen']}→{x['destino']} ({x['prevision']} {float(x['probabilidad']):.0%})"
    )
        
if st.button("🔍 Explicar vuelo seleccionado", type="primary", width='stretch'):
            with st.spinner("Generando explicación SHAP..."):

                payload = {
                    "aerolinea": seleccion['aerolinea'],
                    "origen": seleccion['origen'],
                    "destino": seleccion['destino'],
                    "fecha_partida": seleccion.get('fecha_partida', '2026-01-22T14:00:00'),
                    "distancia_km": float(seleccion.get('distancia_km', 4000))
                }
                
                try:
                    response = requests.post("http://127.0.0.1:5000/explain", json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        shap_vals = np.array(data['shap_values'])
                        base_value = data['base_value']
                        features = data['features']
                        feature_values_str = list(data['feature_values'].values())
                        
                        st.markdown(f"**Análisis para:** {seleccion['aerolinea']} {seleccion['origen']}→{seleccion['destino']}")
                        
                        st.caption("Contribución de cada variable al riesgo")
                        sorted_idx = np.argsort(shap_vals)[::-1]
                        sorted_shap = shap_vals[sorted_idx]
                        sorted_features = [features[i] for i in sorted_idx]
                        
                        fig_water, ax = plt.subplots(figsize=(12, 6))
                        colors = ['green' if x < 0 else 'red' for x in sorted_shap]
                        y_pos = np.arange(len(sorted_features))
                        bars = ax.barh(y_pos, sorted_shap, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
                        for i, (bar, shap_val) in enumerate(zip(bars, sorted_shap)):
                            width = bar.get_width()
                            ax.text(width + 0.005 * np.sign(width), bar.get_y() + bar.get_height()/2,
                                    f'{shap_val:.3f}', ha='left' if width >= 0 else 'right',
                                    va='center', fontweight='bold', fontsize=10, color='black')
                        ax.axvline(x=base_value, color='orange', linestyle='--', linewidth=2, label=f'Base value: {base_value:.3f}')
                        ax.set_yticks(y_pos)
                        ax.set_yticklabels(sorted_features, fontsize=11, fontweight='bold')
                        ax.set_title("Explicación de la decisión del modelo.", fontsize=14, fontweight='bold', pad=20)
                        ax.set_xlabel("Impacto de features en Prob. Retraso", fontsize=12, fontweight='bold')
                        ax.text(0.5, -0.20, 
                        'VERDE disminuye prob. restraso | ROJO aumenta prob. retraso', 
                        transform=ax.transAxes, ha='center', va='bottom',
                        fontsize=11, fontweight='bold', 
                        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3CD', edgecolor='#FFA500', alpha=0.95))
                        ax.legend(loc='upper right')
                        ax.grid(axis='x', alpha=0.3)
                        ax.margins(y=0.02)
                        plt.tight_layout()
                        st.pyplot(fig_water)
                        plt.close()
                        
                    else:
                        st.error(f"Error SHAP API: {response.text}")
                except Exception as e:
                    st.error(f"Error conectando a SHAP: {str(e)}")
        
else:
    st.info("*En caso de no existir nada en el historial **Cargar Histórico H2** o predice nuevos vuelos para generar explicaciones.*")

# Footer
st.markdown("---")
st.markdown("*Hecho por H12-25-L-Equipo 74* para Hackathon ONE II - Latam @ NoCountry 2025-2026")