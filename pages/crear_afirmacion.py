import streamlit as st
from utils.database import agregar_afirmacion

st.title("Crear Nueva Afirmación")

# Formulario para crear afirmación
with st.form("crear_afirmacion_form"):
    texto = st.text_area(
        "Escribe tu afirmación",
        placeholder="Por ejemplo: 'Soy capaz de lograr todo lo que me propongo'",
        height=100
    )
    
    categoria = st.selectbox(
        "Categoría",
        ["Autoestima", "Éxito", "Bienestar", "Motivación", "Gratitud", "Otro"]
    )
    
    if categoria == "Otro":
        categoria = st.text_input("Especifica la categoría")
    
    submitted = st.form_submit_button("Crear Afirmación")
    
    if submitted:
        if texto:
            agregar_afirmacion(texto, categoria)
            st.success("¡Afirmación creada exitosamente! ✨")
        else:
            st.error("Por favor, escribe una afirmación antes de enviar.")

# Sección de ayuda
st.markdown("---")
st.subheader("Consejos para crear afirmaciones efectivas")
st.markdown("""
1. **Usa el tiempo presente**: "Soy" en lugar de "Seré"
2. **Sé positivo**: Enfócate en lo que quieres, no en lo que no quieres
3. **Sé específico**: Cuanto más específica sea tu afirmación, más poderosa será
4. **Sé realista**: Asegúrate de que tu afirmación sea creíble para ti
5. **Usa palabras poderosas**: Elige palabras que te inspiren y motiven
""") 