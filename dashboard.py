import streamlit as st
import pandas as pd
from db import obtener_datos

def dashboard():
    st.title("📊 Dashboard General de Inventario")

    df = obtener_datos()

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    # KPI principales
    total_productos = df['producto'].nunique()
    total_unidades = df['Total'].sum()
    productos_bajo = df[df['Estado'] == 'Bajo'].shape[0]
    productos_alerta = df[df['Estado'] == 'Alerta'].shape[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🧾 Productos únicos", total_productos)
    col2.metric("📦 Total unidades", int(total_unidades))
    col3.metric("🔴 En estado BAJO", productos_bajo)
    col4.metric("🟠 En ALERTA", productos_alerta)

    st.markdown("---")
    st.subheader("🔍 Estado del inventario")

    st.dataframe(df.sort_values("Estado", ascending=True), use_container_width=True)
