from django.urls import path
from .views import signup_view

app_name = 'join'
urlpatterns = [
    path('', signup_view, name='join'),
]
