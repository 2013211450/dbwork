# -*- encoding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from databasework import views
from django.views.static import serve
from dbwork import settings
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
    url(r'^neighbor/$', views.query_neighbor, name="get_neighbor"),
    url(r'^neighbor/calculator/$', views.calc_neighbor, name="get_neighbor"),
    url(r'^excel/download/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'E:\\project\\dbwork\\databasework\\static\\', 'show_indexes': True}),
]
