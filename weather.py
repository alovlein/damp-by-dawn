import requests
import json
import sqlite3
from datetime import datetime
import re
import pandas as pd

base_url = 'https://api.weather.gov'
headers = {'user-agent': 'Alec Lovlein', 'from': 'alovlein@gmail.com'}
lat, lon = 45.1219, -93.4000


def get_coor(latitude, longitude):
    gridpoints = json.loads(requests.get(f'{base_url}/points/{latitude},{longitude}', headers=headers).text)

    with open('weather_dir/gridpoints.json', 'w', encoding='utf-8') as f:
        json.dump(gridpoints, f)


def get_forecast():
    with open('weather_dir/gridpoints.json') as f:
        gridpoints = json.load(f)
    
    forecast_url = gridpoints["properties"]["forecast"]
    forecast = json.loads(requests.get(forecast_url, headers=headers).text)
    
    with open('weather_dir/forecast.json', 'w', encoding='utf-8') as f:
        json.dump(forecast, f)


def save_forecast():
    with open('weather_dir/forecast.json') as f:
        raw_forecast = json.load(f)['properties']['periods']

    conn = sqlite3.connect('external.db')
    cur = conn.cursor()

    for period_data in raw_forecast:
        sunlight, precipitation = decipher_forecast(period_data['detailedForecast'])
        row = [datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), period_data['startTime'], period_data['icon'], convert_temp(period_data['temperature'], period_data['temperatureUnit']),\
                period_data['windSpeed'], period_data['windDirection'], precipitation, sunlight]

        cur.execute(f'insert into forecasts values (?, ?, ?, ?, ?, ?, ?, ?)', row)
    conn.commit()
    conn.close()


def convert_temp(temp, unit):
    assert unit in ('F', 'C')

    if unit == 'F':
        converted_temp = ((temp - 32) * 5 / 9) + 273.15
    if unit == 'C':
        converted_temp = temp + 273.15

    return converted_temp


def decipher_forecast(forecast_text):
    forecast_text = forecast_text.lower()
    precipitation, sunlight = None, None

    if 'sunny' in forecast_text:
        sunlight = 5
    elif 'mostly sunny' in forecast_text:
        sunlight = 4
    elif 'partly sunnyy' in forecast_text:
        sunlight = 3
    elif 'partly cloudy' in forecast_text:
        sunlight = 2
    elif 'mostly cloudy' in forecast_text:
        sunlight = 1
    elif 'clear' in forecast_text:
        sunlight = 0

    if 'chance of precipitation' in forecast_text:
        precipitation = re.search(r'\d+%', forecast_text).group()

    return sunlight, str(precipitation)


def read_forecasts():
    conn = sqlite3.connect('external.db')

    forecast_data = pd.read_sql('select * from forecasts', conn)
    print(forecast_data)

    conn.commit()
    conn.close()


read_forecasts()


