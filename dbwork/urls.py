# -*- encoding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from databasework import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.profile, name="profile"),                                   #主页， 导入导出页面
    url(r'^bts/$', views.bts_query, name="bts_query"),
    url(r'^cell/$', views.cell_query, name="cell_query"),
    url(r'^traffic/measurement/$', views.measurement, name="measurement"),         #话务统计
    url(r'^traffic/$', views.traffic_query, name="traffic_query"),            #          话务查询
    url(r'^congestion/$', views.congestion_query, name="congestion_query"),          # 拥塞查询
    url(r'^account/login/$', views.account_login, name="account_login"),     #
    url(r'^excel/import/$', views.excel_import, name="excel_import"),       #
    url(r'^excel/export/$', views.excel_export, name="excel_export"),          #
    url(r'^neighbor/$', views.get_neighbor, name="get_neighbor"),
]
