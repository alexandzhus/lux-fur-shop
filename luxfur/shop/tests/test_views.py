from django.test import TestCase, RequestFactory

from shop.views import *

from django.urls import reverse

from shop.models import Product, Material, Category


class ShopHomeListViewTestCase(TestCase):
    """
    Тестируем view ShopHome
    """
    fixtures = ['subjects.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = ShopHome()
        cls.test_material = Material.objects.create(name='Цинк', slug='Zink')
        cls.test_category = Category.objects.create(name='Ролик для мебели', slug='Rolik dly mebely')
        cls.test_product = Product.objects.create(name='Ролик', slug='Rolik', price=1550, material=cls.test_material,
                                                  category=cls.test_category)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_product.delete()
        cls.test_category.delete()
        cls.test_material.delete()

    def test_url_exists_in_indicate_location(self) -> None:
        """
        Тест view ShopHome, проверка на заданный url адрес(существует ли такой путь)
        :return: None
        """

        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        """
        Тест view ShopHome, проверка на заданный в настройках url при помощи его имени
        :return: None
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_use_right_template(self) -> None:
        """
        Тестируем view ShopHome, проверяем, что вьюшка использует правильный шаблон
        :return: None
        """

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_view_get_right_context(self) -> None:
        """
        Тестируем view ShopHome, проверяем, что представление получает правильный контекст
        :return: None
        """
        context_object_name = self.view.context_object_name
        context_extra_context = self.view.extra_context
        self.assertEqual(context_object_name, 'products')
        self.assertEqual(context_extra_context, {'title': "Главная страница сайта Lux-Fur"})

    def test_view_get_right_queryset(self) -> None:
        """
        Тестируем view ShopHome, проверка на получение списка объектов модели Product
        :return: None
        """
        request = RequestFactory().get('')
        test_view = ShopHome()
        test_view.request = request
        queryset = test_view.get_queryset()
        self.assertQuerysetEqual(queryset, Product.objects.all())

    def test_product_list_exists(self) -> None:
        """
        Тестируем представление ShopHome, проверяем список продуктов
        :return: None
        """
        response = self.client.get(reverse('home'))
        products = Product.objects.all()
        products_ = response.context['products']
        for p, p_ in zip(products, products_):
            self.assertEquals(p.pk, p_.pk)


class DetailProductViewTestCase(TestCase):
    """
    Тестируем представление DetailProduct
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = DetailProduct()
        cls.test_material = Material.objects.create(name='Цинк', slug='Zink')
        cls.test_category = Category.objects.create(name='Ролик для мебели', slug='Rolik dly mebely')
        cls.test_product = Product.objects.create(name='Ролик', slug='Rolik', price=1550, material=cls.test_material,
                                                  category=cls.test_category)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.test_product.delete()
        cls.test_category.delete()
        cls.test_material.delete()

    def test_url_exists(self) -> None:
        """
        Тестируем view DetailProduct на существующий путь url(без доменного имени)
        :return: None
        """
        response = self.client.get('/product/Rolik/')
        self.assertEqual(response.status_code, 200)

    def test_view_use_right_template(self) -> None:
        """
        Тестируем view DetailProduct, проверяем, что вьюшка использует правильный шаблон
        :return: None
        """

        response = self.client.get('/product/Rolik/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')

    def test_view_get_right_context(self) -> None:
        """
        Тестируем view DetailProduct, проверяем, что представление получает правильный контекст
        :return: None
        """

        context_object_name = self.view.context_object_name
        context_extra_context = self.view.extra_context
        self.assertEqual(context_object_name, 'product')
        self.assertEqual(context_extra_context, {"title": "Детальная информация о товаре"})

    def test_view_get_context_data(self) -> None:
        """
        Тест представления DetailProduct на получение правильного context_data
        :return: None
        """
        response = self.client.get('/product/Rolik/')
        self.assertIn('product_image', response.context)
        self.assertIn('cart_product_form', response.context)
