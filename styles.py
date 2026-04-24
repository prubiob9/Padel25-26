import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        div.stButton > button[kind="primary"] { background-color: #28a745 !important; color: white !important; }
        
        .bracket-wrapper { 
            display: flex !important; 
            flex-direction: row !important; 
            flex-wrap: nowrap !important;
            gap: 40px; 
            padding: 30px; 
            overflow-x: auto; 
            background-color: #0e1117; 
            border-radius: 15px;
            width: 100%;
        }
        
        .bracket-column { 
            display: flex; 
            flex-direction: column; 
            justify-content: space-around; 
            min-width: 220px;
            flex-shrink: 0;
        }
        
        .match-box { 
            border: 1px solid #444; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px; 
            background: #1a1c23; 
            text-align: center; 
            color: #ddd;
        }
        
        .match-winner { border: 2px solid #28a745 !important; color: #28a745 !important; background: #121a12 !important; font-weight: bold; }
        .match-waiting { border: 1px dashed #555 !important; color: #777 !important; background: transparent !important; }
        
        .match-pending-label {
            background-color: #262730;
            color: #555;
            padding: 8px;
            border-radius: 5px;
            text-align: center;
            border: 1px solid #333;
            font-size: 0.85rem;
            height: 38.4px; 
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
        }

        /* FIX: Alineación de Clasificación PJ-PG-PP */
        th, td { text-align: right !important; }
        th:first-child, td:first-child { text-align: left !important; }

        .status-badge { padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; background: #333; color: #fff; margin-bottom: 10px; display: inline-block; }
        hr { opacity: 0.1; margin: 8px 0; }
        </style>
        """, unsafe_allow_html=True)