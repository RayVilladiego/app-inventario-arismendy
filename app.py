import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# Configurar el alcance para Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Leer las credenciales desde los secrets de Streamlit
credenciales_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(credenciales_dict, scope)
cliente = gspread.authorize(credenciales)

# Abrir la hoja de cálculo (ajusta si el nombre cambia)
hoja = cliente.open("Inventario AYA").sheet1

# Obtener los datos actuales como DataFrame
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

# UI de la app
st.title("📦 Inventario Arismendy (Google Sheets)")
st.markdown("Consulta y registra recursos críticos en tiempo real.")

# Mostrar tabla de inventario
st.subheader("📋 Inventario actual")
st.dataframe(df)

# Formulario para agregar nuevos recursos
st.subheader("➕ Agregar nuevo recurso")
with st.form("formulario"):
    nombre = st.text_input("Nombre del recurso")
    cantidad = st.number_input("Cantidad", min_value=0)
    categoria = st.text_input("Categoría")
    enviar = st.form_submit_button("Agregar")

    if enviar and nombre and categoria:
        hoja.append_row([nombre, int(cantidad), categoria])
        st.success("✅ Recurso agregado correctamente. Refresca la app para ver los cambios.")
