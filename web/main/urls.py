from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:sensor_id>/', views.sensor_current_status, name='sensor_status'),
    path('<str:sensor_id>/history/', views.sensor_history, name='sensor_history')
]

