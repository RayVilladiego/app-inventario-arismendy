import streamlit as st
from db import insertar_movimiento, obtener_productos, actualizar_stock
from utils import calcular_estado

def compras():
    st.title("🛒 Módulo de Compras")

    productos = obtener_productos()
    producto = st.selectbox("Selecciona un producto", productos)

    cantidad = st.number_input("Cantidad a ingresar", min_value=1, step=1)

    if st.button("Registrar entrada"):
        insertar_movimiento(producto, cantidad, "entrada")
        actualizar_stock(producto, cantidad, tipo="entrada")

        nuevo_estado = calcular_estado(producto)
        st.success(f"✅ Entrada registrada. Nuevo estado del producto: {nuevo_estado}")
