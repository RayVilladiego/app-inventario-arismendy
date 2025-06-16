import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Alcance para Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Autenticación con las credenciales almacenadas en secrets
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["google_credentials"], scope
)
cliente = gspread.authorize(credenciales)

# ID único de tu hoja de cálculo (copiado del enlace)
SHEET_ID = "1IIxcoPm9CKesyj86SP1u2wVTzRKrwj3SSha7vYEYRXE"

# Conectarse a la hoja
hoja = cliente.open_by_key(SHEET_ID).sheet1

# Obtener datos actuales
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

# Título de la app
st.title("📦 Inventario Arismendy")
st.markdown("Consulta y gestión de recursos críticos en tiempo real.")

# Mostrar tabla de datos
st.subheader("📋 Inventario actual")
st.dataframe(df)

# Formulario para agregar nuevos registros
st.subheader("➕ Agregar nuevo recurso")
with st.form("formulario"):
    nombre = st.text_input("Nombre del recurso")
    cantidad = st.number_input("Cantidad", min_value=0)
    categoria = st.text_input("Categoría")
    enviar = st.form_submit_button("Agregar")

    if enviar and nombre and categoria:
        hoja.append_row([nombre, int(cantidad), categoria])
        st.success("✅ Recurso agregado correctamente. Recarga la app para ver los cambios.")
