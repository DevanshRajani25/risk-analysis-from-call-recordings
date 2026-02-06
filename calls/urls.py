from django.urls import path
from .views import upload_audio, analyze_call

urlpatterns = [
    path("", upload_audio),
    path("analyze/", analyze_call),
]
