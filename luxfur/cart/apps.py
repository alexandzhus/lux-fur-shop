from django.apps import AppConfig


class CartConfig(AppConfig):
    verbose_name = "Корзина"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
