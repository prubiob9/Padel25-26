import streamlit as st
import pandas as pd
import json
import os
import time
from styles import apply_styles 

st.set_page_config(page_title="Torneito Padel 25/26", layout="wide")
apply_styles()

# --- PERSISTENCIA REAL-TIME ---
DB_FILE = "resultados_torneo.json"

def cargar_datos():
    if os.path.exists(DB_FILE):
        # Comprobar si el archivo tiene contenido
        if os.path.getsize(DB_FILE) == 0:
            return {}
        try:
            with open(DB_FILE, "r") as f: 
                return json.load(f)
        except json.JSONDecodeError:
            # Si el JSON está mal escrito, devolvemos vacío
            return {}
    return {}

def guardar_datos():
    with open(DB_FILE, "w") as f: 
        json.dump(st.session_state.resultados, f)

# IMPORTANTE: Cargamos los datos al inicio para sincronizar dispositivos
st.session_state.resultados = cargar_datos()

if 'parejas' not in st.session_state:
    st.session_state.parejas = [f"Pareja {i+1}" for i in range(6)]

# --- LÓGICA DE PROGRESIÓN ---
P = st.session_state.parejas
R = st.session_state.resultados

def get_g(m_id): return R.get(m_id)
def get_p(m_id, p1, p2): 
    gan = R.get(m_id)
    if not gan or not p1 or not p2: return None
    return p1 if gan == p2 else p2

# Nombres de partidos
labels = {
    'M1': 'Winners - Cuartos 1', 'M2': 'Winners - Cuartos 2', 'M3': 'Winners - Cuartos 3',
    'M6': 'Losers - Ronda 1', 'M4': 'Winners - Semis', 'M7': 'Losers - Ronda 2',
    'M5': 'Final Winners', 'M8': 'Losers - Semifinal', 'M9': 'Final Losers'
}

