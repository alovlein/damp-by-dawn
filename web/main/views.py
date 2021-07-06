from django.shortcuts import render
from django.http import HttpResponse
from .models import Sensors

def index(request):
    return HttpResponse('This is the main index and live editing still works')

def sensor_current_status(request, sensor_id):
    sensor_statuses = Sensors.objects.filter(name__startswith=sensor_id).order_by('name')
    context = {'sensor_statuses': sensor_statuses}
    return render(request, 'main/sensor_status.html', context)

def sensor_history(request, sensor_id):
    return HttpResponse(f'This houses the historical sensor readings graphs for sensor {sensor_id}')


