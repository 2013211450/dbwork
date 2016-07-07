# -*- encoding: utf-8 -*-
import os, sys
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from databasework.models import *
from django.db import connection, transaction
import json
import xlrd, xlwt

# Create your views here.
UPLOADMODEL = {
    'cell': Cell,
    'msc': Msc,
    'bsc': Bsc,
    'bts': Bts,
    'phone': Phone,
}

def account_login(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(user)
            return JsonResponse({'code':0, 'reason':u'登录成功'})
        else:
            return JsonResponse({'code': -1, 'reason':u'登录失败'})

@login_required
def bts_query(request):
    user = request.user
    bts_name = request.GET.get('bts_name', None)
    if not bts_name:
        bts = Bts.objects.first()
    else:
        bts = Bts.objects.filter(name=bts_name).first()
    data = {}
    data['bsc_id'] = bts.bsc_id
    data['power'] = bts.power
    data['longitude'] = bts.longitude
    data['latitude'] = bts.latitude
    data['altitude'] = bts.altitude
    data['company'] = bts.company
    data['user'] = user
    return render(request, 'bts.html', data)

@login_required
def cell_query(request):
    user = request.user
    cell_id = request.GET.get('bts_name', None)
    if not cell_id:
        cell = Cell.objects.first()
    else:
        cell = Cell.objects.filter(id=cell_id).first()
    data = {}
    data['bts_name'] = cell.bts.name
    data['area_name'] = cell.area_name
    data['longitude'] = cell.longitude
    data['latitude'] = cell.latitude
    data['direction'] = cell.direction
    data['lac'] = cell.lac
    data['user'] = user
    data['radious'] = cell.radious
    return render(request, 'cell.html', data)



@login_required
def  traffic_query(request):
    if request.method == 'POST':
        mode = int(request.POST.get('mode', 0))
        cell_id = request.POST.get('cell_id', None)
        query_date = request.POST.get('date', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        if cell_id == None or start_time == None or end_time == None:
            return JsonResponse({'code':-1, 'reason':u'缺少必要的参数'})
        cursor = connection.cursor()
        if mode == 0:
            proc_command = 'HOURLY_TRAFF'
            query_command = 'select QTIME, QTRAFFAVG, QCONGRATE, QTRAFFLINE from HOURLY_TRAFF'
        else:
            proc_command = 'Minute_TRAFF'
            if mode == 1:
                query_command = 'select QTIME, QTRAFFAVG15, QTRAFFLINE15 from Minute'
            else:
                query_command = 'select QTIME, QTRAFFAVG, QTRAFFLINE from Minute'
        cursor.calproc(proc_command, (cell_id, query_date, start_time, end_time))
        transaction.commit_unless_managed()
        cursor.execute(query_command)
        data = cursor.fetchall()
        return JsonResponse({'code':0, 'data': data, 'mode': mode})
    else:
        return render(request, 'traffic.html', {'user': request.user})



@login_required
def congestion_query(request):
    if request.method == 'POST':
        cell_id = request.POST.get('cell_id', None)
        query_date = request.POST.get('date', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        if cell_id == None or start_time == None or end_time == None:
            return JsonResponse({'code':-1, 'reason':u'缺少必要的参数'})
        cursor = connection.cursor()
        cursor.calproc('C_PHONE')
        transaction.commit_unless_managed()
        phones = Phone.objects.filter(date=query_date, time__gte=start_time, time_lte=end_time).all()
        data = []
        for r in phones:
            data.append({
                'time': r.time,
                'traff': r.traff,
                'rate': r.rate,
            })
        return JsonResponse({'code':0, 'data': data})
    else:
        return render(request, 'congestion.html', {'user': request.user})


@login_required
def measurement(request):
    if request.method == 'POST':
        cell_id = request.POST.get('cell_id', None)
        query_date = request.POST.get('date', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        if cell_id == None or start_time == None or end_time == None:
            return JsonResponse({'code':-1, 'reason':u'缺少必要的参数'})
        cursor = connection.cursor()
        cursor.calproc('C_PHONE')
        transaction.commit_unless_managed()
        phones = Phone.objects.filter(date=query_date, time__gte=start_time, time_lte=end_time).all()
        data = []
        for r in phones:
            data.append({
                'time': r.time,
                'traff': r.traff,
                'rate': r.rate,
            })
        return JsonResponse({'code':0, 'data': data})
    else:
        return render(request, 'congestion.html', {'user': request.user})


def excel_export(request):
    if request.method == 'POST':
        excel_file = request.FILES['file']
        upload_model = request.POST.get('upload_model')
        filename = str(excel_file)
        if not os.path.exist('upload/'):
            os.mkdir('upload/')
        filename = 'upload/' + filename
        with open(filename, 'wb+') as destination:
            for r in excel_file.chunks():
                destination.write(r)
        excel = xlrd.open_workbook(filename)
        sheet = excel.sheet_by_index(0)
        obj = UPLOADMODEL[upload_model]
        for r in sheet.row_values(0):
            if not hasattr(obj, r):
                return JsonResponse({'code': -1, 'reason': u'数据格式不符合规范'})
        rows = sheet.nrows
        cols = sheet.ncols
        for i in range(1, rows):
            now = obj.objects.create()
            for j in range(0, cols):
                setattr(now, sheet.cell(0, j).value.encode('utf-8'), sheet.cell(i, j).value.encode('utf-8'))
        os.remove(filename)
        return JsonResponse({'code': 0, 'reason': u'导入数据成功'})

def excel_import(request):
    pass
