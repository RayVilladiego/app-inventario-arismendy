import streamlit as st
from login import login
from mod_compras import interfaz_compras
from mod_almacen import interfaz_almacen
from mod_auditor import interfaz_auditor
from dashboard import mostrar_dashboard

# Simulación de login con perfiles
perfil = login()

st.sidebar.title("Navegación")

if perfil == "Compras":
    interfaz_compras()

elif perfil == "Almacén":
    interfaz_almacen()

elif perfil == "Auditor":
    interfaz_auditor()

if st.sidebar.button("Dashboard"):
    mostrar_dashboard()
