#!/usr/bin/python3
import serial
import time
import sched
import psycopg2
import os
import pytz
from datetime import datetime, timedelta
from config import config

DEVICE_PATH = '/dev/ttyACM1' 
try:
    arduino = serial.Serial(
        port=DEVICE_PATH, # Replace with Arduino path
        baudrate=9600,
        timeout=0.1)
except serial.SerialException as e:
    print(e)

def connect_database():
#    DATABASE_URL = os.environ['DATABASE_URL']
#    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    params = config()
    conn = psycopg2.connect(**params)
    print("Connected to database")
    return conn

def read_data():
    data = arduino.readline().decode('utf-8')[:-2]
    if not data == "":
        t, h = data.split(',')
        t = float(t)
        h = float(h)
    return t, h

def request_data():
    arduino.write('a'.encode())


def log_reading():
    arduino.write('a'.encode())
    time.sleep(2)
    data = arduino.readline().decode('utf-8')[:-2]
    if not data == "":
        t, h = data.split(',')
        t = float(t)
        h = float(h)
        try:
            conn = connect_database()
            cur = conn.cursor()
            ts = datetime.now(pytz.timezone("Asia/Calcutta"))
            cur.execute(
                """INSERT INTO dht_data (created_on, temperature, humidity) values (%s,%s,%s)""",
                (ts, t, h)
            )
            cur.close()
            conn.commit()
            conn.close()
            print("Data logged at", ts)
        except Exception as e:
            # Add data locally till connection is restored
            print("Could not connect to the database with the error:\n", e)


def main():
    last_log = datetime.now(pytz.timezone("Asia/Calcutta")) # Adjust Timezone if required
    print("Data logging started!")
    while True:
        current_time = datetime.now(pytz.timezone("Asia/Calcutta")) # Adjust Timezone if required
        if current_time - last_log > timedelta(minutes=1): # Delay between two readings
            log_reading()
            last_log = current_time
            

if __name__ == '__main__':
    main()
