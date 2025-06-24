import psycopg2
import streamlit as st

# Conexión a tu base de datos Supabase (Transaction Pooler)
DB_URL = "postgresql://postgres.jmjbygwaatketijoifrw:Raybarcelona12345*@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

# Función de conexión
def get_connection():
    return psycopg2.connect(DB_URL)

# Insertar o actualizar material
def insertar_material(nombre, cantidad, min_stock, max_stock):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO inventario (nombre, cantidad, min_stock, max_stock)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (nombre) DO UPDATE SET
                cantidad = EXCLUDED.cantidad,
                min_stock = EXCLUDED.min_stock,
                max_stock = EXCLUDED.max_stock;
        """, (nombre, cantidad, min_stock, max_stock))
        conn.commit()
        st.success(f"✅ Material '{nombre}' registrado correctamente.")
    except Exception as e:
        st.error(f"❌ Error al insertar material: {e}")
    finally:
        cursor.close()
        conn.close()

# Consultar todo el inventario
def obtener_inventario():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre, cantidad, min_stock, max_stock FROM inventario ORDER BY nombre;")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        st.error(f"❌ Error al obtener inventario: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Registrar salida de material
def registrar_salida(nombre, cantidad_salida):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE inventario
            SET cantidad = cantidad - %s
            WHERE nombre = %s;
        """, (cantidad_salida, nombre))
        conn.commit()
        st.success(f"✅ Salida registrada correctamente para '{nombre}'.")
    except Exception as e:
        st.error(f"❌ Error al registrar salida: {e}")
    finally:
        cursor.close()
        conn.close()
