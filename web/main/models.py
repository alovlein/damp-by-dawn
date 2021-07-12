from django.db import models


class Measurements(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    sensor_id = models.CharField(max_length=32, default='')
    measurement_date = models.TextField(default='', blank=True, null=True)
    temperature = models.FloatField()
    sunlight = models.FloatField()
    humidity = models.FloatField()
    moisture = models.FloatField()
    precipitation = models.FloatField()

    class Meta:
        managed = False
        db_table = 'measurements'


class ForecastsDaily(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    query_date = models.TextField(default='', blank=True, null=True)
    forecast_date = models.TextField(default='', blank=True, null=True)
    icon = models.TextField(default='', blank=True, null=True)
    precipitation_chance = models.TextField(default='', blank=True, null=True)
    precipitation_amount = models.TextField(default='', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forecasts_daily'


class ForecastsHourly(models.Model):
    pk_id = models.IntegerField(primary_key=True)
    query_date = models.TextField(default='', blank=True, null=True)
    forecast_date = models.TextField(default='', blank=True, null=True)
    icon = models.TextField(default='', blank=True, null=True)
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    wind_west = models.IntegerField()
    wind_north = models.IntegerField()
    sunlight = models.FloatField()

    class Meta:
        managed = False
        db_table = 'forecasts_hourly'


