from django.urls import path
from .views import upload_log

urlpatterns = [
    path('', upload_log, name='upload'),
]