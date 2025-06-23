import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
from utils.styles import load_css
from utils.database import save_vote, get_today_votes, save_comment, get_recent_comments
import random
from datetime import datetime
import json

# --- FUNCIONES DE AFIRMACIONES (PILA) ---
AFFIRMATIONS_PATH = os.path.join("data", "affirmations.json")
AFIRMACIONES_MOSTRADAS_PATH = os.path.join("data", "afirmaciones_mostradas.json")

@st.cache_data
def load_affirmations():
    with open(AFFIRMATIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_afirmaciones_mostradas():
    if not os.path.exists(AFIRMACIONES_MOSTRADAS_PATH):
        return []
    with open(AFIRMACIONES_MOSTRADAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_afirmacion_mostrada(fecha, afirmacion):
    historial = load_afirmaciones_mostradas()
    historial.append({"fecha": fecha, "afirmacion": afirmacion})
    with open(AFIRMACIONES_MOSTRADAS_PATH, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)

def get_daily_affirmation():
    affirmations_dict = load_affirmations()
    affirmations = affirmations_dict["affirmations"]
    today = datetime.now().strftime("%Y-%m-%d")
    historial = load_afirmaciones_mostradas()
    # Si ya hay afirmación para hoy, usarla
    for entry in historial[::-1]:
        if entry["fecha"] == today:
            return entry["afirmacion"]
    # Obtener las últimas 4 afirmaciones mostradas
    ultimas = [entry["afirmacion"] for entry in historial[-4:]]
    # Buscar la siguiente afirmación secuencial que no esté en las últimas 4
    for afirmacion in affirmations:
        if afirmacion not in ultimas:
            save_afirmacion_mostrada(today, afirmacion)
            return afirmacion
    # Si todas han sido usadas recientemente, usar la primera
    afirmacion = affirmations[0]
    save_afirmacion_mostrada(today, afirmacion)
    return afirmacion

# Configuración de la página (debe ser la primera llamada a Streamlit)
st.set_page_config(
    page_title="Afirmaciones Positivas",
    page_icon="✨",
    layout="wide"
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
if 'message_sent' not in st.session_state:
    st.session_state.message_sent = False
if 'show_release_page' not in st.session_state:
    st.session_state.show_release_page = False
if 'comment_sent' not in st.session_state:
    st.session_state.comment_sent = False

# Estilos CSS
st.markdown("""
    <style>
        /* Estilos generales */
        .main {
            background-color: #f5f5f5;
        }
        
        /* Estilos para secciones */
        .section {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .section h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        /* Estilos para tarjetas de comentarios */
        .comment-card {
            background-color: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4CAF50;
        }
        
        .comment-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
            color: #666;
            font-size: 0.9em;
        }
        
        .comment-user {
            font-weight: bold;
            color: #2c3e50;
        }
        
        .comment-time {
            color: #666;
        }
        
        .comment-content {
            color: #333;
            line-height: 1.5;
            font-size: 1.1em;
        }
        
        /* Estilos para el formulario */
        .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
        }
        
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 20px;
            padding: 0.5rem 2rem;
            border: none;
            font-weight: bold;
        }
        
        .stButton button:hover {
            background-color: #45a049;
        }
        
        /* Estilos para mensajes de estado */
        .stSuccess {
            background-color: #dff0d8;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .stInfo {
            background-color: #d9edf7;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Si no hay nombre de usuario, mostrar la pantalla de bienvenida
if not st.session_state.user_name:
    st.markdown("""
        <div class="welcome-container">
            <h1 style="color: #2c3e50; margin-bottom: 1rem;">✨ Bienvenido a Afirmaciones Diarias ✨</h1>
            <p style="color: #34495e; font-size: 1.2rem; margin-bottom: 2rem;">
                Por favor, ingresa tu nombre para comenzar este viaje de positividad
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("welcome_form"):
        user_name = st.text_input("Tu nombre")
        submitted = st.form_submit_button("Comenzar")
        if submitted and user_name:
            st.session_state.user_name = user_name
            st.experimental_rerun()
    st.stop()

# Menú lateral
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem;">✨</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### 👋 ¡Hola, {st.session_state.user_name}!")
    if st.button("Cambiar nombre"):
        st.session_state.user_name = None
        st.experimental_rerun()
    
    selected = option_menu(
        menu_title="Menú",
        options=["Inicio", "Mis Afirmaciones", "Crear Afirmación", "Mensaje Privado"],
        icons=["house", "book", "plus-circle", "envelope"],
        menu_icon="list",
        default_index=0,
    )

# Contenido principal
if selected == "Inicio":
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>✨ Afirmación del Día ✨</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Obtener la afirmación del día
    affirmation = get_daily_affirmation()
    
    # Mostrar la afirmación con animación
    if not st.session_state.affirmation_shown:
        st.markdown(f"""
            <div class="affirmation-card">
                <div class="typewriter">
                    <h2 style="color: #2c3e50; text-align: center;">{affirmation}</h2>
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
                save_vote(st.session_state.user_name, "positive")
                st.session_state.voted = True
                st.success("¡Gracias por tu feedback!")
        with col2:
            if st.button("😐 Neutral"):
                save_vote(st.session_state.user_name, "neutral")
                st.session_state.voted = True
                st.success("¡Gracias por tu feedback!")
        with col3:
            if st.button("👎 No me resuena"):
                save_vote(st.session_state.user_name, "negative")
                st.session_state.voted = True
                st.success("¡Gracias por tu feedback!")
    
    # Mostrar estadísticas si ya votó
    if st.session_state.voted:
        st.markdown("""
            <div style="text-align: center; margin: 2rem 0;">
                <h3>Estadísticas del día</h3>
            </div>
        """, unsafe_allow_html=True)
        
        votes = get_today_votes()
        if votes:
            positive = sum(1 for v in votes if v['voto'] == 'positive')
            neutral = sum(1 for v in votes if v['voto'] == 'neutral')
            negative = sum(1 for v in votes if v['voto'] == 'negative')
            
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

elif selected == "Mensaje Privado":
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>✨ Mensaje Privado ✨</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.message_sent:
        st.markdown("""
            <div class="private-message">
                <p>¿Te gustaría compartir algo sobre cómo te resuena esta afirmación? Tu mensaje será privado y solo visible para el administrador.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("private_message_form"):
            message = st.text_area("Tu mensaje", height=150)
            submitted = st.form_submit_button("Enviar Mensaje")
            
            if submitted and message:
                # Obtener la afirmación actual
                current_affirmation = get_daily_affirmation()
                
                # Guardar el mensaje en la base de datos
                save_private_message(
                    usuario_nombre=st.session_state.user_name,
                    afirmacion=current_affirmation,
                    mensaje=message,
                    ip_address=st.experimental_get_query_params().get("ip", [None])[0],
                    user_agent=st.experimental_get_query_params().get("user_agent", [None])[0]
                )
                
                st.session_state.message_sent = True
                st.success("¡Gracias por compartir tu mensaje! Será revisado por el administrador.")
                
                # Mostrar el botón de "largue todo"
                if st.button("✨ Largue Todo ✨"):
                    st.session_state.show_release_page = True
                    st.experimental_rerun()
    else:
        st.info("Ya has enviado un mensaje hoy. ¡Gracias por compartir!")
        # Mostrar el botón de "largue todo" incluso si ya envió el mensaje
        if st.button("✨ Largue Todo ✨"):
            st.session_state.show_release_page = True
            st.experimental_rerun()

# Sección de comentarios públicos
st.markdown("""
    <div class="section">
        <h2>✨ Comparte tu Positividad</h2>
        <p>Deja un mensaje positivo para inspirar a otros. ¡Tu energía puede hacer la diferencia!</p>
    </div>
""", unsafe_allow_html=True)

# Formulario para comentarios
with st.form("comentario_form"):
    comentario = st.text_area("Tu mensaje positivo", height=100)
    submit_button = st.form_submit_button("Compartir Mensaje")
    
    if submit_button and comentario:
        save_comment(st.session_state.user_name, comentario)
        st.session_state.comment_sent = True
        st.success("¡Gracias por compartir tu positividad! 🌟")
        st.experimental_rerun()

# Mostrar comentarios recientes
st.markdown("""
    <div class="section">
        <h3>Mensajes del Día</h3>
    </div>
""", unsafe_allow_html=True)

comments = get_recent_comments()
if not comments:
    st.info("""
        <div style='text-align: center; padding: 20px;'>
            <p>¡Sé el primero en compartir un mensaje positivo hoy! 🌟</p>
            <p>Tu mensaje puede inspirar a otros a tener un mejor día.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for comment in comments:
        fecha = datetime.strptime(comment['fecha_creacion'], '%Y-%m-%d %H:%M:%S.%f')
        hora = fecha.strftime('%H:%M')
        
        st.markdown(f"""
            <div class="comment-card">
                <div class="comment-header">
                    <span class="comment-user">👤 {comment['usuario_nombre']}</span>
                    <span class="comment-time">🕒 {hora}</span>
                </div>
                <div class="comment-content">
                    {comment['comentario']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Sección de administración (solo visible para el administrador)
admin_username = os.getenv('ADMIN_USERNAME')
if admin_username and st.session_state.user_name == admin_username:
    # Verificación adicional de seguridad
    if st.session_state.get('is_admin', False) or st.text_input("🔐 Contraseña de administrador", type="password") == os.getenv('ADMIN_PASSWORD'):
        st.session_state.is_admin = True
        st.markdown("---")
        st.markdown("### 🔐 Panel de Administración")
        
        # Mostrar mensajes privados
        messages = get_private_messages()
        if messages:
            for msg in messages:
                with st.expander(f"Mensaje de {msg['usuario_nombre']} - {msg['fecha_creacion']}"):
                    st.markdown(f"**Afirmación:** {msg['afirmacion']}")
                    st.markdown(f"**Mensaje:** {msg['mensaje']}")
                    if not msg['leido']:
                        if st.button(f"Marcar como leído", key=f"read_{msg['id']}"):
                            mark_message_as_read(msg['id'])
                            st.experimental_rerun()
    else:
        st.error("Acceso denegado")
        st.session_state.is_admin = False 