from __future__ import unicode_literals

from django.db import models

# Create your models here.

class BaseStation(models.Model):

    CellID = models.IntegerField(primary_key=True, blank=False)
    BstName = models.CharField(max_length=32, null=True, default='')
    AreaName = models.CharField(max_length=16, null=True, default='')
    LAC = models.IntegerField(null=True, default=0)
    Longitude = models.FloatField(max_length=8, null=True, default=0.0)
    Latitude = models.FloatField(max_length=8, null=True, default=0.0)
    Direction = models.IntegerField(null=True, default=0)
    Bcch = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'base_station'

    def __unicode__(self):
        return self.BstName

class ExcelFile(models.Model):

    filepos = models.FileField(upload_to='./upload/')
    upload_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'excel_file'
