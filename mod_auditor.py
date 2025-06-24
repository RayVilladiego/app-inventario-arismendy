import streamlit as st
import pandas as pd
from db import obtener_datos_productos

def modulo_auditoria():
    st.title("🕵️ Módulo de Auditoría - Control y Verificación de Inventario")

    st.write("📋 Aquí puedes visualizar el estado actual del inventario y registrar los conteos físicos para comparar.")

    df = obtener_datos_productos()
    if df.empty:
        st.warning("No hay productos registrados.")
        return

    df['Conteo Físico'] = 0

    conteo = st.experimental_data_editor(df[['codigo', 'material', 'medida', 'total', 'Conteo Físico']], num_rows="dynamic", use_container_width=True)

    if st.button("📊 Comparar Inventario Físico vs. Sistema"):
        conteo['Diferencia'] = conteo['Conteo Físico'] - conteo['total']
        st.dataframe(conteo, use_container_width=True)
        st.success("✅ Comparación realizada. Revisa la columna 'Diferencia' para identificar inconsistencias.")
