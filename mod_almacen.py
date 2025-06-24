import streamlit as st
from db import actualizar_stock
import pandas as pd

def modulo_almacen():
    st.title("📦 Módulo de Almacén - Registro de Entradas/Salidas")

    with st.form("form_almacen"):
        codigo = st.text_input("Código del producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        movimiento = st.radio("Tipo de movimiento", ["entrada", "salida"])
        submit = st.form_submit_button("Registrar movimiento")

    if submit:
        if not codigo:
            st.warning("⚠️ Debes ingresar el código del producto.")
        else:
            exito = actualizar_stock(codigo, cantidad, movimiento=movimiento)
            if exito:
                st.success(f"✔ Movimiento de {movimiento} registrado correctamente.")
            else:
                st.error("❌ Error al registrar el movimiento. Revisa si el producto existe o si hay suficiente stock.")
