import streamlit as st

# Diccionario simulado de usuarios
usuarios = {
    "admin": {"contraseña": "1234", "rol": "Compras"},
    "compras": {"contraseña": "compra123", "rol": "Compras"},
    "almacen": {"contraseña": "almacen123", "rol": "Almacén"},
    "auditor": {"contraseña": "auditor123", "rol": "Auditor"}
}

def login_screen():
    st.title("🔐 Sistema de Inventario Arismendy")
    st.subheader("Inicio de sesión")

    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")
    login_btn = st.button("Iniciar sesión")

    if login_btn:
        if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.session_state.rol = usuarios[usuario]["rol"]
            st.success(f"Bienvenido, {usuario}")
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

