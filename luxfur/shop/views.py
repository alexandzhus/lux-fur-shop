from django.db.models import Q
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView


from .models import *
from cart.forms import CartAddProductForm


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
    model = Product
    context_object_name = 'products'
    template_name = 'shop/index.html'
    extra_context = {
        'title': "Главная страница сайта Lux-Fur",

    }

    def get_queryset(self):
        query = self.request.GET.get('search')
        print(query)
        if query:
            product_list = Product.objects.filter(Q(name__iregex=query) | Q(price__icontains=query))

            return product_list

        return Product.objects.all().select_related('category')





class DetailProduct(DetailView):
    """
    Клас для отображения детальной информации о товаре
    """
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'

    extra_context = {"title": "Детальная информация о товаре"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        product: Product = self.object
        product_image = ProductImage.objects.filter(product_id=product)
        context['product_image'] = product_image
        context['cart_product_form'] = cart_product_form

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])





class Category(ListView):
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'
    template_name = 'shop/category.html'
