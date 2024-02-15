from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import OrderCreateForm
from .models import *
from cart.cart import Cart

# class OrderCreate(CreateView):
#     form_class = OrderCreateForm
#     template_name = 'orders/order_form.html'
#     success_url = reverse_lazy('orders/order_create_done')
#     extra_context = {
#         "title": 'Оформление заказа'
#     }
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart = Cart(self.request)
#         context['cart'] = cart
#
#         return context


class OrderDetail(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order: Order = self.object
        order_item = OrderItems.objects.filter(order_id=order)
        total_cost = order.get_total_cost()
        context['order'] = order
        context['order_item'] = order_item
        context['total_cost'] = total_cost

        return context



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItems.objects.create(order=order, product=item['product'],
                                          product_amount=item['quantity'],
                                          product_price=item['price'])

                cart.clear()
                data = {
                    'order': order,
                }
                return render(request, 'orders/order_create_done.html', context=data)

    else:
        form = OrderCreateForm()
    data = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/order_form.html', context=data)

