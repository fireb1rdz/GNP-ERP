from urllib.parse import urlparse
from django.urls import path, include
from .views import index

urlpatterns = [
    path('', index, name='index'),
]