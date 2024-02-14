from django.db import models
from django.urls import reverse

from shop.models import Product
from users.models import User




class Order(models.Model):
    """
    Модель для хранения сведений о заказе
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', verbose_name='Пользователь')
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="E-mail")
    phone_number = models.CharField(max_length=20, null=True, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    postal_code = models.CharField(max_length=255, verbose_name="Почтовый индекс")
    city = models.CharField(max_length=255, verbose_name="Город")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления заказа")
    paid = models.BooleanField(default=False, verbose_name="Оплата")


    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-time_create']

    def __str__(self):
        return 'Order: {}; email: {}; create: {}'.format(self.id, self.email,
                                                         self.time_create.strftime("%Y-%m-%d %H:%M:%S"))

    def get_total_items(self):
        order_item: OrderItems
        return sum([order_item.product_amount for order_item in self.order_items.all()])

    def get_items(self):
        return self.order_items.all()

    def get_total_cost(self):
        items = self.get_items()
        return sum(item.get_cost() for item in items.all())

    def get_absolute_url(self):
        return reverse('orders:order_detail', args=[str(self.id)])




class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product', verbose_name="Товар")
    product_amount = models.PositiveIntegerField(default=1, verbose_name="Кол-во товара")
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")

    def __str__(self):
        return 'order: {}; product: {}; price: {}'.format(self.id, self.product.name,
                                                         self.product_price)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def get_cost(self):
        return self.product_price * self.product_amount


    def get_name(self):
        return self.product.name



