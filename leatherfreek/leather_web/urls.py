# leather_web/urls.py
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.home, name='home'),  
]
