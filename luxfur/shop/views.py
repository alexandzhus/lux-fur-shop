from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import *

def index(request: HttpRequest) -> HttpResponse:

    products = Product.objects.all()

    data = {
        'products': products,
        'title': "Главная страница сайта Lux-Fur"
    }

    return render(request,'shop/index.html', context=data)
