
import streamlit as st
from db import execute_query
from utils import calcular_estado

def run():
    st.title("🛒 Módulo Compras - Registrar nuevo producto")

    with st.form("form_compras"):
        codigo = st.text_input("Código del producto")
        nombre = st.text_input("Nombre")
        total = st.number_input("Cantidad inicial", min_value=0, step=1)
        minimo = st.number_input("Stock mínimo", min_value=0, step=1)
        maximo = st.number_input("Stock máximo", min_value=1, step=1)
        submitted = st.form_submit_button("Registrar")

        if submitted:
            estado = calcular_estado(total, minimo, maximo)
            query = """
                INSERT INTO inventario (codigo, nombre, total, min, max, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (codigo) DO NOTHING;
            """
            execute_query(query, (codigo, nombre, total, minimo, maximo, estado))
            st.success("Producto registrado correctamente.")
