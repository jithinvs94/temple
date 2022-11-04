from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('booking/booking_summary', views.booking, name='booking_summary'),
    path('booking/print', views.print, name='print'),
    path('get_data/', views.get_data, name='get_data'),
    path('get_data/view', views.get_data, name='view'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]
