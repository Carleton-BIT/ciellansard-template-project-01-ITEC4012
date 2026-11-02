from django.urls import path

from . import views
import requests
from django.conf.urls.static import static
import project_1.settings as settings

urlpatterns = [
    #path("", views.file_submission, name="file_submission"),
    path("", views.index, name="index"),
]

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)