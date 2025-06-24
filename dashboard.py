import streamlit as st
import pandas as pd
from db import obtener_datos
from utils import calcular_estado

def dashboard_screen():
    st.title("📊 Dashboard de Inventario")

    df = obtener_datos()
    st.dataframe(df)

    # Mostrar conteo por estado
    estados = df['producto'].apply(calcular_estado)
    conteo = estados.value_counts().reset_index()
    conteo.columns = ['Estado', 'Cantidad']

    st.subheader("Resumen de estado de inventario")
    st.bar_chart(conteo.set_index('Estado'))

    st.subheader("Top 5 productos con menor stock")
    top_bajos = df.sort_values('Total').head(5)
    st.table(top_bajos[['producto', 'Total']])
