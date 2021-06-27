import utils
import os


lat, lon = 45.1219, -93.4000
def get_fresh_forecast(latitude, longitude, frequency, overwrite=False):
    assert frequency in ('hourly', 'daily')
    if os.path.isfile('data/gridpoints.json') and not overwrite:
        print('using stored gridpoints, if overwrite is needed re-run with overwrite=True')
    else:
        utils.get_coor(latitude, longitude)

    utils.get_forecast(frequency)
    utils.save_forecast(frequency)

get_fresh_forecast(lat, lon, 'hourly')
get_fresh_forecast(lat, lon, 'daily')

