import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Configurar el acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_credentials"], scope)
cliente = gspread.authorize(credenciales)

# Abrir hoja por ID (copiada del enlace)
SHEET_ID = "1IIxcoPm9CKesyj86SP1u2wVTzRKrwj3SSha7vYEYRXE"
hoja = cliente.open_by_key(SHEET_ID).sheet1

# Cargar datos como DataFrame
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

st.title("📦 Inventario Arismendy")
st.markdown("Consulta y gestión de recursos críticos en tiempo real.")

st.subheader("📋 Inventario actual")
st.dataframe(df)

# 🔧 Función para actualizar producto en hoja
def actualizar_producto(nombre, cantidad, tipo):
    datos = hoja.get_all_records()
    for idx, fila in enumerate(datos):
        if fila["Material"].strip().lower() == nombre.strip().lower():
            fila_num = idx + 2  # 2 porque gspread es 1-indexado y fila 1 es encabezado

            entrada = int(fila["Entrada"])
            salida = int(fila["Salida"])
            minimo = int(fila["Min"])
            maximo = int(fila["Max"])

            # Actualizar entrada o salida
            if tipo == "entrada":
                entrada += cantidad
                hoja.update_cell(fila_num, 7, entrada)
            elif tipo == "salida":
                salida += cantidad
                hoja.update_cell(fila_num, 8, salida)

            # Recalcular total y estado
            total = entrada - salida
            hoja.update_cell(fila_num, 9, total)

            if total < minimo:
                estado = "Bajo"
            elif total < maximo:
                estado = "Alerta"
            else:
                estado = "OK"

            hoja.update_cell(fila_num, 10, estado)
            return True
    return False

# ➕ Formulario para registrar entradas
st.subheader("➕ Registrar entrada de producto")
with st.form("entrada_form"):
    nombre_entrada = st.text_input("Nombre del producto")
    cantidad_entrada = st.number_input("Cantidad a ingresar", min_value=1, step=1)
    enviar = st.form_submit_button("Registrar entrada")

    if enviar:
        ok = actualizar_producto(nombre_entrada, cantidad_entrada, tipo="entrada")
        if ok:
            st.success("✅ Entrada registrada correctamente.")
        else:
            st.error("❌ Producto no encontrado.")

# ➖ Formulario para registrar salidas
st.subheader("➖ Registrar salida de producto")
with st.form("salida_form"):
    nombre_salida = st.text_input("Nombre del producto", key="salida_nombre")
    cantidad_salida = st.number_input("Cantidad a retirar", min_value=1, step=1, key="salida_cantidad")
    retirar = st.form_submit_button("Registrar salida")

    if retirar:
        ok = actualizar_producto(nombre_salida, cantidad_salida, tipo="salida")
        if ok:
            st.success("✅ Salida registrada correctamente.")
        else:
            st.error("❌ Producto no encontrado.")

