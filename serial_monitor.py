from serial import Serial
from datetime import datetime
import re
import time


serial_params = {'port': '/dev/ttyACM0', 'baudrate': 9600}

conn = Serial(serial_params['port'], serial_params['baudrate'], timeout=1)

reading = True
measurement_dict = {}
while reading:
    line = conn.readline()
    if line:
        time.sleep(1)
        date_read = datetime.today().strftime('%Y-%m-%d-%H:%M')
        measurement_dict['date_read'] = date_read
        measurement = line.decode().split(':')
        if len(measurement) > 1:
            measurement_dict[measurement[0]] = measurement[1].replace('\r\n', '')
        else:
            print(measurement_dict)
            measurement_dict = {}

conn.close()

