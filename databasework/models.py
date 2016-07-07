from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Msc(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=True)
    company = models.CharField(max_length=32, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    altitude = models.IntegerField(null=True)

    class Meta:
        db_table = 'msc'

    def __unicode__(self):
        return self.MscName

class Bsc(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=True)
    company = models.CharField(max_length=32, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    msc = models.ForeignKey(Msc)

    class Meta:
        db_table = 'bsc'

class Bts(models.Model):

    name = models.CharField(primary_key=True, max_length=32)
    company = models.CharField(max_length=32, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    bsc_id = models.IntegerField()
    altitude = models.IntegerField(null=True)
    power = models.IntegerField(null=True)

    class Meta:
        db_table = 'bts'

class Ctrl(models.Model):

    bsc = models.ForeignKey(Bsc)
    bts = models.ForeignKey(Bts)

    class Meta:
        db_table = 'ctrl'
        unique_together = ("bsc", "bts")

class Cell(models.Model):

    id = models.IntegerField(primary_key=True, blank=False)
    bts = models.ForeignKey(Bts, db_column='bts_name')
    area_name = models.CharField(max_length=16, null=True, default='')
    lac = models.IntegerField(null=True, default=0)
    longitude = models.FloatField(max_length=8, null=True, default=0.0)
    latitude = models.FloatField(max_length=8, null=True, default=0.0)
    direction = models.IntegerField(null=True, default=0)
    radious = models.IntegerField(null=True, default=0)
    bcch = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'cell'

    def __unicode__(self):
        return self.bstname + ':' + self.area_name

class Ant(models.Model):
    cell = models.ForeignKey(Cell, primary_key=True)
    antenna_high = models.IntegerField(null=True)
    half_angle = models.IntegerField(null=True)
    max_attenuation = models.IntegerField(null=True)
    gain = models.IntegerField(null=True)
    anttilt = models.IntegerField(null=True)
    pt = models.IntegerField(null=True)
    mspwr = models.IntegerField(null=True)

    class Meta:
        db_table = 'ant'

class Ms(models.Model):

    imei = models.CharField(primary_key=True, max_length=16)
    isdn = models.CharField(max_length=16)
    username = models.CharField(max_length=16)
    company = models.CharField(max_length=32)
    gsmmspsense = models.IntegerField()
    gsmmsheight = models.FloatField()
    gsmmspfout = models.FloatField()
    mzone = models.FloatField()

    class Meta:
        db_table = 'ms'

class idle(models.Model):

    cell = models.ForeignKey(Cell)
    ms = models.ForeignKey(Ms)

    class Meta:
        db_table = 'idle'
        unique_together = ("cell", "ms")

class test(models.Model):

    keynum = models.IntegerField(primary_key=True)
    cell = models.ForeignKey(Cell)
    longitude = models.FloatField()
    latitude = models.FloatField()
    rxlev = models.FloatField()

    class Meta:
        db_table = 'test'

class Phone(models.Model):

    date = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    cell = models.ForeignKey(Cell)
    ntch = models.IntegerField()
    traff = models.FloatField()
    rate = models.FloatField()
    thtraff = models.FloatField()
    callnum = models.FloatField()
    congsnum = models.FloatField()
    callcongs = models.FloatField(null=True)

    class Meta:
        db_table = 'phone'
        unique_together = ('date', 'time', "cell")

class Fpnt(models.Model):

    cell_id = models.IntegerField()
    freq = models.IntegerField()

    class Meta:
        db_table = 'fpnt'
        unique_together = ('cell_id', 'freq')

class Distr(models.Model):

    cl_cell = models.ForeignKey(Cell, related_name='cl+')
    fn_cell = models.ForeignKey(Cell, related_name='fn+')

    class Meta:
        db_table = 'distr'
        unique_together = ("cl_cell", "fn_cell")

class ExcelFile(models.Model):

    file_pos = models.FileField(upload_to='./upload/')
    upload_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'excel_file'
