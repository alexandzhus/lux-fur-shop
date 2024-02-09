from decimal import Decimal
from config import settings
from shop.models import Product


class Cart(object):
    """
    Класс позволяет управлять корзиной покупок
    """

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session  # Инициализируем сессию с помощью объекта request
        # также с помощью объекта request мы храним текущую сессию корзины для других методов класса
        cart = self.session.get(settings.CART_SESSION_ID)  # пытаемся получить корзину из текущей сессии
        if not cart:
            cart = self.session[
                settings.CART_SESSION_ID] = {}  # если корзина в сессии отсутствует мы создаем пустую корзину установив в ней пустой словарь
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавляем продукт в корзину или обновляем его количество
        :param product:
        :param quantity:
        :param update_quantity:
        :return:
        """
        product_id = str(product.id)  # присваиваем переменной id продукта в строковом формате(джанго для сериализации
        # использует JSON). Здесь id продукта используется в качестве ключа в словаре содержимого продукта

        if product_id not in self.cart:
            # если продукта нет в корзине, то добавляем кол-во и цену
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Сохраняет все изменения в корзине
        :return:
        """
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаляет продукт и вызывает метод save() для обновления корзины в сессии
        :return:
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """

        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет товаров в корзине
        :return:
        """

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчитывает стоимость всех товаров в корзине
        :return:
        """
        return Decimal(sum(item['price'] * item['quantity'] for item in self.cart.values()))

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
