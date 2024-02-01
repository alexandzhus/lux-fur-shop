from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import *


# def index(request: HttpRequest) -> HttpResponse:
#
#     products = Product.objects.all()
#
#     data = {
#         'products': products,
#         'title': "Главная страница сайта Lux-Fur"
#     }
#
#     return render(request,'shop/index.html', context=data)


# def product(request: HttpRequest, product_slug) -> HttpResponse:
#
#     product = get_object_or_404(Product, slug=product_slug)
#
#     data = {
#         "product": product,
#         "title": "Детальная информация о продукте"
#     }
#
#     return render(request, 'shop/product_detail.html', context=data)


class ShopHome(ListView):
    """
    Класс для отображения главной страницы сайта со списком товаров
    """
    context_object_name = 'products'
    template_name = 'shop/index.html'
    extra_context = {
        'title': "Главная страница сайта Lux-Fur"
    }

    def get_queryset(self):
        return Product.objects.all().select_related('category')


class DetailProduct(DetailView):
    """
    Клас для отображения детальной информации о товаре
    """
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'
    extra_context = {"title": "Детальная информация о товаре"}

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])
