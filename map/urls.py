from django.urls import path
from . import views

app_name = 'map'
urlpatterns = [
    path('', views.map_view, name='map'),
    path('get-locations/', views.get_locations, name='get-locations'),
]