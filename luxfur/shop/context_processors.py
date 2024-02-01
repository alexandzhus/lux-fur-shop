menu = [
    {"title": "О нас", 'url_name': "about"},
    {"title": "Обратная связь", 'url_name': "contact"},
    ]


def get_shop_context(request):
    return {'mainmenu': menu}