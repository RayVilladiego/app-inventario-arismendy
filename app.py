import streamlit as st
from login import login_screen
from dashboard import dashboard_screen
from mod_compras import compras_screen
from mod_almacen import almacen_screen
from mod_auditor import auditor_screen

# Inicializar variables de sesión
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario' not in st.session_state:
    st.session_state.usuario = ''
if 'rol' not in st.session_state:
    st.session_state.rol = ''

# Función para mostrar menú según el rol
def mostrar_menu():
    st.sidebar.title("📊 Menú Principal")
    st.sidebar.write(f"👤 Usuario: {st.session_state.usuario}")
    st.sidebar.write(f"🔐 Rol: {st.session_state.rol}")
    
    opciones = []
    if st.session_state.rol == "Compras":
        opciones = ["Dashboard", "Módulo Compras"]
    elif st.session_state.rol == "Almacén":
        opciones = ["Dashboard", "Módulo Almacén"]
    elif st.session_state.rol == "Auditor":
        opciones = ["Dashboard", "Módulo Auditor"]
    opciones.append("Cerrar sesión")
    
    seleccion = st.sidebar.radio("Navegación", opciones)
    
    if seleccion == "Dashboard":
        dashboard_screen()
    elif seleccion == "Módulo Compras":
        compras_screen()
    elif seleccion == "Módulo Almacén":
        almacen_screen()
    elif seleccion == "Módulo Auditor":
        auditor_screen()
    elif seleccion == "Cerrar sesión":
        st.session_state.autenticado = False
        st.session_state.usuario = ''
        st.session_state.rol = ''
        st.experimental_rerun()

# Punto de entrada
def main():
    st.set_page_config(page_title="Sistema Inventario Arismendy", layout="wide")
    if not st.session_state.autenticado:
        login_screen()
    else:
        mostrar_menu()

if __name__ == "__main__":
    main()
