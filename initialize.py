import sqlite3
from pathlib import Path


Path('data/').mkdir(exist_ok=True)
conn = sqlite3.connect('data/external.db')
cur = conn.cursor()

cur.execute('create table forecasts_hourly (pk_id integer primary key autoincrement, query_date, forecast_date, icon, temperature, wind_speed, wind_west, wind_north, sunlight)')
cur.execute('create table forecasts_daily (pk_id integer primary key autoincrement, query_date, forecast_date, icon, precipitation_chance, precipitation_amount)')

conn.commit()
conn.close()

conn = sqlite3.connect('data/internal.db')
cur = conn.cursor()

cur.execute('create table measurements (pk_id integer primary key autoincrement, sensor_id, measurement_date, temperature, sunlight, humidity, moisture, precipitation)')

conn.commit()
conn.close()

