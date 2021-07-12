from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.sensor_overview, name='sensor_status'),
]

