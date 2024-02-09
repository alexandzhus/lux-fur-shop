from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('cart-add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart-remove/<int:product_id>/', cart_remove, name='cart_remove'),
]