import psycopg2
import pandas as pd

# Configura tu conexión a Supabase (Transaction Pooler)
DB_URL = "postgresql://postgres.jmjbygwaatketijoifrw:Raybarcelona12345*@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

def obtener_datos():
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventario;")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["nombre", "cantidad", "min_stock", "max_stock"])
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        print("❌ Error al obtener datos:", e)
        return pd.DataFrame()

def insertar_material(nombre, cantidad, min_stock, max_stock):
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventario (nombre, cantidad, min_stock, max_stock)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (nombre) DO UPDATE SET
            cantidad = EXCLUDED.cantidad,
            min_stock = EXCLUDED.min_stock,
            max_stock = EXCLUDED.max_stock;
        """, (nombre, cantidad, min_stock, max_stock))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error al insertar material:", e)

def actualizar_stock(nombre, cantidad_salida):
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad FROM inventario WHERE nombre = %s;", (nombre,))
        result = cursor.fetchone()

        if not result:
            return "no_encontrado"

        cantidad_actual = result[0]
        if cantidad_actual < cantidad_salida:
            return "stock_insuficiente"

        nueva_cantidad = cantidad_actual - cantidad_salida
        cursor.execute("UPDATE inventario SET cantidad = %s WHERE nombre = %s;", (nueva_cantidad, nombre))
        conn.commit()
        cursor.close()
        conn.close()
        return "actualizado"

    except Exception as e:
        print("❌ Error al actualizar stock:", e)
        return "error"
