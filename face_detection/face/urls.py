from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('webcam', views.hm),path('',views.face,name='webcam')
]