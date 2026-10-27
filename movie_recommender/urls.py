from django.urls import path

from . import views
import requests

urlpatterns = [
    path("", views.index, name="index"),
]