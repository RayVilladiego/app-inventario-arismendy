import streamlit as st
from db import obtener_datos

def dashboard_screen():
    st.title("📊 Dashboard de Inventario")

    df = obtener_datos()

    if df.empty:
        st.warning("No hay datos disponibles en la tabla 'inventario'.")
        return

    st.subheader("📦 Tabla de inventario actual")
    st.dataframe(df, use_container_width=True)

    # Indicador de criticidad
    df["estado"] = df.apply(lambda row: calcular_estado(row["cantidad"], row["min_stock"]), axis=1)
    colores = {"OK": "🟢", "Alerta": "🟠", "Bajo": "🔴"}
    df["estado"] = df["estado"].map(colores)

    st.subheader("🚦 Estado crítico de inventario")
    st.dataframe(df[["nombre", "cantidad", "min_stock", "max_stock", "estado"]], use_container_width=True)
