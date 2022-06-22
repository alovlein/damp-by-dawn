import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plotly_horizon(df, x_column_name, y_column_name, label_column_name, overwrite_columns=False):
    assert x_column_name in df.columns
    assert y_column_name in df.columns
    assert label_column_name in df.columns
    if not overwrite_columns:
      assert 'normalized' not in df.columns
      assert 'bandwidth' not in df.columns
      assert 'average' not in df.columns
      assert 'color' not in df.columns

    average = df.groupby(label_column_name)[y_column_name].transform('mean')
    df['average'] = average
    stdev = df.groupby(label_column_name)[y_column_name].transform('std')
    df['normalized'] = (df[y_column_name] - average) / stdev

    df['bandwidth'] = 1  # TODO: set bandwidth s.t. we always see atleast 4 levels (but we cap at 6...)

    conditions = [
        (df['normalized'] > 2 * df['bandwidth']),
        (df['normalized'] >= df['bandwidth']),
        (df['normalized'] >= 0.),
        (df['normalized'] >= -df['bandwidth']),
        (df['normalized'] >= -2 * df['bandwidth']),
        (df['normalized'] < - 2 * df['bandwidth']),
    ]
    choices = ['#2166AC', '#4393C3', '#92C5DE', '#F4A582', '#D6604D', '#B2182B']
    df['color'] = np.select(conditions, choices)

    unique_labels = np.unique(df[label_column_name])

    fig = make_subplots(rows=unique_labels.shape[0], cols=2, shared_xaxes=True, vertical_spacing=0.02)
    for row_num, label in enumerate(unique_labels):
        subset = df[df[label_column_name] == label]
        offset = subset['bandwidth'].iloc[0]
        color_cond = (subset['color'] != choices[2]) & (subset['color'] != choices[1]) & (subset['color'] != choices[0])
        row_num += 1
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=subset['normalized'].mask(color_cond, 0.).clip(upper=offset),
            mode='none',
            fill='tozeroy',
            fillcolor=choices[2]
        ), row=row_num, col=1)
        color_cond = ((subset['color'] != choices[1]) & (subset['color'] != choices[0]))
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=(subset['normalized'] - 1 * subset['bandwidth']).mask(color_cond, 0.).clip(upper=offset),
            mode='none',
            fill='tozeroy',
            fillcolor=choices[1]
        ), row=row_num, col=1)
        color_cond = subset['color'] != choices[0]
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=(subset['normalized'] - 2 * subset['bandwidth']).mask(color_cond, 0.).clip(upper=offset),
            mode='none',
            fill='tozeroy',
            fillcolor=choices[0]
        ), row=row_num, col=1)
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=np.ones(subset.shape[0]) * offset,
            mode='lines',
            line_color='rgba(0., 0., 0., 0.)'
        ), row=row_num, col=1)
        color_cond = subset['color'] != choices[5]
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=(subset['normalized'] + 3 * subset['bandwidth']).mask(color_cond, offset).clip(lower=0.),
            mode='none',
            fill='tonexty',
            fillcolor=choices[5]
        ), row=row_num, col=1)
        color_cond = (subset['color'] != choices[5]) & (subset['color'] != choices[4])
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=(subset['normalized'] + 2 * subset['bandwidth']).mask(color_cond, offset).clip(lower=0.),
            mode='none',
            fill='tonexty',
            fillcolor=choices[4]
        ), row=row_num, col=1)
        color_cond = (subset['color'] != choices[5]) & (subset['color'] != choices[4]) & (subset['color'] != choices[3])
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=(subset['normalized'] + 1 * subset['bandwidth']).mask(color_cond, offset).clip(lower=0.),
            mode='none',
            fill='tonexty',
            fillcolor=choices[3]
        ), row=row_num, col=1)

        fig.add_annotation(
            xref="x domain", yref="y domain",
            x=0.01, y=0.5, showarrow=False,
            bgcolor="white", opacity=0.85,
            row=row_num, col=1,
            text=f'{label}: {np.round(subset["average"].iloc[0], 1)}',
            font=dict(
                family="Courier New, monospace",
                color="black"
            )
        )
        fig.add_trace(go.Scatter(
            x=subset['timestamp'],
            y=subset['normalized'],
            mode='none',
            fill='tozeroy',
            fillcolor='black'
        ), row=row_num, col=2)

    fig.update_layout(title_text='Horizon Charts', showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=False, showticklabels=False)
    fig.show()
