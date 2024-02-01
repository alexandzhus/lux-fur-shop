from django.urls import path

from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('product/<slug:product_slug>/', DetailProduct.as_view(), name='product_detail'),
]