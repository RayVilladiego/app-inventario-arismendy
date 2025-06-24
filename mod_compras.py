import streamlit as st
from db import insertar_producto, actualizar_stock
import pandas as pd

def modulo_compras():
    st.title("🛒 Módulo de Compras - Ingreso de Materiales")

    with st.form("form_compras"):
        codigo = st.text_input("Código del producto")
        material = st.text_input("Nombre del material")
        medida = st.text_input("Unidad de medida (ej: UND, KG, GAL)")
        cantidad = st.number_input("Cantidad a ingresar", min_value=1, step=1)
        minimo = st.number_input("Cantidad mínima recomendada", min_value=0, step=1)
        maximo = st.number_input("Cantidad máxima recomendada", min_value=0, step=1)
        submit = st.form_submit_button("Registrar")

    if submit:
        if not all([codigo, material, medida]):
            st.warning("Por favor completa todos los campos obligatorios.")
        else:
            # Intenta insertar primero. Si ya existe, actualiza.
            exito = insertar_producto(codigo, material, medida, cantidad, minimo, maximo)
            if exito:
                st.success("✔ Producto ingresado correctamente.")
            else:
                actualizado = actualizar_stock(codigo, cantidad, movimiento="entrada")
                if actualizado:
                    st.success("✔ Producto ya existía. Cantidad actualizada.")
                else:
