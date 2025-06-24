import streamlit as st
from db import insertar_material
from utils import calcular_estado

def compras_screen():
    st.title("🛒 Módulo de Compras - Registro de materiales")

    producto = st.text_input("Nombre del producto")
    cantidad = st.number_input("Cantidad a ingresar", min_value=1, step=1)
    minimo = st.number_input("Stock mínimo permitido", min_value=0, step=1)
    maximo = st.number_input("Stock máximo recomendado", min_value=1, step=1)

    if st.button("Registrar entrada"):
        estado = calcular_estado(cantidad, minimo, maximo)
        insertar_material(producto, cantidad, minimo, maximo, estado)
        st.success(f"{producto} registrado exitosamente con estado: {estado}")
