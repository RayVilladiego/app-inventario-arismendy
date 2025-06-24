import streamlit as st
from db import actualizar_stock
from utils import calcular_estado

def almacen_screen():
    st.title("🏷️ Módulo de Almacén - Salida de materiales")

    producto = st.text_input("Nombre del producto a retirar")
    cantidad_salida = st.number_input("Cantidad a retirar", min_value=1, step=1)

    if st.button("Registrar salida"):
        resultado = actualizar_stock(producto, cantidad_salida)
        if resultado == "no_encontrado":
            st.warning(f"⚠️ El producto '{producto}' no está registrado.")
        elif resultado == "stock_insuficiente":
            st.warning("⚠️ No hay suficiente stock para realizar la salida.")
        elif resultado == "actualizado":
            st.success(f"✅ Stock de '{producto}' actualizado correctamente.")
        else:
            st.error("❌ Error inesperado al actualizar el stock.")
