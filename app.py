import streamlit as st
from datetime import datetime
import json
import os

# Ruta al archivo de afirmaciones
AFFIRMATIONS_PATH = os.path.join("data", "affirmations.json")
COMMENTS_PATH = os.path.join("data", "comments.json")
VOTES_PATH = os.path.join("data", "votes.json")

# Cargar afirmaciones
@st.cache_data
def load_affirmations():
    with open(AFFIRMATIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_daily_affirmation():
    affirmations = load_affirmations()
    today = datetime.now().date()
    idx = today.toordinal() % len(affirmations)
    return affirmations[idx]

# Guardar voto
def save_vote(user, vote):
    votes = []
    if os.path.exists(VOTES_PATH):
        with open(VOTES_PATH, "r", encoding="utf-8") as f:
            votes = json.load(f)
    today = datetime.now().strftime("%Y-%m-%d")
    votes.append({"user": user, "vote": vote, "date": today})
    with open(VOTES_PATH, "w", encoding="utf-8") as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)

def get_today_votes():
    if not os.path.exists(VOTES_PATH):
        return []
    today = datetime.now().strftime("%Y-%m-%d")
    with open(VOTES_PATH, "r", encoding="utf-8") as f:
        votes = json.load(f)
    return [v for v in votes if v["date"] == today]

# Guardar comentario
def save_comment(user, comment):
    comments = []
    if os.path.exists(COMMENTS_PATH):
        with open(COMMENTS_PATH, "r", encoding="utf-8") as f:
            comments = json.load(f)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comments.append({"user": user, "comment": comment, "datetime": now})
    with open(COMMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

def get_recent_comments():
    if not os.path.exists(COMMENTS_PATH):
        return []
    with open(COMMENTS_PATH, "r", encoding="utf-8") as f:
        comments = json.load(f)
    return comments[-10:][::-1]  # últimos 10, más reciente primero

# --- Interfaz Streamlit ---
st.set_page_config(page_title="Afirmaciones Positivas", page_icon="✨", layout="centered")

if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "voted" not in st.session_state:
    st.session_state.voted = False
if "comment_sent" not in st.session_state:
    st.session_state.comment_sent = False

# Pantalla de bienvenida
if not st.session_state.user_name:
    st.title("✨ Bienvenido a Afirmaciones Diarias ✨")
    user_name = st.text_input("Por favor, ingresa tu nombre para comenzar:")
    if st.button("Comenzar") and user_name:
        st.session_state.user_name = user_name
        st.experimental_rerun()
    st.stop()

st.sidebar.title(f"👋 ¡Hola, {st.session_state.user_name}!")
if st.sidebar.button("Cambiar nombre"):
    st.session_state.user_name = None
    st.experimental_rerun()

st.title("✨ Afirmación del Día ✨")
affirmation = get_daily_affirmation()
st.header(affirmation)

# Votación
if not st.session_state.voted:
    st.subheader("¿Te resuena esta afirmación?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Sí"):
            save_vote(st.session_state.user_name, "positive")
            st.session_state.voted = True
            st.success("¡Gracias por tu feedback!")
    with col2:
        if st.button("😐 Neutral"):
            save_vote(st.session_state.user_name, "neutral")
            st.session_state.voted = True
            st.success("¡Gracias por tu feedback!")
    with col3:
        if st.button("👎 No"):
            save_vote(st.session_state.user_name, "negative")
            st.session_state.voted = True
            st.success("¡Gracias por tu feedback!")
else:
    st.info("Ya votaste hoy. ¡Gracias!")
    votes = get_today_votes()
    if votes:
        positive = sum(1 for v in votes if v["vote"] == "positive")
        neutral = sum(1 for v in votes if v["vote"] == "neutral")
        negative = sum(1 for v in votes if v["vote"] == "negative")
        st.write(f"👍 {positive} | 😐 {neutral} | 👎 {negative}")

# Comentarios públicos
st.markdown("---")
st.subheader("✨ Comparte tu positividad")
with st.form("comentario_form"):
    comentario = st.text_area("Deja un mensaje positivo para inspirar a otros:", height=100)
    submit_button = st.form_submit_button("Compartir Mensaje")
    if submit_button and comentario:
        save_comment(st.session_state.user_name, comentario)
        st.session_state.comment_sent = True
        st.success("¡Gracias por compartir tu positividad! 🌟")
        st.experimental_rerun()

st.subheader("Mensajes del Día")
comments = get_recent_comments()
if not comments:
    st.info("Sé el primero en compartir un mensaje positivo hoy! 🌟")
else:
    for comment in comments:
        fecha = comment["datetime"]
        st.markdown(f"**{comment['user']}** ({fecha}): {comment['comment']}") 