from django.urls import path,include
from . import views
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name="cart"),
    path('add/', views.add_to_cart, name="add_to_cart"),
    path('remove/', views.remove_from_cart, name="rem_from_cart"),
    path('update/', views.update_cart, name="update_cart"),
    path('empty-cart/', views.empty_cart, name='empty_cart'),   
    path('checkout/', views.checkout_page, name='checkout'),

    # Paypal Urls for payments
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
]
