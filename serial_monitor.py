from serial import Serial
from datetime import datetime
import re
import time
import sqlite3
import utils


serial_params = {'port': '/dev/ttyACM0', 'baudrate': 9600}

conn = Serial(serial_params['port'], serial_params['baudrate'], timeout=1)

reading = True
measurement_dict = {}
while reading:
    line = conn.readline()
    if line:
        time.sleep(0.33)
        date_read = datetime.today().strftime('%Y-%m-%d-%H:%M')
        measurement_dict['date_read'] = date_read
        measurement = line.decode().split(':')
        if len(measurement) > 1:
            measurement_dict[measurement[0]] = measurement[1].replace('\r\n', '')
        else:
            print(measurement_dict)
            db_conn = sqlite3.connect('data/internal.db')
            cur = db_conn.cursor()
            split_temp = measurement_dict['Temperature'].strip().split(' ')
            temperature_value, temperature_unit = float(split_temp[0]), split_temp[1]
            cur.execute('insert into measurements values (?, ?, ?, ?, ?, ?)', [measurement_dict['date_read'], utils.convert_temp(temperature_value, temperature_unit),\
                    measurement_dict['Light level'], measurement_dict['Humidity'].strip().split(' ')[0], measurement_dict['Soil moisture'], measurement_dict['Water']])
            db_conn.commit()
            db_conn.close()
            print(f'measurements written at {date_read}')
            measurement_dict = {}

conn.close()

