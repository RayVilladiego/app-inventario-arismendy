# app.py

import streamlit as st

st.set_page_config(page_title="Sistema WMS", layout="wide")

st.title("Sistema de Inventario - Arismendy")

st.info("Esta app fue desplegada correctamente. Pronto se redireccionará al módulo principal.")

# Opción para redireccionar
if st.button("Ir al módulo principal"):
    st.switch_page("main.py")
