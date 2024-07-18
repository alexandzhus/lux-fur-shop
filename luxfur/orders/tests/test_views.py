from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory, Client

from cart.cart import Cart
from orders.models import Order, OrderItems
from orders.views import OrderDetail, order_create
from shop.models import Material, Category, Product


class CreatingAllEntities(TestCase):
    """
    В классе создаются все нужные для тестов сущности
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

        cls.view = OrderDetail()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        cls.order.delete()
        cls.order_items.delete()
        cls.product.delete()
        cls.material.delete()
        cls.category.delete()


class OrderDetailViewTestCase(CreatingAllEntities):
    """
    Тест представления OrderDetail
    """

    def test_view_for_exists_location(self) -> None:
        """
        Тест представления OrderDetail на существующий url
        :return: None
        """
        response = self.client.get('/orders/order-detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_use_right_template(self) -> None:
        """
        Тест представления OrderDetail используется нужный шаблон
        :return: None
        """
        response = self.client.get('/orders/order-detail/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')

    def test_view_use_right_model(self) -> None:
        """
        Тест представления OrderDetail используется нужная модель
        :return: None
        """
        view_model = self.view.model
        self.assertEqual(view_model, Order)

    def test_view_get_right_context_data(self) -> None:
        """
        Тест представления OrderDetail получает правильный контекст
        :return: None
        """
        response = self.client.get('/orders/order-detail/1/')
        self.assertIn('order', response.context)
        self.assertIn('order_item', response.context)
        self.assertIn('total_cost', response.context)


class OrderCreateViewTestCase(TestCase):
    """
    Тест представления order_create
    """

    # def setUp(self):
    #     cart = Cart()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = get_user_model().objects.create(username='sashadzhus',
                                                        email='alexandrdzhus@gmail.com',
                                                        password='123',
                                                        )

        cls.material = Material.objects.create(name='Олово', slug='Olovo')
        cls.category = Category.objects.create(name='Ручка для зонтика',
                                               slug='ruchka-dly-zontika', )
        cls.product = Product.objects.create(name='Замок', slug='Zamok', price='1500',
                                             material=cls.material, category=cls.category)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        cls.product.delete()
        cls.material.delete()
        cls.category.delete()

    def test_view_for_exists_location(self) -> None:
        """
        Тест представления OrderDetail на существующий url
        :return: None
        """
        response = self.client.get('/orders/order-create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        """
        Тест view ShopHome, проверка на заданный в настройках url при помощи его имени
        :return: None
        """
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)

    def test_view_right_template(self) -> None:
        """
        Тест представления order_create на использование правильного шаблона
        :return: None
        """
        response = self.client.get(reverse('orders:order_create'))
        self.assertTemplateUsed(response, 'orders/order_form.html')

    def test_view_create_order(self) -> None:
        """
        Тест представления order_create на создание нового заказа
        :return: None
        """
        data1 = {
            '1': {'product_id': self.product.id,
                  'quantity': 2,
                  'price': Decimal(1500),
                  },

        }
        request = RequestFactory()
        request.session = {}
        request.session['cart'] = data1
        cart = Cart(request)

        self.client.force_login(self.test_user)

        data = {
            'first_name': 'sasha1',
            'last_name': 'dzhus1',
            'email': 'alex@mail.ru',
            'phone_number': +79787458576,
            'address': 'POR 89-73',
            'postal_code': 199038,
            'city': 'Sevastopol',

        }

        response = self.client.post(reverse('orders:order_create'), data=data)

        self.assertEqual(response.status_code, 200)

        # проверяем список заказов(создался ли заказ на залогининого пользователя)
        response = self.client.get(reverse('users:profile'))
        orders = Order.objects.all()
        orders_ = response.context['user_orders']
        for o, o_ in zip(orders, orders_):
            self.assertEquals(o.pk, o_.pk)

        # создание OrderItems

        for item in cart:
            OrderItems.objects.create(order=Order.objects.get(pk=1), product=item['product'],
                                      product_amount=item['quantity'],
                                      product_price=item['price'])

        # Проверяем создание списка продуктов в заказе(OrderItems)
        response_order_items = self.client.get('/orders/order-detail/1/')
        self.assertEqual(response_order_items.status_code, 200)
        order_items = OrderItems.objects.all()
        order_items_ = response_order_items.context['order_item']
        for i, i_ in zip(order_items, order_items_):
            self.assertEqual(i.id, i_.id)
