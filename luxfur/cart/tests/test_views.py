from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from cart.views import Cart, CartDetailView, cart_remove, cart_add
from config.settings import DEFAULT_PRODUCT_IMAGE
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

        cls.material = Material.objects.create(name='Олово', slug='Olovo')
        cls.category = Category.objects.create(name='Ручка для зонтика',
                                               slug='ruchka-dly-zontika', )
        cls.product1 = Product.objects.create(name='Замок', slug='Zamok', quantity=6, price='1500',
                                              material=cls.material, category=cls.category)
        cls.product2 = Product.objects.create(name='Замочек на тумбу', slug='Zamochek-na-tumbu', quantity=6,
                                              price='750',
                                              material=cls.material, category=cls.category)

        cls.request = RequestFactory()
        cls.request.session = {}

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_user.delete()
        cls.product1.delete()
        cls.product2.delete()
        cls.material.delete()
        cls.category.delete()


class CartDetailViewTestCase(CreatingAllEntities):
    """
    Тест представления CartDetailView
    """

    def setUp(self):
        self.client.force_login(self.test_user)
        self.product_in_cart = {
            '1': {
                'product': self.product1.name,
                'price': self.product1.price,
                'quantity': 2,

            },
            '2': {
                'product': self.product2.name,
                'price': self.product2.price,
                'quantity': 2,
            }
        }
        self.view = CartDetailView()

    def tearDown(self):
        self.product_in_cart.clear()

    def test_view_path_exists(self) -> None:
        """
        Тест представления CartDetailView на существование пути url
        :return: None
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_path_exists_by_name(self) -> None:
        """
        Тест представления CartDetailView на существование пути url по имени
        :return: None
        """
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_view_use_right_template(self) -> None:
        """
        Тест представления CartDetailView на использование правильного шаблона
        :return: None
        """
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')

    def test_view_get_right_extra_content(self) -> None:
        """
        Тест представления CartDetailView на получение правильного extra_content
        :return: None
        """
        view_extra_context = self.view.extra_context
        self.assertEqual(view_extra_context, {
            'title': "Корзина",
            'default_image': DEFAULT_PRODUCT_IMAGE,
        })

    def test_view_get_right_context_data(self) -> None:
        """
        Тест представления CartDetailView на  получение правильной context_data
        :return: None
        """
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertIn('cart', response.context)


class CartRemoveViewTestCase(CreatingAllEntities):
    """
    Тест представления cart_remove
    """

    def setUp(self):
        self.client.force_login(self.test_user)
        self.product_in_cart = {
            '1': {
                'product': self.product1.name,
                'price': self.product1.price,
                'quantity': 2,

            },
            '2': {
                'product': self.product2.name,
                'price': self.product2.price,
                'quantity': 2,
            }
        }

    def test_view_path_url_exists(self) -> None:
        """
        Тест представления cart_remove на существующий путь url
        :return: None
        """
        response = self.client.get(f'/cart/cart-remove/{self.product1.id}/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_path_url_exists_for_name(self) -> None:
        """
        Тест представления cart_remove на существующий путь url по имени
        :return: None
        """
        response = self.client.get(reverse('cart:cart_remove', args=[self.product1.id]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_is_happening(self) -> None:
        """
        Тест представления cart_remove на перенаправление
        :return: None
        """
        response = self.client.post(f'/cart/cart-remove/{self.product1.id}/')
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_view_remove_from_cart(self) -> None:
        """
        Тест представления cart_remove на удаление товара из корзины
        :return: None
        """
        self.request.session['cart'] = self.product_in_cart
        cart = Cart(self.request)
        response = self.client.post(reverse('cart:cart_remove', args=[self.product1.id]))

        self.assertEqual(response.status_code, 302)
        cart_remove(self.request, self.product1.id)
        self.assertEqual(cart.cart, {'2': {'price': '750', 'product': 'Замочек на тумбу', 'quantity': 2}})


class CartAddViewTestCase(CreatingAllEntities):
    """
    Тест представления cart_add
    """

    def setUp(self):
        self.client.force_login(self.test_user)

    def test_view_path_url_exists(self) -> None:
        """
        Тест представления cart_add на существующий путь url
        :return: None
        """
        response = self.client.get(f'/cart/cart-add/{self.product1.id}/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_path_url_exists_fir_name(self) -> None:
        """
        Тест представления cart_add на существующий путь url по имени
        :return: None
        """
        response = self.client.get(reverse('cart:cart_add', args=[self.product1.id]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_redirect_is_happening(self) -> None:
        """
        Тест представления cart_remove на перенаправление
        :return: None
        """
        response = self.client.post(f'/cart/cart-add/{self.product1.id}/')
        self.assertRedirects(response, reverse('cart:cart_detail'))



