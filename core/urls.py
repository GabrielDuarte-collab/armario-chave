from django.urls import path
from core import views


urlpatterns = [
    path('', views.index, name='index'),
    path("status/", views.status_api, name="status_api"),
    path('api/status_nichos/', views.api_status_nichos, name= 'status_nichos'),
]
