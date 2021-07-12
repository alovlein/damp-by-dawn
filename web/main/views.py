from django.shortcuts import render
from django.http import HttpResponse
from .models import Measurements
from .utils import plot

def index(request):
    return HttpResponse('This is the main index and live editing still works')

def sensor_current_status(request, sensor_id):
    sensor_statuses = Measurements.objects.filter(sensor_id=sensor_id).using('internal_data')
    context = {'sensor_statuses': sensor_statuses}
    return render(request, 'main/sensor_status.html', context)

def sensor_history(request, sensor_id):
    sensor_history_plot = plot.historical_plot(sensor_id)
    context = { 'plot_div': sensor_history_plot }
    return render(request, 'main/historical_plot.html', context)


