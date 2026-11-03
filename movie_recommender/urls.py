from django.urls import path

from . import views
import requests

urlpatterns = [
    path("", views.file_submission, name="index"),
    #path("", views.index, name="index"),
]