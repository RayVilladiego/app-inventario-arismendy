# dashboard.py

import streamlit as st
from db import fetch_query

def run():
    st.title("📈 Dashboard General")

    df = fetch_query("SELECT * FROM inventario ORDER BY nombre ASC")

    st.markdown("### 🧮 Estado General del Inventario")
    st.dataframe(df)

    bajo = df[df["estado"] == "Bajo"]
    alerta = df[df["estado"] == "Alerta"]
    ok = df[df["estado"] == "OK"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Productos OK", len(ok))
    col2.metric("En Alerta", len(alerta), delta=len(alerta))
    col3.metric("Stock Bajo", len(bajo), delta=len(bajo))
