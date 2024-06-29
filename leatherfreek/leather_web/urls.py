# leather_web/urls.py
from django.urls import path
from . import views  # Import your views
from . import ajax_view

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
    path('shopping_cart/', views.shopping_cart_view, name='shopping_cart'),
    #ajax
    path('add_to_cart_ajax/<int:product_id>/', ajax_view.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('increase_quantity_ajax/<int:product_id>/', ajax_view.increase_quantity_ajax, name='increase_quantity_ajax'),
    path('decrease_quantity_ajax/<int:product_id>/', ajax_view.decrease_quantity_ajax, name='decrease_quantity_ajax'),


    path('about-contact/', views.about_contact, name='about_contact'),
]
