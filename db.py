import psycopg2
import pandas as pd

# Parámetros de conexión al Transaction Pooler de Supabase
DB_HOST = "aws-0-us-east-2.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.jmjbygwaatketijoifrw"
DB_PASSWORD = "Raybarcelona12345*"
DB_PORT = "6543"

def conectar():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None

def ejecutar_consulta(query, params=None, fetch=False):
    conn = conectar()
    result = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                columns = [desc[0] for desc in cursor.description]
                result = pd.DataFrame(cursor.fetchall(), columns=columns)
            conn.commit()
            cursor.close()
        except Exception as e:
            print("Error al ejecutar la consulta:", e)
        finally:
            conn.close()
    return result
