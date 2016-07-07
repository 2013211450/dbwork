"""dbwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from databasework import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bts/$', views.bts_query, name="bts_query"),
    url(r'^cell/$', views.cell_query, name="cell_query"),
    url(r'^traffic/measurement/$', views.measurement, name="measurement"),
    url(r'^traffic/$', views.traffic_query, name="traffic_query"),
    url(r'^congestion/$', views.congestion_query, name="congestion_query"),
    url(r'^account/login/$', views.account_login, {'template_name':'login.html'}),
    url(r'^excel/import/$', views.excel_import, name="excel_import"),
    url(r'^excel/export/$', views.excel_export, name="excel_export")
]
