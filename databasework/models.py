from __future__ import unicode_literals

from django.db import models
from django import forms
import math

# Create your models here.

class Msc(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=True)
    company = models.CharField(max_length=32, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    altitude = models.IntegerField(null=True)

    class Meta:
        db_table = 'msc'

    def __unicode__(self):
        return self.MscName

    def setattr(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

class Bsc(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=True)
    company = models.CharField(max_length=32, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    msc = models.ForeignKey(Msc, null=True)

    class Meta:
        db_table = 'bsc'

    def setattr(self, key, value):
        if key == 'msc':
            self.msc = Msc.objects.filter(id=value).first()
        elif hasattr(self, key):
            setattr(self, key, value)

class Bts(models.Model):

    name = models.CharField(primary_key=True, max_length=32)
    company = models.CharField(max_length=32, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    bsc_id = models.IntegerField(null=True)
    altitude = models.IntegerField(null=True)
    power = models.IntegerField(null=True)

    class Meta:
        db_table = 'bts'

    def setattr(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

class Ctrl(models.Model):

    bsc = models.ForeignKey(Bsc)
    bts = models.ForeignKey(Bts)

    class Meta:
        db_table = 'ctrl'
        unique_together = ("bsc", "bts")

    def setattr(self, key, value):
        if key == 'bsc':
            self.bsc = Bsc.objects.filter(pk=value).first()
        elif key == 'bts':
            self.bts = Bts.objects.filter(pk=value).first()

class Cell(models.Model):

    id = models.IntegerField(primary_key=True)
    bts = models.ForeignKey(Bts, db_column='bts_name', null=True)
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

    def setattr(self, key, value):
        if key == 'bts':
            self.bts = Bts.objects.filter(pk=value).first()
        elif hasattr(self, key):
            setattr(self, key, value)

class Ant(models.Model):
    cell = models.OneToOneField(Cell, primary_key=True)
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

    imei = models.CharField(primary_key=True, max_length=32)
    isdn = models.CharField(max_length=16)
    username = models.CharField(max_length=16)
    company = models.CharField(max_length=32)
    gsmmspsense = models.IntegerField()
    gsmmsheight = models.FloatField()
    gsmmspfout = models.FloatField()
    mzone = models.CharField(max_length=16, null=True)

    class Meta:
        db_table = 'ms'



class Idle(models.Model):

    cell = models.ForeignKey(Cell)
    ms = models.ForeignKey(Ms)

    class Meta:
        db_table = 'idle'
        unique_together = ("cell", "ms")

    def setattr(self, key, value):
        if key == 'cell':
            self.cell = Cell.objects.filter(pk=value).first()
        elif key == 'ms':
            self.ms = Ms.objects.filter(pk=value).first()

class Test(models.Model):

    keynum = models.IntegerField(primary_key=True)
    cell = models.ForeignKey(Cell)
    longitude = models.FloatField()
    latitude = models.FloatField()
    rxlev = models.FloatField()

    class Meta:
        db_table = 'test'

    def setattr(self, key, value):
        if key == 'cell':
            self.cell = Cell.objects.filter(pk=value).first()
        elif hasattr(self, key):
            setattr(self, key, value)

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

    def setattr(self, key, value):
        if key == 'cell':
            self.cell = Cell.objects.filter(pk=value).first()
        elif hasattr(self, key):
            setattr(self, key, value)

class Fpnt(models.Model):

    cell_id = models.IntegerField()
    freq = models.IntegerField()

    class Meta:
        db_table = 'fpnt'
        unique_together = ('cell_id', 'freq')


class Distr(models.Model):

    cl_cell = models.ForeignKey(Cell, related_name='cl+')
    fn_cell = models.ForeignKey(Cell, related_name='fn+')
    distance = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'distr'
        unique_together = ("cl_cell", "fn_cell")

    def setattr(self, key, value):
        if key == 'cl_cell':
            self.cl_cell = Cell.objects.filter(pk=value).first()
        elif key == 'fn_cell':
            self.fn_cell = Cell.objects.filter(pk=value).first()
        elif hasattr(self, key):
            setattr(self, key, value)

    @classmethod
    def get_neighbor(cls, cell):
        return cls.objects.filter(cl_cell=cell).order_by("distance").all()

    def get_distance(self):
        lat1 = self.cl_cell.latitude * math.pi / 180
        lat2 = self.fn_cell.latitude * math.pi / 180
        a = lat1 - lat2
        b = self.cl_cell.longitude * math.pi / 180 - self.fn_cell.longitude * math.pi  / 180
        s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2, 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(b/2), 2)))
        s *= 63781370
        return int(math.floor(s))


    @classmethod
    def cal_neighbor(cls, cell):
        cells = Cell.objects.all()
        for r in cells:
            if r.id == cell.id:
                continue
            now = cls.objects.create(cl_cell=cell, fn_cell=r)
            now.distance = now.get_distance()
            if now.distance < cell.radious:
                now.save()


class ExcelFile(models.Model):

    file_pos = models.FileField(upload_to='./upload/')
    upload_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'excel_file'

class UploadFileForm(forms.Form):

    title = forms.CharField(max_length=64)
    filetype = forms.CharField(max_length=32)
    thefile = forms.FileField()


