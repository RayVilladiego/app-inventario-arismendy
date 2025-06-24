import streamlit as st
from login import login_screen
from mod_compras import compras_screen
from mod_almacen import almacen_screen
from mod_auditor import auditor_screen
from dashboard import dashboard_screen

# Configuración general de la app
st.set_page_config(page_title="Inventario Arismendy", layout="wide")

# Estados de sesión
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = ''
if 'rol' not in st.session_state:
    st.session_state.rol = ''

# Función para manejar el menú lateral según el rol
def mostrar_menu():
    st.sidebar.title("Menú Principal")
    opciones = ["Dashboard"]

    if st.session_state.rol == "Compras":
        opciones.append("Módulo Compras")
    elif st.session_state.rol == "Almacén":
        opciones.append("Módulo Almacén")
    elif st.session_state.rol == "Auditor":
        opciones.append("Módulo Auditor")

    seleccion = st.sidebar.radio("Navegación", opciones)

    if seleccion == "Dashboard":
        dashboard_screen()
    elif seleccion == "Módulo Compras":
        compras_screen()
    elif seleccion == "Módulo Almacén":
        almacen_screen()
    elif seleccion == "Módulo Auditor":
        auditor_screen()

# Control de flujo de la app
def main():
    if not st.session_state.autenticado:
        login_screen()
    else:
        mostrar_menu()

if __name__ == "__main__":
    main()
