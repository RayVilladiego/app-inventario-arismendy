# main.py

import streamlit as st
from login import check_login

# Módulos por rol
import importlib

ROL_MODULOS = {
    "compras": "mod_compras",
    "almacen": "mod_almacen",
    "auditor": "mod_auditor",
    "admin": "dashboard"
}

st.set_page_config(page_title="WMS - Control de Inventario", layout="wide")

# Autenticación
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "rol" not in st.session_state:
    st.session_state.rol = None
if "usuario" not in st.session_state:
    st.session_state.usuario = None

def login_ui():
    st.title("🔐 Sistema WMS - Inicio de sesión")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        rol = check_login(user, password)
        if rol:
            st.session_state.logged_in = True
            st.session_state.rol = rol
            st.session_state.usuario = user
            st.success(f"Bienvenido, {user.upper()} ({rol.upper()})")
            st.experimental_rerun()
        else:
            st.error("Credenciales inválidas")

def logout_ui():
    st.sidebar.markdown(f"👤 Usuario: `{st.session_state.usuario}` ({st.session_state.rol})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.usuario = None
        st.session_state.rol = None
        st.experimental_rerun()

# Interfaz principal
if not st.session_state.logged_in:
    login_ui()
else:
    logout_ui()

    rol = st.session_state.rol
    modulo = ROL_MODULOS.get(rol)
