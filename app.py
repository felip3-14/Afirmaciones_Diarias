import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
from utils.affirmations_api import affirmations_api
from utils.styles import load_css, get_aurora_colors
from utils.daily_affirmation import daily_affirmation
import random

# Configuración de la página (debe ser la primera llamada a Streamlit)
st.set_page_config(
    page_title="Afirmaciones Diarias",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar variables de entorno
load_dotenv()

# Cargar estilos CSS y JavaScript
load_css()
st.markdown("""
    <script src="static/js/animations.js"></script>
""", unsafe_allow_html=True)

# Inicializar variables de sesión
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'affirmation_shown' not in st.session_state:
    st.session_state.affirmation_shown = False
if 'voted' not in st.session_state:
    st.session_state.voted = False

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .affirmation-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Formulario de nombre si no está registrado
if not st.session_state.user_name:
    st.markdown("""
        <div class="name-form">
            <h2 style="text-align: center; color: #2c3e50;">✨ Bienvenido a Afirmaciones Diarias ✨</h2>
            <p style="text-align: center; color: #34495e;">Por favor, ingresa tu nombre para comenzar</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("name_form"):
        name = st.text_input("Tu nombre")
        submitted = st.form_submit_button("Comenzar")
        if submitted and name:
            st.session_state.user_name = name
            st.rerun()

# Si el usuario está registrado, mostrar la aplicación principal
if st.session_state.user_name:
    # Menú lateral
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: white;">✨ Hola, {st.session_state.user_name}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title="Menú Principal",
            options=["Inicio", "Mis Afirmaciones", "Crear Afirmación", "Compartir"],
            icons=["house", "book", "plus-circle", "share"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.1)"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "white",
                    "--hover-color": "#3498db",
                },
                "nav-link-selected": {"background-color": "#3498db"},
            }
        )

    # Contenido principal
    if selected == "Inicio":
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>✨ Afirmación del Día ✨</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Obtener la afirmación del día
        affirmation = daily_affirmation.get_daily_affirmation()
        
        # Mostrar la afirmación con animación
        if not st.session_state.affirmation_shown:
            st.markdown(f"""
                <div class="affirmation-card">
                    <div class="typewriter">
                        <h2 style="color: #2c3e50; text-align: center;">{affirmation['affirmation']}</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.affirmation_shown = True
        
        # Sección de votación
        if not st.session_state.voted:
            st.markdown("""
                <div style="text-align: center; margin: 2rem 0;">
                    <h3>¿Te resuena esta afirmación?</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Sí, me resuena"):
                    daily_affirmation.save_vote(st.session_state.user_name, "positive")
                    st.session_state.voted = True
                    st.success("¡Gracias por tu feedback!")
            with col2:
                if st.button("😐 Neutral"):
                    daily_affirmation.save_vote(st.session_state.user_name, "neutral")
                    st.session_state.voted = True
                    st.success("¡Gracias por tu feedback!")
            with col3:
                if st.button("👎 No me resuena"):
                    daily_affirmation.save_vote(st.session_state.user_name, "negative")
                    st.session_state.voted = True
                    st.success("¡Gracias por tu feedback!")
        
        # Mostrar estadísticas si ya votó
        if st.session_state.voted:
            st.markdown("""
                <div style="text-align: center; margin: 2rem 0;">
                    <h3>Estadísticas del día</h3>
                </div>
            """, unsafe_allow_html=True)
            
            votes = daily_affirmation.get_today_votes()
            if votes:
                positive = sum(1 for v in votes if v['vote'] == 'positive')
                neutral = sum(1 for v in votes if v['vote'] == 'neutral')
                negative = sum(1 for v in votes if v['vote'] == 'negative')
                
                st.markdown(f"""
                    <div class="stats-container">
                        <div style="text-align: center;">
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">👍 {positive} personas resonaron con esta afirmación</p>
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">😐 {neutral} personas se mantuvieron neutrales</p>
                            <p style="font-size: 1.2rem; margin: 0.5rem 0;">👎 {negative} personas no resonaron con esta afirmación</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    elif selected == "Mis Afirmaciones":
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>✨ Mis Afirmaciones Guardadas ✨</h1>
            </div>
        """, unsafe_allow_html=True)
        # Aquí irá la lógica para mostrar las afirmaciones guardadas

    elif selected == "Crear Afirmación":
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>✨ Crear Nueva Afirmación ✨</h1>
            </div>
        """, unsafe_allow_html=True)
        # Aquí irá el formulario para crear nuevas afirmaciones

    elif selected == "Compartir":
        st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1>✨ Compartir Afirmaciones ✨</h1>
            </div>
        """, unsafe_allow_html=True)
        # Aquí irá la funcionalidad para compartir afirmaciones 