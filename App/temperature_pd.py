import pandas as pd
import psycopg2
import os
from config import config

def connect_database_local():
    params = config()
    conn = psycopg2.connect(**params)
    return conn


def connect_database():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def data_today(conn, date=None):
    # TODO - Add exception handling for no data
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT created_on, temperature, humidity
        FROM dht_data
        WHERE created_on::date = now()::date
        """)
    if cursor.rowcount == 0:
        print("[WARN] No data found for today.")
        return None

    tuples = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(tuples, columns=["time", "temperature", "humidity"])
    df['time'] = pd.to_datetime(df['time']).dt.tz_convert("Asia/Calcutta")
    df['temperature'] = pd.to_numeric(df['temperature'])
    df['humidity'] = pd.to_numeric(df['humidity'])
    return df