# --- MODAL: CUADRO VISUAL CORREGIDO ---
@st.dialog("🖼️ Mapa del Torneo - Especial 6", width="large")
def modal_bracket():
    R = st.session_state.resultados
    P = st.session_state.parejas

    def get_name(m_id, player_slot):
        match_data = next((m for m in partidos if m['id'] == m_id), None)
        if not match_data: return "???"
        name = match_data[player_slot]
        if not name: return match_data.get(f"{player_slot}_src", "...")
        ganador = R.get(m_id)
        if ganador and ganador == name:
            return f"<b style='color: #28a745;'>{name}</b>"
        return name

    # Generamos el HTML sin sangrías al inicio de las líneas (clave para que no salga como código)
    html = f"""
<div style='color: white; font-family: sans-serif;'>
<h3 style='text-align:center; color: #28a745; margin-bottom: 10px;'>🏆 WINNERS BRACKET</h3>
<div class="bracket-wrapper" style="display: flex; flex-direction: row; gap: 20px; justify-content: center; align-items: flex-start;">
<div class="bracket-column" style="display: flex; flex-direction: column; gap: 10px;">
<div class="status-badge">Cuartos</div>
<div class="match-box">{get_name('M1','p1')}<br><hr>{get_name('M1','p2')}</div>
<div class="match-box">{get_name('M2','p1')}<br><hr>{get_name('M2','p2')}</div>
<div class="match-box">{get_name('M3','p1')}<br><hr>{get_name('M3','p2')}</div>
</div>
<div class="bracket-column" style="display: flex; flex-direction: column; gap: 10px; padding-top: 45px;">
<div class="status-badge">Semis WB</div>
<div class="match-box" style="margin-top: 20px;">{get_name('M4','p1')}<br><hr>{get_name('M4','p2')}</div>
</div>
<div class="bracket-column" style="display: flex; flex-direction: column; gap: 10px; padding-top: 45px;">
<div class="status-badge">Final WB</div>
<div class="match-box" style="margin-top: 20px;">{get_name('M5','p1')}<br><hr>{get_name('M5','p2')}</div>
</div>
</div>
<br>
<h3 style='text-align:center; color: #f39c12; margin-top: 20px; margin-bottom: 10px;'>🔄 LOSERS BRACKET</h3>
<div class="bracket-wrapper" style="display: flex; flex-direction: row; gap: 20px; justify-content: center; background-color: #1a150e; padding: 15px; border-radius: 10px; border: 1px solid #333;">
<div class="bracket-column">
<div class="status-badge">Ronda 1</div>
<div class="match-box">{get_name('M6','p1')}<br><hr>{get_name('M6','p2')}</div>
</div>
<div class="bracket-column">
<div class="status-badge">Ronda 2</div>
<div class="match-box">{get_name('M7','p1')}<br><hr>{get_name('M7','p2')}</div>
</div>
<div class="bracket-column">
<div class="status-badge">Semis L</div>
<div class="match-box">{get_name('M8','p1')}<br><hr>{get_name('M8','p2')}</div>
</div>
<div class="bracket-column">
<div class="status-badge">Final L</div>
<div class="match-box">{get_name('M9','p1')}<br><hr>{get_name('M9','p2')}</div>
</div>
</div>
<br>
<div style="text-align: center; border: 2px solid #28a745; padding: 15px; border-radius: 15px; background: #0e1a0e; max-width: 400px; margin: 0 auto;">
<h3 style='margin: 0; color: #28a745;'>👑 GRAN FINAL</h3>
<div class="match-box" style="font-size: 1.1rem; border:none; background:transparent;">
{get_name('FINAL','p1')}<br><hr style="opacity: 0.3;">{get_name('FINAL','p2')}
</div>
</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)

# --- MAPA DE PARTIDOS ---
partidos = [
    {'id': 'M1', 'label': labels['M1'], 'p1': P[0], 'p2': P[1], 'turno': 1},
    {'id': 'M2', 'label': labels['M2'], 'p1': P[2], 'p2': P[3], 'turno': 1},
    {'id': 'M3', 'label': labels['M3'], 'p1': P[4], 'p2': P[5], 'turno': 2},
    {'id': 'M6', 'label': labels['M6'], 'p1': get_p('M1', P[0], P[1]), 'p1_src': f"Perdedor {labels['M1']}", 'p2': get_p('M2', P[2], P[3]), 'p2_src': f"Perdedor {labels['M2']}", 'turno': 2},
    {'id': 'M4', 'label': labels['M4'], 'p1': get_g('M1'), 'p1_src': f"Ganador {labels['M1']}", 'p2': get_g('M2'), 'p2_src': f"Ganador {labels['M2']}", 'turno': 3},
    {'id': 'M7', 'label': labels['M7'], 'p1': get_g('M6'), 'p1_src': f"Ganador {labels['M6']}", 'p2': get_p('M3', P[4], P[5]), 'p2_src': f"Perdedor {labels['M3']}", 'turno': 3},
    {'id': 'M5', 'label': labels['M5'], 'p1': get_g('M3'), 'p1_src': f"Ganador {labels['M3']}", 'p2': get_g('M4'), 'p2_src': f"Ganador {labels['M4']}", 'turno': 4},
    {'id': 'M8', 'label': labels['M8'], 'p1': get_p('M4', get_g('M1'), get_g('M2')), 'p1_src': f"Perdedor {labels['M4']}", 'p2': get_g('M7'), 'p2_src': f"Ganador {labels['M7']}", 'turno': 4},
    {'id': 'M9', 'label': labels['M9'], 'p1': get_p('M5', get_g('M3'), get_g('M4')), 'p1_src': f"Perdedor {labels['M5']}", 'p2': get_g('M8'), 'p2_src': f"Ganador {labels['M8']}", 'turno': 5},
    {'id': 'M10', 'label': 'Partido 5º y 6º', 'p1': get_p('M6', get_p('M1', P[0], P[1]), get_p('M2', P[2], P[3])), 'p1_src': f"Perdedor {labels['M6']}", 'p2': get_p('M7', get_g('M6'), get_p('M3', P[4], P[5])), 'p2_src': f"Perdedor {labels['M7']}", 'turno': 5},
    {'id': 'FINAL', 'label': '🏆 GRAND FINAL', 'p1': get_g('M5'), 'p1_src': f"Ganador {labels['M5']}", 'p2': get_g('M9'), 'p2_src': f"Ganador {labels['M9']}", 'turno': 6},
]

# --- UI ---
with st.sidebar:
    st.title("🎾 GemDev Control")
    if st.button("🖼️ VER CUADRO", use_container_width=True): modal_bracket()
    with st.expander("👥 Editar Parejas"):
        for i in range(6):
            P[i] = st.text_input(f"Pareja {i+1}", P[i], key=f"e_{i}")
    if st.button("🔄 Reiniciar Torneo"):
        st.session_state.resultados = {}; guardar_datos(); st.rerun()

st.title("🏆 Torneito Padel 25/26")
turnos = {}
for m in partidos: turnos.setdefault(m['turno'], []).append(m)

for t_idx in sorted(turnos.keys()):
    with st.expander(f"⏳ TURNO {t_idx}", expanded=True):
        cols = st.columns(2)
        for i, m in enumerate(turnos[t_idx]):
            with cols[i]:
                st.markdown(f"<span class='status-badge'>{m['label']}</span>", unsafe_allow_html=True)
                gan_actual = R.get(m['id'])
                is_ready = m['p1'] and m['p2']
                c1, c2 = st.columns(2)
                for idx, p_key in enumerate(['p1', 'p2']):
                    with [c1, c2][idx]:
                        if m[p_key]:
                            if st.button(m[p_key], key=f"btn_{m['id']}_{idx}", disabled=not is_ready,
                                         type="primary" if gan_actual == m[p_key] else "secondary", use_container_width=True):
                                st.session_state.resultados[m['id']] = m[p_key]
                                guardar_datos() # GUARDADO AUTOMÁTICO
                                if m['id'] == 'FINAL': 
                                    st.balloons()
                                    st.toast(f"¡Tenemos campeones: {m[p_key]}!", icon="🏆")
                                    time.sleep(2)
                                st.rerun()
                        else:
                            st.markdown(f'<div class="match-pending-label">{m.get(p_key+"_src", "Pendiente")}</div>', unsafe_allow_html=True)
