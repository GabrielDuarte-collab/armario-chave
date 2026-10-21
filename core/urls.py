from django.urls import path
from . import views

urlpatterns = [
    path("status/", views.status_api, name="status_api"),
]    