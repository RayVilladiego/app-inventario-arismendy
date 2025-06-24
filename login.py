import streamlit as st

# Usuarios de prueba (puedes agregar más)
USUARIOS = {
    "admin": {"password": "1234", "rol": "Compras"},
    "almacen": {"password": "4567", "rol": "Almacén"},
    "auditor": {"password": "7890", "rol": "Auditor"}
}

def login():
    st.title("Bienvenido al sistema de gestión de inventario")
    st.subheader("División de Almacén - Arismendy")

    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")
    boton_login = st.button("Iniciar sesión")

    if boton_login:
        if usuario in USUARIOS and USUARIOS[usuario]["password"] == contraseña:
            st.success(f"Inicio de sesión exitoso como {USUARIOS[usuario]['rol']}")
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = USUARIOS[usuario]["rol"]
            st.session_state["autenticado"] = True
        else:
            st.error("Usuario o contraseña incorrectos")
