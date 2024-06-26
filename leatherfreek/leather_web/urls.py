# leather_web/urls.py
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.home, name='home'),
    path('index_trial/', views.index_trial, name='index_trial'),  
    path('product_card/<int:product_id>/', views.product_card, name='product_card'),
    path('view_products/<int:catagory_id>/', views.view_products, name='view_products'),
]
