from .cart import Cart


def cart_context_processor(request):
    return {'cart': Cart(request)}