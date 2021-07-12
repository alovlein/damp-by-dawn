from django.contrib import admin
from .models import Measurements, ForecastsDaily, ForecastsHourly 

admin.site.register(Measurements)
admin.site.register(ForecastsDaily)
admin.site.register(ForecastsHourly)

