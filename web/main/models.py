from django.db import models


class Sensors(models.Model):
    
    name = models.CharField(max_length=32)
    relative_coor_north = models.FloatField()
    relative_coor_west = models.FloatField()
    read_date = models.DateTimeField()
    read_value = models.FloatField()


    class Meta:
        ordering = ['-name']


    def __str__(self):
        return self.name


