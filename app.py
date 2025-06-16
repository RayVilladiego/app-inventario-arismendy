import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import base64

# Configurar el alcance para Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Leer las credenciales desde los secrets (codificadas en base64)
creds_base64 = st.secrets["GOOGLE_CREDENTIALS_BASE64"]
decoded = base64.b64decode(creds_base64).decode("utf-8")
creds_dict = json.loads(decoded)

# Autenticarse con Google
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
cliente = gspread.authorize(credenciales)

# Abrir la hoja de cálculo (asegúrate que el nombre sea correcto)
hoja = cliente.open("Inventario AYA").sheet1

# Obtener datos actuales
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

# Interfaz principal
st.title("📦 Inventario Arismendy")
st.markdown("Consulta y registra recursos críticos en tiempo real.")

# Mostrar tabla
st.subheader("📋 Inventario actual")
st.dataframe(df)

# Formulario para añadir
st.subheader("➕ Agregar nuevo recurso")
with st.form("formulario"):
    nombre = st.text_input("Nombre del recurso")
    cantidad = st.number_input("Cantidad", min_value=0)
    categoria = st.text_input("Categoría")
    enviar = st.form_submit_button("Agregar")

    if enviar and nombre and categoria:
        hoja.append_row([nombre, int(cantidad), categoria])
        st.success("✅ Recurso agregado correctamente. Recarga la app para ver los cambios.")
