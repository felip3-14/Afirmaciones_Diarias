import streamlit as st

def load_css():
    """Carga los estilos CSS personalizados"""
    st.markdown("""
        <style>
        /* Estilos generales */
        .main {
            background: linear-gradient(-45deg, #1a2a6c, #b21f1f, #fdbb2d, #4b6cb7);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            padding: 2rem;
            min-height: 100vh;
        }
        
        /* Animación del fondo tipo aurora boreal */
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* Estilos para el sidebar */
        .css-1d391kg {
            background: rgba(44, 62, 80, 0.9);
            backdrop-filter: blur(10px);
            padding: 2rem 1rem;
        }
        
        /* Estilos para las tarjetas de afirmaciones */
        .affirmation-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .affirmation-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
            z-index: 1;
            pointer-events: none;
        }
        
        .affirmation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }
        
        /* Estilos para los botones */
        .stButton > button {
            background: linear-gradient(45deg, #3498db, #2ecc71);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.8rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            background: linear-gradient(45deg, #2980b9, #27ae60);
        }
        
        /* Efecto de brillo para los botones */
        .stButton > button::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255,255,255,0.1),
                transparent
            );
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% {
                transform: translateX(-100%) rotate(45deg);
            }
            100% {
                transform: translateX(100%) rotate(45deg);
            }
        }
        
        /* Estilos para los títulos */
        h1, h2, h3 {
            color: white;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Animación de escritura para las afirmaciones */
        .typewriter {
            overflow: hidden;
            border-right: .15em solid #3498db;
            white-space: nowrap;
            margin: 0 auto;
            letter-spacing: .15em;
            animation: 
                typing 3.5s steps(40, end),
                blink-caret .75s step-end infinite;
        }
        
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #3498db }
        }
        
        /* Estilos para el formulario de nombre */
        .name-form {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        /* Estilos para las estadísticas */
        .stats-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            backdrop-filter: blur(10px);
        }
        
        /* Estilos para el menú de opciones */
        .option-menu {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Estilos para los inputs */
        .stTextInput > div > div > input {
            border-radius: 25px;
            padding: 0.8rem 1.5rem;
            border: 2px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.9);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
            background: rgba(255,255,255,1);
        }
        
        /* Estilos para los mensajes de éxito */
        .stSuccess {
            background: rgba(46, 204, 113, 0.1);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #2ecc71;
            backdrop-filter: blur(10px);
        }
        
        /* Efecto de partículas para el fondo */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }
        
        .particle {
            position: absolute;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            pointer-events: none;
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            0% {
                transform: translateY(0) translateX(0);
                opacity: 0;
            }
            50% {
                opacity: 0.5;
            }
            100% {
                transform: translateY(-100vh) translateX(100px);
                opacity: 0;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def get_aurora_colors():
    """Retorna una lista de colores para el fondo tipo aurora boreal"""
    return {
        'primary': '#3498db',
        'secondary': '#2ecc71',
        'accent': '#e74c3c',
        'background': '#f5f7fa',
        'text': '#2c3e50'
    } 