import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Afirmaciones Diarias",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Menú lateral
with st.sidebar:
    st.title("✨ Afirmaciones Diarias")
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Inicio", "Mis Afirmaciones", "Crear Afirmación", "Compartir"],
        icons=["house", "book", "plus-circle", "share"],
        menu_icon="cast",
        default_index=0,
    )

# Contenido principal
if selected == "Inicio":
    st.title("Bienvenido a Afirmaciones Diarias")
    st.write("Tu espacio para inspirarte y motivarte cada día.")
    
    # Mostrar afirmación del día
    st.subheader("Afirmación del Día")
    st.markdown("""
        <div class="affirmation-card">
            <h3>✨ Hoy soy capaz de lograr todo lo que me proponga</h3>
            <p>Recuerda que cada día es una nueva oportunidad para brillar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sección de categorías
    st.subheader("Categorías Populares")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Autoestima")
    with col2:
        st.button("Éxito")
    with col3:
        st.button("Bienestar")

elif selected == "Mis Afirmaciones":
    st.title("Mis Afirmaciones Guardadas")
    # Aquí irá la lógica para mostrar las afirmaciones guardadas

elif selected == "Crear Afirmación":
    st.title("Crear Nueva Afirmación")
    # Aquí irá el formulario para crear nuevas afirmaciones

elif selected == "Compartir":
    st.title("Compartir Afirmaciones")
    # Aquí irá la funcionalidad para compartir afirmaciones 