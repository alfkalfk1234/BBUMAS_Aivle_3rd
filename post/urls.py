from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.index, name='post'),
    path('posting', views.posting, name='posting'),
    path('<int:pk>', views.post_detail, name='post_detail'),   
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('faq', views.faq, name='faq'),
]