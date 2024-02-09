from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, TemplateView

from config.settings import DEFAULT_PRODUCT_IMAGE
from .cart import *
from .forms import CartAddProductForm
from shop.models import Product
# Create your views here.


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'
    extra_context = {
        'title': "Корзина",
        'default_image': DEFAULT_PRODUCT_IMAGE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context




# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/cart_detail.html', context={'cart': cart})