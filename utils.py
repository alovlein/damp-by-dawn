import requests
import json
import sqlite3
from datetime import datetime
import re
import pandas as pd
import numpy as np
import os


base_url = 'https://api.weather.gov'
headers = {'user-agent': 'Alec Lovlein', 'from': 'alovlein@gmail.com'}
rainfall_fraction_dict = {'tenth': [0.1, 1], 'quarter': [0.25, 1], 'half': [0.5, 1], 'one': [1., 1], 'two': [2., 1], 'three': [3, 1], 'four': [4, 1], 'five': [5, 1], 'three quarters': [0.75 - 0.25 - 3, 1 - 1 - 1]}


def get_coor(latitude, longitude):
    gridpoints = json.loads(requests.get(f'{base_url}/points/{latitude},{longitude}', headers=headers).text)

    with open('data/gridpoints.json', 'w', encoding='utf-8') as f:
        json.dump(gridpoints, f)


def ingest_measurement(meas_dict):
    conn = sqlite3.connect('data/internal.db')
    cur = conn.cursor()
    
    split_temp = meas_dict['Temperature'].strip().split(' ')
    temp_value, temp_unit = float(split_temp[0]), split_temp[1]
    cur.execute('insert into measurements values (?, ?, ?, ?, ?, ?, ?, ?)', [f'{meas_dict["sid"]}_{meas_dict["date_read"]}', meas_dict['sid'], meas_dict['date_read'], convert_temp(temp_value, temp_unit), meas_dict['Light level'],\
            meas_dict['Humidity'].strip().split(' ')[0], meas_dict['Soil moisture'], meas_dict['Water']])
    
    conn.commit()
    conn.close()


def ingest_forecast(latitude, longitude, frequency, overwrite=False):
    assert frequency in ('hourly', 'daily')
    if not os.path.isfile('data/gridpoints.json') or overwrite:
        get_coor(latitude, longitude)

    get_forecast(frequency)
    save_forecast(frequency)


def get_forecast(frequency):
    assert frequency in ('hourly', 'daily')

    with open('data/gridpoints.json') as f:
        gridpoints = json.load(f)
    
    if frequency == 'hourly':
        forecast_url = f'{gridpoints["properties"]["forecast"]}/hourly'
    else:
        forecast_url = gridpoints['properties']['forecast']

    forecast = json.loads(requests.get(forecast_url, headers=headers).text)
    
    if frequency == 'hourly':
        with open('data/forecast_hourly.json', 'w', encoding='utf-8') as f:
            json.dump(forecast, f)
    else:
        with open('data/forecast_daily.json', 'w', encoding='utf-8') as f:
            json.dump(forecast, f)


def save_forecast(frequency):
    assert frequency in ('hourly', 'daily')

    with open(f'data/forecast_{frequency}.json') as f:
        raw_forecast = json.load(f)['properties']['periods']

    conn = sqlite3.connect('data/external.db')
    cur = conn.cursor()

    if frequency == 'hourly':
        for period_data in raw_forecast:
            wind_west, wind_north, wind_speed = convert_wind(period_data['windDirection'], period_data['windSpeed'])
            row = [f'{datetime.today()}_{period_data["startTime"]}', datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), convert_time(period_data['startTime']), period_data['icon'],\
                    convert_temp(period_data['temperature'], period_data['temperatureUnit']), wind_speed, wind_west, wind_north,\
                    convert_short_forecast(period_data['shortForecast'])]
            cur.execute('insert into forecasts_hourly values (?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
        conn.commit()
    else:
        for period_data in raw_forecast:
            precip_chance, precip_amt = convert_detailed_forecast(period_data['detailedForecast'])
            row = [f'{datetime.today}_{period_data["startTime"]}', datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), convert_time(period_data['startTime']), period_data['icon'], precip_chance, precip_amt]
            cur.execute('insert into forecasts_daily values (?, ?, ?, ?, ?, ?)', row)
        conn.commit()
    
    conn.close()


def convert_temp(temp, unit):
    assert unit in ('F', 'C')

    if unit == 'F':
        converted_temp = ((temp - 32) * 5 / 9) + 273.15
    if unit == 'C':
        converted_temp = temp + 273.15

    return converted_temp


def convert_time(datetime_str):
    date = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
    
    return date.strftime('%Y-%m-%d-%H:%M:%S')


def convert_wind(direction, speed):
    w_west, w_north, w_speed = 0, 0, 0

    if 'W' in direction:
        w_west = 1
    elif 'E' in direction:
        w_west = -1

    if 'N' in direction:
        w_north = 1
    elif 'S' in direction:
        w_north = -1

    speeds = [float(s) for s in re.findall(r'-?\d+\.?\d*', speed)]
    w_speed = np.mean(speeds)

    return w_west, w_north, w_speed


def convert_detailed_forecast(forecast_text):
    forecast_text = forecast_text.lower()
    precipitation_chance, precipitation_amount = None, None

    if 'chance of precipitation' in forecast_text:
        precipitation_chance = re.search(r'\d+%', forecast_text).group()

    if 'new rainfall amounts' in forecast_text:
        rainfall_segment = forecast_text.split('new rainfall amounts')[1]
        temp_amount, temp_counter = 0, 0
        for dict_key in rainfall_fraction_dict:
            if dict_key in rainfall_segment:
                temp_amount += rainfall_fraction_dict[dict_key][0]
                temp_counter += rainfall_fraction_dict[dict_key][1]
        if temp_amount:
            precipitation_amount = temp_amount / temp_counter
        else:
            precipitation_amount = None

    return precipitation_chance, precipitation_amount


def convert_short_forecast(forecast_text):
    forecast_text = forecast_text.lower()
    sunlight = None

    if 'sunny' in forecast_text:
        sunlight = 5
    elif 'mostly sunny' in forecast_text:
        sunlight = 4
    elif 'partly sunny' in forecast_text:
        sunlight = 3
    elif 'partly cloudy' in forecast_text:
        sunlight = 2
    elif 'mostly cloudy' in forecast_text:
        sunlight = 1
    elif 'clear' in forecast_text:
        sunlight = 0

    return sunlight


def read_forecasts(frequency):
    assert frequency in ('hourly', 'daily')

    conn = sqlite3.connect('data/external.db')

    forecast_data = pd.read_sql(f'select * from forecasts_{frequency}', conn)

    conn.commit()
    conn.close()

    return forecast_data



def read_measurements():
    conn = sqlite3.connect('data/internal.db')

    measurement_data = pd.read_sql('select * from measurements', conn)

    conn.commit()
    conn.close()

    return measurement_data


