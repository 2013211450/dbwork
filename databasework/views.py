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
    'Cell': Cell,
    'Msc': Msc,
    'Bsc': Bsc,
    'Bts': Bts,
    'Phone': Phone,
    'Ms': Ms,
    'Ant': Ant,
    'Test': Test,
    'Fpnt': Fpnt,
}
CHOICES = [
    ('Cell', u'小区Cell信息'),
    ('Ms', u'移动台MS信息'),
    ('Msc', 'Msc'),
    ('Bts', 'Bts'),
    ('Bsc', 'Bsc'),
    ('Ant', 'Ant'),
    ('Phone', 'Phone'),
    ('Test', 'Test'),
    ('Fpnt', 'Fpnt'),
]


def account_login(request):
    user = request.user
    '''
    if user.is_authenticated:
        return HttpResponseRedirect('/')
    '''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        print user.username
        print user.is_active
        if user and user.is_active:
            auth.login(request, user)
            return JsonResponse({'code':0, 'reason':u'登录成功'})
        else:
            return JsonResponse({'code': -1, 'reason':u'登录失败'})
    else:
        return render(request, 'login.html', {"user": request.user})

@login_required
def bts_query(request):
    user = request.user
    bts_name = request.GET.get('bts_name', None)
    if not bts_name:
        bts = Bts.objects.first()
    else:
        bts = Bts.objects.filter(name=bts_name).first()
    data = {}
    if not bts:
        data['bsc_id'] = u'无'
        data['power'] = u'无'
        data['longitude'] = u'无'
        data['latitude'] = u'无'
        data['altitude'] = u'无'
        data['company'] = u'无'
        data['user'] = user
    else:
        data['bsc_id'] = bts.bsc_id
        data['power'] = bts.power
        data['longitude'] = bts.longitude
        data['latitude'] = bts.latitude
        data['altitude'] = bts.altitude
        data['company'] = bts.company
        data['user'] = user
    return render(request, 'bts.html', {'data': data})

@login_required
def cell_query(request):
    user = request.user
    cell_id = request.GET.get('cell_id', None)
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
    data['bcch'] = cell.bcch
    data['id'] = cell.id
    return render(request, 'cell.html', {'data': data})



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

@login_required
def get_neighbor(request):
    cell_id = request.GET.get('cell_id', None)
    if not cell_id:
        cell = Cell.objects.first()
    else:
        cell = Cell.objects.filter(id=cell_id).first()
    cells = Distr.get_neighbor(cell)
    return render(request, 'neighbor.html', {"cells": cells})


def excel_import(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel']
        upload_model = request.POST.get('upload_model')
        check_model = []
        for k, v in CHOICES:
            check_model.append(k)
        if not upload_model in check_model:
            return JsonResponse({'code': -1, 'reason': u'没有此数据类型'})
        print upload_model
        filename = excel_file.name
        if not os.path.exists('upload/'):
            os.mkdir('upload/')
        filename = 'upload/' + filename
        print filename
        with open(filename, 'wb+') as destination:
            for r in excel_file.chunks():
                destination.write(r)
        print "=======================success================="
        excel = xlrd.open_workbook(filename)
        sheet = excel.sheet_by_index(0)
        obj = UPLOADMODEL[upload_model]
        rows = sheet.nrows
        cols = sheet.ncols
        sql = "insert into " + upload_model + ' ('
        for i in range(0, cols):
            sql += str(sheet.cell(0, i).value)
            if i == int(cols) - 1:
                sql += ') values '
            else:
                sql += ', '
        execute_sql = sql
        res = 0
        cursor = connection.cursor()
        for i in range(1, rows):
            if res == 50:
                cursor.execute(execute_sql)
                transaction.commit()
                print execute_sql
                execute_sql = sql
                res = 0
            execute_sql += '('
            for j in range(0, cols):
                print type(sheet.cell(i, j).value)
                if isinstance(sheet.cell(i, j).value, unicode):
                    execute_sql += '\'' + sheet.cell(i, j).value + '\''
                else:
                    execute_sql += '\'' + str(sheet.cell(i, j).value) + '\''
                if j == cols - 1:
                    execute_sql += ')'
                else:
                    execute_sql += ', '
            res += 1
            if res == 50 or i == rows - 1:
                execute_sql += ';'
            else:
                execute_sql += ', '
        print execute_sql
        cursor.execute(execute_sql)
        transaction.commit()
        os.remove(filename)
        return JsonResponse({'code': 0, 'reason': u'导入数据成功'})

def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close

def excel_export(request):
    modelname = request.GET.get('downloadname')
    check_model = []
    for k, v in CHOICES:
        check_model.append(k)
    if not modelname in check_model:
        return JsonResponse({'code': -1, 'reason': u'没有此数据类型'})
    obj = UPLOADMODEL[modelname]
    return HttpResponse(readFile(filename))


@login_required
def profile(request):

    return render(request, 'excel.html', {'user': request.user, 'choices': CHOICES})

