import sqlite3

conn = sqlite3.connect('external.db')
cur = conn.cursor()

cur.execute('create table forecasts_hourly (query_date, forecast_date, icon, temperature, wind_speed, wind_west, wind_north, sunlight)')
cur.execute('create table forecasts_daily (query_date, forecast_date, icon, precipitation_chance, precipitation_amount)')

conn.commit()
conn.close()

conn = sqlite3.connect('internal.db')
cur = conn.cursor()

cur.execute('create table measurements (date, temperature, sunlight, humidity, moisture, precipitation)')

conn.commit()
conn.close()

