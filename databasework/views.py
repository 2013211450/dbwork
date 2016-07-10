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
from const import UPLOADMODEL, CHOICES, FOREIGNKEY_FIELDS
# Create your views here.

def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close

def turn_datetime_to_int(attr_str):
    if attr_str[0] != '0':
        return int(attr_str)
    else:
        while attr_str[0] == '0' and len(attr_str) > 1:
            attr_str = attr_str[1:]
        if attr_str[0] == '0':
            return 0
        else:
            return int(attr_str)

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
    cell_id = int(cell_id)
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
def traffic_query(request):
    if request.method == 'POST':
        mode = int(request.POST.get('mode', 0))
        cell_id = request.POST.get('cell_id', None)
        query_date = request.POST.get('date', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        query_date = turn_datetime_to_int(str(query_date))
        start_time = turn_datetime_to_int(str(start_time))
        end_time = turn_datetime_to_int(str(end_time))
        cell_id = int(cell_id)
        print type(cell_id), cell_id
        print query_date
        print start_time
        print end_time
        if cell_id == None or start_time == None or end_time == None:
            return JsonResponse({'code':-1, 'reason':u'缺少必要的参数'})
        cursor = connection.cursor()
        if mode == 0:
            proc_command = 'HOURLY_TRAFF'
            query_command = 'select QTIME, QTRAFFAVG, QTRAFFLINE, QCONGRATE from HOURLY'
        else:
            if mode == 1:
                proc_command = 'Minute_TRAFF15'
            else:
                proc_command = 'Minute_TRAFF'
            query_command = 'select QTIME, QTRAFFAVG, QTRAFFLINE from Minute'
        cursor.callproc(proc_command, (cell_id, query_date, start_time, end_time))
        transaction.commit()
        cursor.execute(query_command)
        data_list = {}
        data = []
        data.append([])
        data.append([])
        data.append([])
        data.append([])
        resp = cursor.fetchall()
        for r in resp:
            for i in range(0, len(r)):
                data[i].append(r[i])
        data_list['code'] = 0
        data_list['time'] = data[0]
        data_list['mode'] = mode
        data_list['traffavg'] = data[1]
        data_list['traffline'] = data[2]
        if mode == 0:
            data_list['congrate'] = data[3]
        return JsonResponse(data_list)
    else:
        return render(request, 'traffic2.html', {'user': request.user})



@login_required
def congestion_query(request):
    congestion_rate = request.GET.get('rate', None)
    query_date = request.GET.get('date', None)
    start_time = request.GET.get('start_time', None)
    end_time = request.GET.get('end_time', None)
    if congestion_rate and start_time and end_time and query_date:
        congestion_rate = float(congestion_rate)
        query_date = turn_datetime_to_int(str(query_date))
        start_time = turn_datetime_to_int(str(start_time))
        end_time = turn_datetime_to_int(str(end_time))
        print congestion_rate
        print query_date
        print start_time
        print  end_time
        if start_time < end_time:
            cursor = connection.cursor()
            cursor.callproc('CONGS_RATE', (congestion_rate, query_date, start_time, end_time))
            transaction.commit()
            cursor.execute('select QCELLID, QTIME, QTRAFFAVG, QCONGRATE, QTHRATE from CONGS')
            data = cursor.fetchall()
            data_list = []
            for r in data:
                data_list.append({
                    'cell_id': r[0],
                    'time': r[1],
                    'traffavg': r[2],
                    'congrate': r[3],
                    'thrate': r[4],
                })
            return render(request, 'congestion.html', {'user': request.user, 'data': data_list, 'limit_rate': congestion_rate})
    return render(request, 'congestion.html', {'user': request.user})


@login_required
def measurement(request):
    if request.method == 'POST':
        cell_id = request.POST.get('cell_id', None)
        query_date = request.POST.get('date', None)
        start_time = request.POST.get('start_time', None)
        end_time = request.POST.get('end_time', None)
        if cell_id == None or start_time == None or end_time == None or query_date == None:
            return JsonResponse({'code':-1, 'reason':u'缺少必要的参数'})
        query_date = turn_datetime_to_int(str(query_date))
        start_time = turn_datetime_to_int(str(start_time))
        end_time = turn_datetime_to_int(str(end_time))
        cell_id = int(cell_id)
        print type(query_date), query_date
        print type(start_time), start_time
        print type(end_time), end_time
        if start_time > end_time:
            return JsonResponse({'code':-1, 'reason': u'起始时间不能大于结束时间'})
        cursor = connection.cursor()
        cursor.callproc('C_PHONE')
        transaction.commit()
        phones = Phone.objects.filter(date=query_date, time__gte=start_time, time_lte=end_time).all()
        time_data = []
        traff_data = []
        rate_data = []
        for r in phones:
            data.append({
                'time': r.time,
                'traff': r.traff,
                'rate': r.rate,
            })
        return JsonResponse({'code':0, 'data': data})
    else:
        return render(request, 'measurement.html', {'user': request.user})

@login_required
def query_neighbor(request):
    cell_id = request.GET.get('cell_id', None)
    cell_id = int(cell_id)
    if not cell_id:
        cell = Cell.objects.first()
    else:
        cell = Cell.objects.filter(id=cell_id).first()
    cells = Distr.get_neighbor(cell)
    print len(cells)
    return render(request, 'neighbor.html', {"cells": cells, 'user': request.user})

@login_required
def calc_neighbor(request):
    cells = Cell.objects.order_by('id').all()
    for cell in cells:
        Distr.calc_neighbor(cell)
    return JsonResponse({'code': 0})

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
        sql = "replace into " + upload_model + ' ('
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


@login_required
def excel_export(request):
    modelname = request.GET.get('downloadname')
    check_model = []
    if not UPLOADMODEL.has_key(modelname):
        return JsonResponse({'code': -1, 'reason': u'没有此数据类型'})
    obj = UPLOADMODEL[modelname]
    excel = xlwt.Workbook()
    sheet = excel.add_sheet(modelname)
    data = obj.objects.all()
    fieldnames = obj._meta.get_all_field_names()
    count = obj.objects.count()
    print fieldnames
    for i in range(0, len(fieldnames)):
        sheet.write(0, i, fieldnames[i])
    for i in range(0, count):
        for j in range(0, len(fieldnames)):
            value = getattr(data[i], fieldnames[j], None)
            print type(value), fieldnames[j]
            if fieldnames[j] in FOREIGNKEY_FIELDS:
                value = value.pk
            sheet.write(i + 1, j, value)
    excel.save('databasework/static/temp.xls')
    return HttpResponseRedirect('/excel/download/temp.xls')


@login_required
def profile(request):
    return render(request, 'excel.html', {'user': request.user, 'choices': CHOICES})

