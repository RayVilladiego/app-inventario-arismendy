import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Configurar alcance (scope) de la API de Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciales = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
cliente = gspread.authorize(credenciales)

# Abrir la hoja de cálculo de Google Sheets (ajusta el nombre si es diferente)
hoja = cliente.open("Inventario AYA").sheet1

# Obtener todos los registros como diccionarios
datos = hoja.get_all_records()
df = pd.DataFrame(datos)

# Título principal
st.title("📦 Inventario Arismendy (Conectado a Google Sheets)")
st.write("Consulta y actualización en tiempo real del inventario crítico de recursos.")

# Mostrar tabla del inventario
st.subheader("📋 Inventario actual")
st.dataframe(df)

# Formulario para agregar nuevo recurso
st.subheader("➕ Agregar nuevo recurso")
with st.form("formulario"):
    nombre = st.text_input("Nombre del recurso")
    cantidad = st.number_input("Cantidad", min_value=0)
    categoria = st.text_input("Categoría")
    enviar = st.form_submit_button("Agregar")

    if enviar and nombre and categoria:
        hoja.append_row([nombre, int(cantidad), categoria])
        st.success("✅ Recurso agregado correctamente. Refresca la app para ver los cambios.")
