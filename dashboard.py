import streamlit as st
import pandas as pd
from db import get_all_inventory

def mostrar_dashboard():
    st.title("📊 Dashboard de Inventario")

    data = get_all_inventory()

    if data.empty:
        st.warning("No hay datos en el inventario aún.")
        return

    st.subheader("Resumen general")

    total_productos = len(data)
    productos_bajo_stock = len(data[data["estado"] == "Bajo"])
    productos_alerta = len(data[data["estado"] == "Alerta"])
    productos_ok = len(data[data["estado"] == "OK"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Productos Totales", total_productos)
    col2.metric("🟥 Bajo", productos_bajo_stock)
    col3.metric("🟧 Alerta", productos_alerta)
    col4.metric("🟩 OK", productos_ok)

    st.divider()
    st.subheader("📦 Detalles del Inventario")
    st.dataframe(data, use_container_width=True)
