from serial import Serial
from datetime import datetime
import time
import utils


serial_params = {'port': '/dev/ttyACM0', 'baudrate': 9600}

conn = Serial(serial_params['port'], serial_params['baudrate'], timeout=1)

latitude, longitude = 45.1219, -93.4000
forecast_counter = 0

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
            utils.ingest_measurement(measurement_dict)

            forecast_counter += 1
            if forecast_counter % 12 == 0:
                try:
                    utils.ingest_forecast(latitude, longitude, 'hourly')
                except KeyError:
                    utils.ingest_forecast(latitude, longitude, 'hourly', overwrite=True)
            if forecast_counter % 72 == 0:
                try:
                    utils.ingest_forecast(latitude, longitude, 'daily')
                except KeyError:
                    utils.ingest_forecast(latitude, longitude, 'daily', overwrite=True)
                forecast_counter = 0

conn.close()

