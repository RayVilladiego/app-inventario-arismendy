import psycopg2
import pandas as pd
import streamlit as st

# Reemplaza con tu cadena de conexión real
DB_URL = "postgresql://postgres.jmjbygwaatketijoifrw:Raybarcelona12345*@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

@st.cache_resource
def conectar():
    return psycopg2.connect(DB_URL)

def obtener_datos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario;")
    columnas = [desc[0] for desc in cursor.description]
    datos = cursor.fetchall()
    df = pd.DataFrame(datos, columns=columnas)
    cursor.close()
    conn.close()
    return df

def obtener_productos():
    df = obtener_datos()
    return sorted(df['producto'].unique())

def insertar_movimiento(producto, cantidad, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimientos (producto, cantidad, tipo, fecha)
        VALUES (%s, %s, %s, NOW());
    """, (producto, cantidad, tipo))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_stock(producto, cantidad, tipo):
    conn = conectar()
    cursor = conn.cursor()
    operador = '+' if tipo == 'entrada' else '-'
    cursor.execute(f"""
        UPDATE inventario
        SET total = GREATEST(total {operador} %s, 0)
        WHERE producto = %s;
    """, (cantidad, producto))
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_stock_fisico(producto, cantidad_fisico):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE inventario
        SET fisico = %s
        WHERE producto = %s;
    """, (cantidad_fisico, producto))
    conn.commit()
    cursor.close()
    conn.close()

