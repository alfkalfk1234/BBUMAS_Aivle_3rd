from django.urls import path
from . import views

app_name = 'join'
urlpatterns = [
    path('', views.index, name='join'),
]