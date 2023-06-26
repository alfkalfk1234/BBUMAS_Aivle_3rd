from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('policy', views.policy, name='policy'),
]