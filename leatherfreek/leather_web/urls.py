# leather_web/urls.py
from django.urls import path
from . import views  # Import your views

urlpatterns = [

    #AUTH & USER
    path('accounts/profile/' , views.user_profile , name = 'user_profile'),
    path('accounts/signup/', views.user_signup, name='user_signup'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/logout/', views.user_logout, name='user_logout'),







    path('', views.home, name='home'),
    path('index_trial/', views.index_trial, name='index_trial'),  
    path('product_card/<int:product_id>/', views.product_card, name='product_card'),
    path('view_products/<int:catagory_id>/', views.view_products, name='view_products'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
]
