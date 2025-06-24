import psycopg2
import pandas as pd

# Conexión a Supabase (Transaction Pooler)
DB_URL = "postgresql://postgres.jmjbygwaatketijoifrw:Raybarcelona12345*@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

def conectar():
    return psycopg2.connect(DB_URL)

def crear_tabla():
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            nombre TEXT PRIMARY KEY,
            cantidad INTEGER NOT NULL,
            min_stock INTEGER,
            max_stock INTEGER
        );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error creando la tabla:", e)

def insertar_material(nombre, cantidad, min_stock, max_stock):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM inventario WHERE nombre = %s", (nombre,))
    if cur.fetchone():
        cur.execute("""
            UPDATE inventario
            SET cantidad = cantidad + %s, min_stock = %s, max_stock = %s
            WHERE nombre = %s
        """, (cantidad, min_stock, max_stock, nombre))
    else:
        cur.execute("""
            INSERT INTO inventario (nombre, cantidad, min_stock, max_stock)
            VALUES (%s, %s, %s, %s)
        """, (nombre, cantidad, min_stock, max_stock))
    conn.commit()
    cur.close()
    conn.close()

def actualizar_stock(nombre, cantidad_salida):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT cantidad FROM inventario WHERE nombre = %s", (nombre,))
    resultado = cur.fetchone()

    if not resultado:
        return "no_encontrado"

    cantidad_actual = resultado[0]
    if cantidad_actual < cantidad_salida:
        return "stock_insuficiente"

    nueva_cantidad = cantidad_actual - cantidad_salida
    cur.execute("UPDATE inventario SET cantidad = %s WHERE nombre = %s", (nueva_cantidad, nombre))
    conn.commit()
    cur.close()
    conn.close()
    return "actualizado"

def obtener_datos():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM inventario", conn)
    conn.close()
    return df

def actualizar_stock_fisico(nombre, cantidad_fisica):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE inventario SET cantidad = %s WHERE nombre = %s", (cantidad_fisica, nombre))
    conn.commit()
    cur.close()
    conn.close()


