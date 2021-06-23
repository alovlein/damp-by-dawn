import requests
import json


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
    
    forecast_url = f'{gridpoints["properties"]["forecast"]}/hourly'
    forecast = json.loads(requests.get(forecast_url, headers=headers).text)
    
    with open('weather_dir/forecast.json', 'w', encoding='utf-8') as f:
        json.dump(forecast, f)


def dissect_forecast():
    with open('weather_dir/forecast.json') as f:
        raw_forecast = json.load(f)['properties']['periods']

    for period_data in raw_forecast:
        print(period_data['startTime'])
        print(period_data['shortForecast'])
        print(period_data['temperature'])

dissect_forecast()

