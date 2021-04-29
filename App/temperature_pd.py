import pandas as pd
import psycopg2
import os

def connect_database():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def data_today(conn, date=None):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT created_on, temperature, humidity
        FROM dht_data
        WHERE created_on::date = now()::date
        """)
    tuples = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(tuples, columns=["time", "temperature", "humidity"])
    df['time'] = pd.to_datetime(df['time']).dt.tz_convert("Asia/Calcutta")
    df['temperature'] = pd.to_numeric(df['temperature'])
    df['humidity'] = pd.to_numeric(df['humidity'])
    return df