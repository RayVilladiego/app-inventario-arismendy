# app.py

import streamlit as st
import pandas as pd
import psycopg2

# Configuración de la página
st.set_page_config(page_title="Sistema WMS Arismendy", layout="wide")

# Parámetros de conexión Supabase (Transaction Pooler)
DB_URL = "postgresql://postgres.jmjbygwaatketijoifrw:Raybarcelona12345*@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

@st.cache_resource
def conectar_bd():
    return psycopg2.connect(DB_URL)

conn = conectar_bd()
cursor = conn.cursor()

# --- Funciones de utilidad ---
def cargar_datos():
    cursor.execute("SELECT * FROM inventario ORDER BY codigo")
    columnas = [desc[0] for desc in cursor.description]
    return pd.DataFrame(cursor.fetchall(), columns=columnas)

def registrar_movimiento(codigo, cantidad, tipo):
    cursor.execute("""
        INSERT INTO movimientos (codigo, cantidad, tipo, fecha)
        VALUES (%s, %s, %s, NOW())
    """, (codigo, cantidad, tipo))
    conn.commit()

def actualizar_stock(codigo, cantidad, tipo):
    if tipo == "entrada":
        cursor.execute("UPDATE inventario SET total = total + %s WHERE codigo = %s", (cantidad, codigo))
    else:
        cursor.execute("UPDATE inventario SET total = total - %s WHERE codigo = %s", (cantidad, codigo))
    conn.commit()

# --- Interfaz ---
st.title("📦 Sistema de Inventario - Arismendy")

rol = st.sidebar.selectbox("Selecciona tu rol", ["Compras", "Almacén", "Auditor"])

if rol == "Compras":
    st.header("📝 Registro de Entrada de Materiales")
    df = cargar_datos()
    material = st.selectbox("Selecciona el material", df['material'])
    cantidad = st.number_input("Cantidad a ingresar", min_value=1)

    if st.button("Registrar entrada"):
        codigo = df[df['material'] == material]['codigo'].values[0]
        registrar_movimiento(codigo, cantidad, "entrada")
        actualizar_stock(codigo, cantidad, "entrada")
        st.success("✅ Entrada registrada y stock actualizado.")

elif rol == "Almacén":
    st.header("📤 Registro de Salida de Materiales")
    df = cargar_datos()
    material = st.selectbox("Selecciona el material", df['material'])
    cantidad = st.number_input("Cantidad a retirar", min_value=1)

    if st.button("Registrar salida"):
        codigo = df[df['material'] == material]['codigo'].values[0]
        registrar_movimiento(codigo, cantidad, "salida")
        actualizar_stock(codigo, cantidad, "salida")
        st.success("✅ Salida registrada y stock actualizado.")

elif rol == "Auditor":
    st.header("📊 Visualización de Inventario")
    df = cargar_datos()

    def calcular_estado(fila):
        if fila['total'] < fila['min']:
            return "🔴 Bajo"
        elif fila['total'] < fila['max']:
            return "🟡 Alerta"
        else:
            return "🟢 OK"

    df["estado"] = df.apply(calcular_estado, axis=1)
    st.dataframe(df)

    st.markdown("### 🔍 Productos Críticos")
    st.dataframe(df[df["estado"] != "🟢 OK"])

