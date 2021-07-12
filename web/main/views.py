from django.shortcuts import render
from django.http import HttpResponse
from .models import Measurements
from .utils import plot

def index(request):
    return HttpResponse('This is the main index and live editing still works')


def sensor_overview(request):
    sensor_history_plots = plot.overview_plot()
    context = { 'plot_divs': sensor_history_plots }
    return render(request, 'main/sensor_overview.html', context)


