# modules/mod_auditor.py

import streamlit as st
from db import fetch_query, execute_query
from datetime import datetime

def run():
    st.title("🔍 Módulo Auditor - Conteo Físico y Comparación")

    df = fetch_query("SELECT * FROM inventario ORDER BY nombre ASC")

    codigo = st.selectbox("Selecciona un producto", df["codigo"] + " - " + df["nombre"])
    cantidad_fisica = st.number_input("Cantidad observada (física)", min_value=0, step=1)
    operario = st.text_input("Nombre del auditor")

    if st.button("Registrar conteo físico"):
        selected = df[df["codigo"] == codigo.split(" - ")[0]].iloc[0]
        diferencia = cantidad_fisica - selected["total"]

        execute_query("""
            INSERT INTO conteo_fisico (fecha, codigo, cantidad_fisica, operario, diferencia)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now(), selected["codigo"], cantidad_fisica, operario, diferencia))

        if diferencia == 0:
            st.success("✔️ Conteo coincidente con el sistema.")
        elif diferencia > 0:
            st.warning(f"🟡 Sobrante detectado (+{diferencia})")
        else:
            st.error(f"🔴 Faltante detectado ({diferencia})")

    st.markdown("### 📊 Comparador físico vs sistema")
    df_conteos = fetch_query("SELECT * FROM conteo_fisico ORDER BY fecha DESC LIMIT 20")
    st.dataframe(df_conteos)
