# db.py

import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "aws-0-us-east-2.pooler.supabase.com",
    "port": "6543",
    "dbname": "postgres",
    "user": "postgres.jmjbygwaatketijoifrw",
    "password": "Raybarcelona12345*"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def fetch_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

def insert_and_return(query, params):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result
