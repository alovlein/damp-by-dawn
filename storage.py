import sqlite3

conn = sqlite3.connect('measurements.db')
cur = conn.cursor()

cur.execute('create table s_0000 (date_meas, temp, humidity, light, water, moisture, health)')
cur.execute('insert into s_0000 values ("2021-06-19 22:09:34", 3, 18, 9291, 22, 1134842, 7)')

conn.commit()
conn.close()

