from django.urls import path

from .views import *

app_name = 'orders'

urlpatterns = [
    path('order-create/', order_create, name='order_create'),
    path('order-detail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
]