from openai import OpenAI
import json
import os
import streamlit as st
from datetime import datetime

# Crear acceso a API, El import esta en secrets.toml
# Sino no se sube a Github
client = OpenAI(api_key=st.secrets["openai"]["api_key"])
# Acceso a css
def cargar_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

cargar_css()


# Pedirle a gpt que nos de la idea de cancion
st.title("Chau bloqueo")
st.markdown("""
En un mundo en donde todo va a la velocidad de la luz y surgen estos bloqueos artísticos, se propone **Chau Bloque** con la intención de ayudar al artista a salir de su bloqueo y, con un título y algunos versos, inspirarse para seguir con su creatividad.
""")

# Selección de emoción
st.subheader("Elegí una emoción para inspirarte")
opcion_emocion = st.selectbox("Emoción base de la canción:", [
    "Alegría",
    "Tristeza",
    "Enojo",
    "Nostalgia"
])

# Botón para generar
if st.button("Generar idea"):
    prompt = f"Generá un título de canción y cuatro versos inspirados en la emoción: {opcion_emocion}."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    texto_generado = response.choices[0].message.content.strip()
    lineas = [linea for linea in texto_generado.split("\n") if linea.strip()]
    titulo = lineas[0] if lineas else "(Sin título)"
    versos = lineas[1:5] if len(lineas) >= 5 else lineas[1:]

    # Mostrar resultados
    st.subheader("Título")
    st.markdown(f"**{titulo}**")

    st.subheader("Versos")
    for verso in versos:
        st.markdown(f"- {verso}")

    # Guardar en JSON
    datos = {"emocion": opcion_emocion, "titulo": titulo, "versos": versos}
    with open("canciones.json", "a", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False)
        f.write("\n")

# Sección de ayuda
st.markdown("---")
st.subheader("Cómo funciona")
st.markdown("""
1. Elegí una de las cuatro emociones disponibles.
2. Hacé clic en "Generar idea".
3. Vas a ver un título de canción y cuatro versos inspiradores.
""")
