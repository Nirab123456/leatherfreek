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
    path('update_profile/', views.update_profile, name='update_profile'),







    path('', views.home, name='home'),
    path('product_card/<int:product_id>/', views.product_card, name='product_card'),
    path('shopping_cart/', views.shopping_cart_view, name='shopping_cart'),
    path('wallet/', views.wallet, name='wallet'),








    #ajax
    path('add_to_cart_ajax/<int:product_id>/', ajax_view.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('increase_quantity_ajax/<int:product_id>/', ajax_view.increase_quantity_ajax, name='increase_quantity_ajax'),
    path('decrease_quantity_ajax/<int:product_id>/', ajax_view.decrease_quantity_ajax, name='decrease_quantity_ajax'),
    path('remove_from_cart_ajax/<int:product_id>/', ajax_view.remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('apply_coupon_code_ajax/', ajax_view.apply_coupon_code_ajax, name='apply_coupon_code_ajax'),
    path('checkout_cart_ajax/', ajax_view.checkout_cart_ajax, name='checkout_cart_ajax'),



    path('about-contact/', views.about_contact, name='about_contact'),
]
