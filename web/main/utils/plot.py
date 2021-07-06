import plotly
from plotly.offline import download_plotlyjs, plot
import plotly.graph_objs as go
    
def graph_example():
    labels = [1,2,3,4]
    values = [10,20,30,40]
    ndata = 100
    fig = {
        'data': [{'labels': labels,
          'values': values,
          'type': 'pie',
          'textposition': None,
          'textinfo': "percent",
          'textfont': {'size': 12},
          'showlegend': False}],
        'layout': {'title': 'Total:'+str(ndata),
           'showlegend': False,
           'height': 200,
           'width': 200,
           'autosize': False,
           'margin': {'t': 50,'l': 75,'r': 0,'b': 10},
           'separators': '.,'}
    }

    plt_div = plotly.offline.plot(fig, output_type='div')

    return plt_div
