import sqlite3

conn = sqlite3.connect('external.db')
cur = conn.cursor()

cur.execute('create table forecasts (query_date, forecast_date, icon, temperature, wind_speed, wind_direction, precipitation, sunlight)')

conn.commit()
conn.close()

conn = sqlite3.connect('internal.db')
cur = conn.cursor()

cur.execute('create table measurements (date, temperature, sunlight, humidity, moisture, precipitation)')

conn.commit()
conn.close()

