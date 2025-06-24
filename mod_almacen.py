# modules/mod_almacen.py

import streamlit as st
from db import fetch_query, execute_query
from datetime import datetime
from utils import calcular_estado

def run():
    st.title("🏷️ Módulo Almacén - Entrada / Salida")

    df = fetch_query("SELECT * FROM inventario ORDER BY nombre ASC")

    codigo = st.selectbox("Selecciona un producto", df["codigo"] + " - " + df["nombre"])
    movimiento = st.selectbox("Tipo de movimiento", ["Entrada", "Salida"])
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    operario = st.text_input("Operario responsable")

    if st.button("Registrar movimiento"):
        selected = df[df["codigo"] == codigo.split(" - ")[0]].iloc[0]
        nuevo_total = selected["total"] + cantidad if movimiento == "Entrada" else selected["total"] - cantidad

        if nuevo_total < 0:
            st.error("No hay suficiente inventario para la salida.")
            return

        estado = calcular_estado(nuevo_total, selected["min"], selected["max"])

        # Actualizar inventario
        execute_query("UPDATE inventario SET total = %s, estado = %s WHERE codigo = %s",
                      (nuevo_total, estado, selected["codigo"]))

        # Registrar movimiento
        execute_query("""
            INSERT INTO movimientos (fecha, codigo, movimiento, cantidad, operario, total_final)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (datetime.now(), selected["codigo"], movimiento, cantidad, operario, nuevo_total))

        st.success(f"Movimiento registrado. Nuevo total: {nuevo_total}")
