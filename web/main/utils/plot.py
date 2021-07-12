import sqlite3
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np


def overview_plot():
    plot_divs = []

    conn = sqlite3.connect('../data/internal.db')
    unique_sensors = pd.read_sql('select distinct sensor_id from measurements', con=conn)
    conn.commit()
    for sensor_id in unique_sensors:
        sensor_data = pd.read_sql('select * from measurements where sensor_id=:sid', con=conn, params={'sid': sensor_id})
        conn.commit()
    conn.close()

    # temporary while we wait for data to load in new schema
    x = np.linspace(-6, 6, num=5000)
    y = np.sin(x) + (np.random.rand(5000) * 2) - 1

    fig = go.Figure()
    scatter = go.Scatter(x=x, y=y, mode='lines', name='test', opacity=0.8, marker_color='blue')
    fig.add_trace(scatter)

    plot_divs.append(plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text=''))

    
    fig = go.Figure()
    scatter = go.Scatter(x=x, y=y, mode='lines', name='test', opacity=0.8, marker_color='purple')
    fig.add_trace(scatter)

    plot_divs.append(plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text=''))


    fig = go.Figure()
    scatter = go.Scatter(x=x, y=y, mode='lines', name='test', opacity=0.8, marker_color='green')
    fig.add_trace(scatter)

    plot_divs.append(plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text=''))

    return plot_divs


def plot_history():
    return True

