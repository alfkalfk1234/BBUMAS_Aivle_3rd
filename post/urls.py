from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.index, name='post'),
    path('posting', views.posting, name='posting'),
    path('faq', views.faq, name='faq'),
]