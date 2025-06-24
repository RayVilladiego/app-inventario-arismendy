import streamlit as st
import pandas as pd
from db import obtener_datos, actualizar_stock_fisico
from utils import recalcular_estado_global

def auditor():
    st.title("🧮 Módulo de Auditoría de Inventario")

    df = obtener_datos()

    if df.empty:
        st.warning("No hay datos para auditar.")
        return

    st.subheader("📝 Ingreso de conteo físico")
    producto = st.selectbox("Selecciona un producto", df['producto'].unique())
    conteo_fisico = st.number_input("Cantidad física encontrada", min_value=0, step=1)

    if st.button("Registrar conteo físico"):
        actualizar_stock_fisico(producto, conteo_fisico)
        nuevo_estado = recalcular_estado_global(producto)
        st.success(f"✅ Conteo físico actualizado. Nuevo estado: {nuevo_estado}")

    st.markdown("---")
    st.subheader("📋 Comparación de Inventario Digital vs Físico")
    st.dataframe(df[['producto', 'Total', 'Fisico', 'Estado']], use_container_width=True)
