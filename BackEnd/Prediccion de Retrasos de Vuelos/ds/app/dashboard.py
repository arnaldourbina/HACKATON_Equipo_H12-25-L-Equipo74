import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from collections import deque
import time
from datetime import datetime, date

# Config
API_URL = "http://localhost:8080/api/predict" 
RECENTS_MAX = 20

st.set_page_config(page_title="FlightOnTime Dashboard", layout="wide")

if 'recent_predictions' not in st.session_state:
    st.session_state.recent_predictions = deque(maxlen=RECENTS_MAX)

st.title("🛫 FlightOnTime - Predicción Retrasos")
st.markdown("Dashboard realtime con Java Spring Boot + CatBoost ML")

# Sidebar - CHECKBOXES
st.sidebar.header("🔮 Nueva Predicción")

# Checkbox Aerolíneas
st.sidebar.subheader("Aerolíneas")
aerolineas_options = ['AS', 'AA', 'US', 'DL', 'NK', 'UA', 'HA', 'B6', 'OO', 'EV', 'MQ',
       'F9', 'WN', 'VX']
aerolinea_seleccionada = st.sidebar.selectbox(
    "Selecciona una aerloínea", 
    aerolineas_options
)[-1]
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
       'ACK', 'MVY', 'WYS', 'DLG', 'AKN', 'GST', 'HYA']
origen = st.sidebar.selectbox("Aeropuertos origen", orígenes_options)[-1]

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
       'ACK', 'MVY', 'WYS', 'DLG', 'AKN', 'GST', 'HYA']
destino = st.sidebar.selectbox("Aeropuertos destino", destinos_options)[-1]

# Fecha/Hora
col1, col2 = st.sidebar.columns(2)
fecha_partida = st.sidebar.date_input(
    "Fecha partida", 
    value=datetime.now().date()
)
hora_partida_str = st.sidebar.text_input("Hora partida (HH:MM:SS)", value="14:00:00", max_chars=8)
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

# Botón Predict
if st.sidebar.button("🚀 Predecir Retraso", type="primary", use_container_width=True):
    fecha_iso = f"{fecha_partida}T{hora_partida.strftime('%H:%M:%S')}"
    
    payload = {
        "aerolinea": aerolinea_seleccionada,
        "origen": origen,
        "destino": destino,
        "fecha_partida": fecha_iso,
        "distancia_km": distancia_km
    }
    
    with st.spinner("CatBoost prediciendo..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            # Guarda histórico
            st.session_state.recent_predictions.appendleft({
                'timestamp': time.strftime('%H:%M:%S'),
                'aerolinea': aerolinea_seleccionada,
                'origen_destino': f"{origen}-{destino}",
                'prevision': result['prevision'],
                'probabilidad': result['probabilidad']
            })
            
            # Muestra resultado
            st.sidebar.markdown("### ✅ **Resultado**")
            st.sidebar.metric("Predicción", result['prevision'], delta=None)
            st.sidebar.metric("Prob. Retraso", f"{result['probabilidad']:.1%}", delta=None)
            st.sidebar.json(payload)
            
        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"**Error API**: {str(e)}")
        except Exception as e:
            st.sidebar.error(f"**Error**: {str(e)}")

# Main Dashboard
col_a, col_b = st.columns([2, 1])

with col_a:
    st.header("📊 Historial Predicciones")
    if st.session_state.recent_predictions:
        df = pd.DataFrame(st.session_state.recent_predictions)
        
        # Tabla responsive
        st.dataframe(
            df[['timestamp', 'aerolinea', 'origen_destino', 'prevision', 'probabilidad']]
            .style.format({'probabilidad': '{:.1%}'}), 
            use_container_width=True
        )
        
        # Gráfico barras
        fig = px.bar(
            df.tail(10), 
            x='timestamp', 
            y='probabilidad', 
            color='prevision',
            hover_data=['aerolinea', 'origen_destino'],
            title="Probabilidad Retraso (Últimas 10)",
            color_discrete_map={'Retraso': '#ef4444', 'Puntual': '#10b981'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # KPI cards
        retrasos_pct = (df['prevision'] == 'Retraso').mean() * 100
        total_preds = len(df)
        st.metric("Tasa Retrasos Prevista", f"{retrasos_pct:.1f}%", delta=None)
        st.metric("Total Predicciones", total_preds)
        
    else:
        st.info("👈 **Selecciona aerolínea/origen/destino** en sidebar y predice")

with col_b:
    st.header("📈 Stats Realtime")
    
    retrasos_count = sum(1 for p in st.session_state.recent_predictions if p['prevision'] == 'Retraso')
    puntual_count = len(st.session_state.recent_predictions) - retrasos_count
    
    col1, col2 = st.columns(2)
    col1.metric("Retrasos", retrasos_count)
    col2.metric("Puntuales", puntual_count)

# Footer
st.markdown("---")
st.markdown("*Hecho en Java Spring Boot + Python + Modelos de ML*")