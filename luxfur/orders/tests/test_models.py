from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order, OrderItems
from shop.models import Material, Category, Product


class OrderModelTestCase(TestCase):
    """
    Тестируем модель Order
    """

    @classmethod
    def setUpClass(cls):
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )
        cls.order = Order.objects.create(user=cls.test_user, first_name='Sasha', last_name='dzhus',
                                         email='alexandrdzhus@gmail.com', phone_number='+79787458576',
                                         address='POR 89-62', postal_code='299038',
                                         city='Sevastopol', paid=False)

        cls.material = Material.objects.create(name='Олово', slug='Olovo')
        cls.category = Category.objects.create(name='Ручка для зонтика',
                                               slug='ruchka-dly-zontika', )
        cls.product = Product.objects.create(name='Замок', slug='Zamok', price='1500',
                                             material=cls.material, category=cls.category)

        cls.order_items = OrderItems.objects.create(order=cls.order, product=cls.product, product_amount=2,
                                                    product_price=1500)

        cls.user_field = cls.order._meta.get_field('user')
        cls.first_name_field = cls.order._meta.get_field('first_name')
        cls.last_name_field = cls.order._meta.get_field('last_name')
        cls.email_field = cls.order._meta.get_field('email')
        cls.address_field = cls.order._meta.get_field('address')
        cls.phone_number_field = cls.order._meta.get_field('phone_number')
        cls.postal_code_field = cls.order._meta.get_field('postal_code')
        cls.city_field = cls.order._meta.get_field('city')
        cls.time_create_field = cls.order._meta.get_field('time_create')
        cls.time_update_field = cls.order._meta.get_field('time_update')
        cls.paid_field = cls.order._meta.get_field('paid')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        cls.order.delete()
        cls.order_items.delete()
        cls.product.delete()
        cls.material.delete()
        cls.category.delete()

    def test_model_user_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля user на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.user_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Пользователь')

    def test_model_first_name_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля first_name на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.first_name_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Имя')

    def test_model_first_name_field_max_length(self) -> None:
        """
        Тестируем модель Order поля first_name на max_length
        :return: None
        """
        real_max_length = getattr(self.first_name_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_last_name_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля last_name на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.last_name_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Фамилия')

    def test_model_last_name_field_max_length(self) -> None:
        """
        Тестируем модель Order поля last_name на max_length
        :return: None
        """
        real_max_length = getattr(self.last_name_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_email_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля email на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.email_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'E-mail')

    def test_model_phone_number_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля phone_number на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.phone_number_field, 'verbose_name')
        self.assertEqual(real_verbose_name, "Номер телефона")

    def test_model_phone_number_field_max_length(self) -> None:
        """
        Тестируем модель Order поля phone_number на max_length
        :return: None
        """
        real_max_length = getattr(self.phone_number_field, 'max_length')
        self.assertEqual(real_max_length, 20)

    def test_model_phone_number_field_for_null(self) -> None:
        """
        Тестируем модель Order поля phone_number на null
        :return: None
        """
        self.assertTrue(getattr(self.phone_number_field, 'null'))

    def test_model_address_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля address на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.address_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Адрес')

    def test_model_address_field_max_length(self) -> None:
        """
        Тестируем модель Order address на max_length
        :return: None
        """
        real_max_length = getattr(self.address_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_postal_code_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля postal_code на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.postal_code_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Почтовый индекс')

    def test_model_postal_codes_field_max_length(self) -> None:
        """
        Тестируем модель Order postal_code на max_length
        :return: None
        """
        real_max_length = getattr(self.postal_code_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_city_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля city на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.city_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Город')

    def test_model_city_field_max_length(self) -> None:
        """
        Тестируем модель Order city на max_length
        :return: None
        """
        real_max_length = getattr(self.city_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_time_create_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля time_create на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.time_create_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Дата создания заказа')

    def test_model_time_create_field_max_length(self) -> None:
        """
        Тестируем модель Order time_create на на auto_now
        :return: None
        """
        self.assertTrue(getattr(self.time_create_field, 'auto_now_add'))

    def test_model_time_update_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля time_update на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.time_update_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Дата обновления заказа')

    def test_model_time_update_field_max_length(self) -> None:
        """
        Тестируем модель Order time_update на на auto_now
        :return: None
        """
        self.assertTrue(getattr(self.time_update_field, 'auto_now'))

    def test_model_paid_field_verbose_name(self) -> None:
        """
        Тестируем модель Order поля paid на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.paid_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Оплата')

    def test_model_paid_field_max_length(self) -> None:
        """
        Тестируем модель Order paid на на auto_now
        :return: None
        """
        self.assertFalse(getattr(self.paid_field, 'default'))

    def test_model_verbose_name(self) -> None:
        """
        Тест модели Order на verbose_name
        :return: None
        """
        order = OrderModelTestCase.order
        self.assertEqual(order._meta.verbose_name, 'Заказ')

    def test_model_verbose_name_plural(self) -> None:
        """
        Тест модели Order на verbose_name_plural
        :return: None
        """
        self.assertEqual(self.order._meta.verbose_name_plural, 'Заказы')

    def test_model_get_absolute_url(self) -> None:
        """
        Тест модели Order на получение url
        :return: None
        """
        self.assertEqual(OrderModelTestCase.order.get_absolute_url(), '/orders/order-detail/1/')

    def test_model_str(self) -> None:
        """
        Тест модели Order на строковое отображение
        :return: None
        """
        self.assertEqual(str(self.order), f'Order: {self.order.id}; email: {self.order.email}; '
                                          f'create: {self.order.time_create.strftime("%Y-%m-%d %H:%M:%S")}')

    def test_model_get_total_items(self) -> None:
        """
        Тест модели Order на получение кол-ва товаров в заказе
        :return: None
        """
        order_items = self.order.get_total_items()
        self.assertEqual(order_items, 2)

    def test_model_get_total_cost(self) -> None:
        """
        Тест модели Order на получение общей стоимости заказных товаров
        :return: None
        """
        order_total_cost = self.order.get_total_cost()

        self.assertEqual(order_total_cost, 3000)

    def test_model_get_item(self) -> None:
        """
        Тест модели Order на получение кол-во товаров из заказа
        :return: None
        """
        order_items = self.order.get_items()
        self.assertQuerysetEqual(order_items, OrderItems.objects.filter(pk=self.order_items.pk))


class OrderItemsModelTestCase(TestCase):
    """
    Тест модели OrderItems
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )
        cls.order = Order.objects.create(user=cls.test_user, first_name='Sasha', last_name='dzhus',
                                         email='alexandrdzhus@gmail.com', phone_number='+79787458576',
                                         address='POR 89-62', postal_code='299038',
                                         city='Sevastopol', paid=False)

        cls.material = Material.objects.create(name='Олово', slug='Olovo')
        cls.category = Category.objects.create(name='Ручка для зонтика',
                                               slug='ruchka-dly-zontika', )
        cls.product = Product.objects.create(name='Замок', slug='Zamok', price='1500',
                                             material=cls.material, category=cls.category)

        cls.order_items = OrderItems.objects.create(order=cls.order, product=cls.product, product_amount=2,
                                                    product_price=1500)

        cls.order_field = cls.order_items._meta.get_field('order')
        cls.product_field = cls.order_items._meta.get_field('product')
        cls.product_amount_field = cls.order_items._meta.get_field('product_amount')
        cls.product_price_field = cls.order_items._meta.get_field('product_price')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        cls.order.delete()
        cls.order_items.delete()
        cls.product.delete()
        cls.material.delete()
        cls.category.delete()

    def test_model_order_field_verbose_name(self) -> None:
        """
        Тест модели OrderItems поля order на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.order_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Заказ')

    def test_model_product_field_verbose_name(self) -> None:
        """
        Тест модели OrderItems поля product на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.product_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Товар')

    def test_model_product_amount_field_verbose_name(self) -> None:
        """
        Тест модели OrderItems поля product_amount на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.product_amount_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Кол-во товара')

    def test_model_product_amount_field_default(self) -> None:
        """
        Тест модели OrderItems поля product_amount на default
        :return: None
        """
        real_default = getattr(self.product_amount_field, 'default')
        self.assertEqual(real_default, 1)

    def test_model_product_price_field_verbose_name(self) -> None:
        """
        Тест модели OrderItems поля product_amount на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.product_price_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Цена товара')

    def test_model_product_price_field_max_digits(self) -> None:
        """
        Тест модели OrderItems поля product_amount на max_digits
        :return: None
        """
        real_max_digits = getattr(self.product_price_field, 'max_digits')
        self.assertEqual(real_max_digits, 10)

    def test_model_product_price_field_decimal_places(self) -> None:
        """
        Тест модели OrderItems поля product_amount на decimal_places
        :return: None
        """
        real_decimal_places = getattr(self.product_price_field, 'decimal_places')
        self.assertEqual(real_decimal_places, 2)

    def test_model_verbose_name(self) -> None:
        """
        Тест модели OrderItems на verbose_name
        :return: None
        """
        order_items = OrderItemsModelTestCase.order_items
        self.assertEqual(order_items._meta.verbose_name, 'Товар в заказе')

    def test_model_verbose_name_plural(self) -> None:
        """
        Тест модели OrderItems на verbose_name_plural
        :return: None
        """
        order_items = OrderItemsModelTestCase.order_items
        self.assertEqual(order_items._meta.verbose_name_plural, 'Товары в заказе')

    def test_model_str(self) -> None:
        """
        Тест модели OrderItems на строковое отображение
        :return: None
        """
        self.assertEqual(str(self.order_items), f'order: {self.order.id}; '
                                                f'product: {self.product.name}; '
                                                f'price: {self.product.price}')

    def test_model_get_cost(self) -> None:
        """
        Тест модели OrderItems на получение стоимости товара в заказе
        :return: None
        """
        self.assertEqual(self.order_items.get_cost(), 3000)
