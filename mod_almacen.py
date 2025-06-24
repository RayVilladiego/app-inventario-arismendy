import streamlit as st
from db import insertar_movimiento, obtener_productos, actualizar_stock
from utils import calcular_estado

def almacen():
    st.title("🏗️ Módulo de Almacén")

    productos = obtener_productos()
    producto = st.selectbox("Selecciona un producto", productos)

    cantidad = st.number_input("Cantidad a retirar", min_value=1, step=1)

    if st.button("Registrar salida"):
        insertar_movimiento(producto, cantidad, "salida")
        actualizar_stock(producto, cantidad, tipo="salida")

        nuevo_estado = calcular_estado(producto)
        st.success(f"✅ Salida registrada. Nuevo estado del producto: {nuevo_estado}")
