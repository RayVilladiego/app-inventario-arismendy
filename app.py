import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Alcance para la API de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Cargar las credenciales directamente desde secrets
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["google_credentials"], scope
)
cliente = gspread.authorize(credenciales)

# Abrir la hoja de cálculo (ajusta el nombre si es diferente)
hoja = cliente.open("Inventario AYA").sheet1

# Obtener los registros actuales
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

# Interfaz de la aplicación
st.title("📦 Inventario Arismendy")
st.markdown("Consulta y registro de recursos críticos en tiempo real.")

# Mostrar la tabla actual
st.subheader("📋 Inventario actual")
st.dataframe(df)

# Formulario para agregar registros
st.subheader("➕ Agregar nuevo recurso")
with st.form("formulario"):
    nombre = st.text_input("Nombre del recurso")
    cantidad = st.number_input("Cantidad", min_value=0)
    categoria = st.text_input("Categoría")
    enviar = st.form_submit_button("Agregar")

    if enviar and nombre and categoria:
        hoja.append_row([nombre, int(cantidad), categoria])
        st.success("✅ Recurso agregado correctamente. Recarga la app para ver los cambios.")
