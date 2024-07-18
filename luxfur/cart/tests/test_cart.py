from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from cart.cart import Cart
from shop.models import Product, Material, Category


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

        cls.material = Material.objects.create(name='Олово', slug='Olovo')
        cls.category = Category.objects.create(name='Ручка для зонтика',
                                               slug='ruchka-dly-zontika', )
        cls.product1 = Product.objects.create(name='Замок', slug='Zamok', quantity=6, price='1500',
                                              material=cls.material, category=cls.category)
        cls.product2 = Product.objects.create(name='Замочек на тумбу', slug='Zamochek-na-tumbu', quantity=6,
                                              price='750',
                                              material=cls.material, category=cls.category)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        cls.product1.delete()
        cls.product2.delete()
        cls.material.delete()
        cls.category.delete()


class CartInitializeTestCase(CreatingAllEntities):
    """
    Тест на инициализацию корзины
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = RequestFactory()
        cls.request.session = {}

    def setUp(self):
        self.product = {
            '1': {
                'product': self.product1.name,
                'price': self.product1.price,
            },
            '2': {
                'product': self.product2.name,
                'price': self.product2.price,
            }
        }

    def test_initialize_cart_clean_sessions(self) -> None:
        """
        Тест корзины, проверяем есть ли в сессии корзина, если нет, то должна создается корзина с пустым словарем
        :return: None
        """
        cart = Cart(self.request)
        self.assertEqual(cart.cart, {})

    def test_initialize_cart_sessions_not_clean(self) -> None:
        """
        Тест корзины, проверяем есть ли в сессии корзина, если есть сравниваем товары в ней
        :return: None
        """

        self.request.session['cart'] = self.product
        cart = Cart(self.request)
        self.assertEqual(cart.cart, self.product)


class CartAddTestCase(CreatingAllEntities):
    """
    Тестируем добавление товаров в корзину
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = RequestFactory()
        cls.request.session = {}

        cls.product_in_cart = {
            '1': {
                'product_id': cls.product1.id,
                'price': Decimal(cls.product1.price),
                'quantity': 2,

            },
            '2': {
                'product_id': cls.product2.id,
                'price': Decimal(cls.product2.price),
                'quantity': 2,
            }
        }

    def test_add_to_cart(self) -> None:
        """
        Тест корзины, обновление товаров в корзине
        :return: None
        """
        cart_after_add_product = {'1': {
            'product_id': self.product1.id,
            'price': Decimal(self.product1.price),
            'quantity': 4,

        },
            '2': {
                'product_id': self.product2.id,
                'price': Decimal(self.product2.price),
                'quantity': 2,
            }
        }

        self.request.session['cart'] = self.product_in_cart
        cart = Cart(self.request)
        self.assertEqual(cart.cart, self.product_in_cart)
        cart.add(self.product1, quantity=2, update_quantity=False)
        self.assertEqual(cart.cart, cart_after_add_product)


class CartClearTestCase(CreatingAllEntities):
    """
    Тест корзины метода clear
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = RequestFactory()
        cls.request.session = {}

        cls.product_in_cart = {
            '1': {
                'product_id': cls.product1.id,
                'price': cls.product1.price,
                'quantity': 5,
            }
        }

    def test_cart_clear_on_session(self) -> None:
        """
        Тест удаление корзины из сессии
        :return: None
        """

        self.request.session['cart'] = self.product_in_cart
        cart = Cart(self.request)
        self.assertEqual(cart.cart, self.product_in_cart)
        cart.clear()
        cart = Cart(self.request)
        self.assertEqual(cart.cart, {})


class CartLenTestCase(CreatingAllEntities):
    """
    Тест корзины метода __len__
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = RequestFactory()
        cls.request.session = {}

        cls.product_in_cart = {
            '1': {
                'product_id': cls.product1.id,
                'price': cls.product1.price,
                'quantity': 5,
            }
        }

    def test_len_product_in_cart(self) -> None:
        """
        Тест корзины на общее ко-во товаров в ней
        :return: None
        """

        self.request.session['cart'] = self.product_in_cart
        cart = Cart(self.request)
        self.assertEqual(cart.cart, self.product_in_cart)
        self.assertEqual(cart.__len__(), 5)


class CartGetTotalPriceTestCase(CreatingAllEntities):
    """
    Тест корзины метода get_total_price
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = RequestFactory()
        cls.request.session = {}

        cls.product_in_cart = {
            '1': {
                'product_id': cls.product1.id,
                'price': Decimal(cls.product1.price),
                'quantity': 5,
            }
        }

    def test_get_total_price_products_in_cart(self) -> None:
        """
        Тест корзины получение общей стоимости товаров
        :return: None
        """

        self.request.session['cart'] = self.product_in_cart
        cart = Cart(self.request)
        self.assertEqual(cart.cart, self.product_in_cart)

        self.assertEqual(cart.get_total_price(), 7500)


class CartRemoveTestCase(CreatingAllEntities):
    """
    Тест корзины метода remove
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request = RequestFactory()
        cls.request.session = {}

        cls.product_in_cart = {
            '1': {
                'product_id': cls.product1.id,
                'price': Decimal(cls.product1.price),
                'quantity': 5,
            },
            '2': {
                'product_id': cls.product2.id,
                'price': Decimal(cls.product2.price),
                'quantity': 3,
            }

        }

    def test_delete_product_from_cart(self) -> None:
        """
        Тест корзины удаление товара из корзины
        :return: None
        """

        self.request.session['cart'] = self.product_in_cart
        cart = Cart(self.request)
        self.assertEqual(cart.cart, self.product_in_cart)
        cart.remove(self.product2)
        self.assertEqual(cart.cart, {'1': {'price': Decimal('1500'), 'product_id': 1, 'quantity': 5}}
                         )
