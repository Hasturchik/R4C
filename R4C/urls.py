from django.contrib import admin
from django.urls import path

from robots.views import create_robot, get_excel_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create_robot/', create_robot, name='create_robot'),
    path('get_excel_report/', get_excel_report, name='get_excel_report'),
]
