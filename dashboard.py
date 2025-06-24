import streamlit as st
from db import obtener_datos
from utils import calcular_estado, color_estado

def dashboard_screen():
    st.title("📊 Dashboard de Inventario")

    df = obtener_datos()
    if df.empty:
        st.warning("⚠️ No hay datos en el inventario.")
        return

    df["Estado"] = df.apply(lambda row: calcular_estado(row["cantidad"], row["min_stock"], row["max_stock"]), axis=1)
    df["Color"] = df["Estado"].map(color_estado)

    def color_fila(row):
        return [f"background-color: {row['Color']}" for _ in row]

    st.dataframe(df.style.apply(color_fila, axis=1).hide(axis="columns", subset=["Color"]))
