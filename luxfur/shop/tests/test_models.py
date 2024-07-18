from django.test import TestCase
from shop.models import Product, Category, Material, ProductImage


class CategoryModelTest(TestCase):
    """
    Тесты модели Category
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(name='Ручка для двери',
                                               slug='ruchka-dly-dvery', )

    @classmethod
    def tearDownClass(cls):
        cls.category.delete()

    def test_model_name_verbose_name(self) -> None:
        """
        Проверяем совпадает ли verbose_name поля name с ожидаемым
        :return: None
        """
        category = CategoryModelTest.category
        verbose = category._meta.get_field('name').verbose_name
        self.assertEqual(verbose, 'Категория')

    def test_model_name_max_length(self) -> None:
        """
        Проверяем совпадает ли максимальная длина с допустимой
        :return: None
        """
        category = CategoryModelTest.category
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_model_slug_verbose_name(self) -> None:
        """
        Проверяем совпадает ли verbose_name поля slug с ожидаемым
        :return: None
        """
        category = CategoryModelTest.category
        slug_verbose_name = category._meta.get_field("slug").verbose_name
        self.assertEqual(slug_verbose_name, 'Slug')

    def test_model_slug_max_length(self) -> None:
        """
        Проверяем совпадает ли max_length поля slug с ожидаемым
        :return: None
        """
        category = CategoryModelTest.category
        slug_max_length = category._meta.get_field('slug').max_length
        self.assertEqual(slug_max_length, 255)

    def test_model_slug_unique(self) -> None:
        """
        Проверяем является ли unique поля slug True or False
        :return: None
        """
        category = CategoryModelTest.category
        slug_unique = category._meta.get_field('slug').unique
        self.assertTrue(slug_unique)

    def test_model_slug_db_index(self) -> None:
        """
        Проверяем является ли db_index поля slug True or False
        :return: None
        """
        category = CategoryModelTest.category
        slug_db_index = category._meta.get_field('slug').db_index
        self.assertTrue(slug_db_index)

    def test_model_verbose_name(self) -> None:
        """
        Проверяем совпадает ли verbose_name модели категории с ожидаемым
        :return: None
        """
        category = CategoryModelTest.category
        verbose_name_cat = category._meta.verbose_name
        self.assertEqual(verbose_name_cat, "Категория")

    def test_model_verbose_name_plural(self) -> None:
        """
        Проверяем совпадает ли verbose_name_plural модели категории с ожидаемым
        :return: None
        """
        category = CategoryModelTest.category
        verbose_plural = category._meta.verbose_name_plural
        self.assertEqual(verbose_plural, 'Категории')

    def test_get_absolute_url_model(self) -> None:
        """
        Проверяем get_absolute_url модели Category
        Это приведет к сбою, если urlconf не определен.
        :return: None
        """
        category = CategoryModelTest.category
        get_absolute_url_cat = category.get_absolute_url()
        self.assertEqual(get_absolute_url_cat, '/category/first-post/')


class MaterialModelTestCase(TestCase):
    """
    Тесты модели Material
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.material = Material.objects.create(name='Латунь', slug='Latun')
        cls.name_field = cls.material._meta.get_field('name')
        cls.slug_field = cls.material._meta.get_field('slug')

    @classmethod
    def tearDownClass(cls):
        cls.material.delete()

    def test_model_name_max_length(self) -> None:
        """
        Тест поля name модели Material на max_length
        :return: None
        """
        max_length = getattr(self.name_field, 'max_length')
        self.assertEqual(max_length, 255)

    def test_model_name_verbose_name(self) -> None:
        """
        Тест поля name  модели Material на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.name_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Материал')

    def test_model_slug_max_length(self) -> None:
        """
        Тест поля slug модели Material на max_length
        :return: None
        """
        max_length_slug = getattr(self.slug_field, "max_length")
        self.assertEqual(max_length_slug, 255)

    def test_model_slug_unigue(self) -> None:
        """
        Тест поля slug модели Material на уникальность
        :return:
        """
        slug_unique = getattr(self.slug_field, 'unique')
        self.assertTrue(slug_unique)

    def test_model_field_slug_verbose_name(self) -> None:
        """
        Тест поля slug модели Material на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.slug_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Slug')

    def test_model_verbose_name(self) -> None:
        """
        Тест модели material на verbose_name
        :return: None
        """
        material = MaterialModelTestCase.material
        self.assertEqual(material._meta.verbose_name, 'Материал')

    def test_model_verbose_name_plural(self) -> None:
        """
        Тест модели Material на verbose_name_plural
        :return: None
        """
        self.assertEqual(self.material._meta.verbose_name_plural, 'Материалы')

    def test_model_get_absolute_url(self) -> None:
        """
        Тест get_absolute_url модели Material
        Если не определен urlconf тест покажет ошибку
        :return: None
        """
        self.assertEqual(MaterialModelTestCase.material.get_absolute_url(), 'material/Latun')


class ProductModelTestCase(TestCase):
    """
    Тестирование модели Product
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Метод вызывается перед запуском всех тестов. Создаются экземпляры моделей Material, Category, Product и
        Тестовая база данных
        :return: None
        """
        super().setUpClass()
        cls.material = Material.objects.create(name='Олово', slug='Olovo')
        cls.category = Category.objects.create(name='Ручка для зонтика',
                                               slug='ruchka-dly-zontika', )
        cls.product = Product.objects.create(name='Замок', slug='Zamok', price='1500',
                                             material=cls.material, category=cls.category)

        cls.name_field = cls.product._meta.get_field('name')
        cls.slug_field = cls.product._meta.get_field('slug')
        cls.quantity_field = cls.product._meta.get_field('quantity')
        cls.description_field = cls.product._meta.get_field('description')
        cls.vendor_code_field = cls.product._meta.get_field('vendor_code')
        cls.price_field = cls.product._meta.get_field('price')
        cls.time_create_field = cls.product._meta.get_field('time_create')
        cls.time_update_field = cls.product._meta.get_field('time_update')
        cls.height_field = cls.product._meta.get_field('height')
        cls.length_field = cls.product._meta.get_field('length')
        cls.width_field = cls.product._meta.get_field('width')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Метод вызывается после прогона всех тестов класа. Удаляет экземпляры моделей Material, Category, Product и
        базу данных
        :return: None
        """
        cls.product.delete()
        cls.material.delete()
        cls.category.delete()

    def test_model_name_max_length(self) -> None:
        """
        Тест поля name модели product на max_length
        :return: None
        """
        real_max_length = getattr(self.name_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_name_verbose_name(self) -> None:
        """
        Тест поля name модели product на verbose_name
        :return: None
        """
        real_verbose_name = getattr(self.name_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Название товара')

    def test_model_slug_verbose_name(self) -> None:
        """
        Тест поля slug модели product на verbose_name
        :return: None
        """
        real_slug = getattr(self.slug_field, 'verbose_name')
        self.assertEqual(real_slug, 'Slug')

    def test_model_slug_max_length(self) -> None:
        """
        Тест поля slug модели product на max_length
        :return: None
        """
        real_max_length = getattr(self.slug_field, 'max_length')
        self.assertEqual(real_max_length, 255)

    def test_model_slug_unigue(self) -> None:
        """
        Тест поля slug модели product на unique
        :return: None
        """
        slug_unique = getattr(self.slug_field, 'unique')
        self.assertTrue(slug_unique)

    def test_model_image_upload_to(self) -> None:
        """
        Тест поля image модели product на upload_to
        :return: None
        """
        product = ProductModelTestCase.product
        real_product_image_upload_to = product._meta.get_field('image').upload_to
        self.assertEqual(real_product_image_upload_to, 'product_images/%Y/%m/%d/')

    def test_model_image_default(self) -> None:
        """
        Тест поля image модели product на default
        :return: None
        """

        product = ProductModelTestCase.product
        real_image_default = product._meta.get_field('image').default
        self.assertIsNone(real_image_default)

    def test_model_quantity_field_verbose_name(self) -> None:
        """
        Тест поля quantity модели Product на verbose_name
        :return: None
        """
        quantity_filed_verbose_name = getattr(self.quantity_field, 'verbose_name')
        self.assertEqual(quantity_filed_verbose_name, 'Общее количество')

    def test_model_quantity_field_null(self) -> None:
        """
        Тест поля quantity модели Product на null
        :return:
        """
        quantity_filed_null = getattr(self.quantity_field, 'null')
        self.assertTrue(quantity_filed_null)

    def test_model_quantity_field_blank(self) -> None:
        """
        Тест поля quantity модели Product на blank
        :return: None
        """
        quantity_filed_blank = getattr(self.quantity_field, 'blank')
        self.assertTrue(quantity_filed_blank)

    def test_model_description_field_verbose_name(self) -> None:
        """
        Тест поля description модели Product на verbose_name
        :return: None
        """
        description_field_verbose_name = getattr(self.description_field, 'verbose_name')
        self.assertEqual(description_field_verbose_name, 'Описание товара')

    def test_model_description_field_blank(self) -> None:
        """
        Тест поля description модели Product на blank
        :return: None
        """
        description_field_blank = getattr(self.description_field, 'blank')
        self.assertTrue(description_field_blank)

    def test_model_vendor_code_fild_max_length(self) -> None:
        """
        Тест модели Product поля vendor_code на max_length
        :return: None
        """
        vendor_code_max_length = getattr(self.vendor_code_field, 'max_length')
        self.assertEqual(vendor_code_max_length, 50)

    def test_model_vendor_code_fild_verbose_name(self) -> None:
        """
        Тест модели Product поля vendor_code на verbose_name
        :return: None
        """
        vendor_code_verbose_name = getattr(self.vendor_code_field, 'verbose_name')
        self.assertEqual(vendor_code_verbose_name, 'Артикул')

    def test_model_vendor_code_fild_unique(self) -> None:
        """
        Тест модели Product поля vendor_code на unique
        :return: None
        """
        vendor_code_unique = getattr(self.vendor_code_field, 'unique')
        self.assertTrue(vendor_code_unique)

    def test_model_vendor_code_fild_blank(self) -> None:
        """
        Тест модели Product поля vendor_code на blank
        :return: None
        """
        vendor_code_blank = getattr(self.vendor_code_field, 'blank')
        self.assertTrue(vendor_code_blank)

    def test_model_vendor_code_fild_null(self) -> None:
        """
        Тест модели Product поля vendor_code на null
        :return: None
        """
        vendor_code_null = getattr(self.vendor_code_field, 'null')
        self.assertTrue(vendor_code_null)

    def test_model_vendor_code_fild_default(self) -> None:
        """
        Тест модели Product поля vendor_code на default
        :return: None
        """
        vendor_code_default = getattr(self.vendor_code_field, 'default')
        self.assertIsNone(vendor_code_default)

    def test_model_price_field_verbose_name(self) -> None:
        """
        Тест модели Product поля price на verbose_name
        :return: None
        """
        price_field_verbose_name = getattr(self.price_field, 'verbose_name')
        self.assertEqual(price_field_verbose_name, 'Цена')

    def test_model_price_field_max_digits(self) -> None:
        """
        Тест модели Product поля price на max_digits
        :return: None
        """
        price_field_max_digits = getattr(self.price_field, 'max_digits')
        self.assertEqual(price_field_max_digits, 10)

    def test_model_price_field_decimal_places(self) -> None:
        """
        Тест модели Product поля price на decimal_places
        :return: None
        """
        price_field_decimal_places = getattr(self.price_field, 'decimal_places')
        self.assertEqual(price_field_decimal_places, 2)

    def test_model_price_field_null(self) -> None:
        """
        Тест модели Product поля price на null
        :return: None
        """
        price_field_null = getattr(self.price_field, 'null')
        self.assertTrue(price_field_null)

    def test_model_time_create_field_verbose_name(self) -> None:
        """
        Тест модели Product поля time_create на verbose_name
        :return: None
        """
        time_create_filed_verbose_name = getattr(self.time_create_field, 'verbose_name')
        self.assertEqual(time_create_filed_verbose_name, 'Время создания')

    def test_model_time_create_field_auto_now_add(self) -> None:
        """
        Тест модели Product поля time_create на auto_now_add
        :return: None
        """
        time_create_filed_auto_now_add = getattr(self.time_create_field, 'auto_now_add')
        self.assertTrue(time_create_filed_auto_now_add)

    def test_model_time_update_field_verbose_name(self) -> None:
        """
        Тест модели Product поля time_update на verbose_name
        :return: None
        """
        time_update_filed_verbose_name = getattr(self.time_update_field, 'verbose_name')
        self.assertEqual(time_update_filed_verbose_name, 'Время изменения')

    def test_model_time_update_field_auto_now(self) -> None:
        """
        Тест модели Product поля time_update на auto_now
        :return: None
        """
        time_update_filed_auto_now = getattr(self.time_update_field, 'auto_now')
        self.assertTrue(time_update_filed_auto_now)

    def test_model_height_field_verbose_name(self) -> None:
        """
        Тест модели Product поля height на verbose_name
        :return: None
        """
        height_field_verbose_name = getattr(self.height_field, 'verbose_name')
        self.assertEqual(height_field_verbose_name, 'Высота')

    def test_model_height_field_blank(self) -> None:
        """
        Тест модели Product поля height на blank
        :return: None
        """
        height_field_blank = getattr(self.height_field, 'blank')
        self.assertTrue(height_field_blank)

    def test_model_height_field_null(self) -> None:
        """
        Тест модели Product поля height на null
        :return: None
        """
        height_field_null = getattr(self.height_field, 'null')
        self.assertTrue(height_field_null)

    def test_model_height_field_default(self) -> None:
        """
        Тест модели Product поля height на default
        :return: None
        """
        height_field_default = getattr(self.height_field, 'default')
        self.assertEqual(height_field_default, 0)

    def test_model_length_field_verbose_name(self) -> None:
        """
        Тест модели Product поля length на verbose_name
        :return: None
        """
        length_field_verbose_name = getattr(self.length_field, 'verbose_name')
        self.assertEqual(length_field_verbose_name, 'Длина')

    def test_model_length_field_blank(self) -> None:
        """
        Тест модели Product поля length на blank
        :return: None
        """
        length_field_blank = getattr(self.height_field, 'blank')
        self.assertTrue(length_field_blank)

    def test_model_length_field_null(self) -> None:
        """
        Тест модели Product поля length на null
        :return: None
        """
        length_field_null = getattr(self.length_field, 'null')
        self.assertTrue(length_field_null)

    def test_model_length_field_default(self) -> None:
        """
        Тест модели Product поля length на default
        :return: None
        """
        length_field_default = getattr(self.length_field, 'default')
        self.assertEqual(length_field_default, 0)

    def test_model_width_field_verbose_name(self) -> None:
        """
        Тест модели Product поля width на verbose_name
        :return: None
        """
        width_field_verbose_name = getattr(self.width_field, 'verbose_name')
        self.assertEqual(width_field_verbose_name, 'Ширина')

    def test_model_width_field_blank(self) -> None:
        """
        Тест модели Product поля width на blank
        :return: None
        """
        width_field_blank = getattr(self.width_field, 'blank')
        self.assertTrue(width_field_blank)

    def test_model_width_field_null(self) -> None:
        """
        Тест модели Product поля width на null
        :return: None
        """
        width_field_null = getattr(self.width_field, 'null')
        self.assertTrue(width_field_null)

    def test_model_width_field_default(self) -> None:
        """
        Тест модели Product поля width на default
        :return: None
        """
        width_field_default = getattr(self.width_field, 'default')
        self.assertEqual(width_field_default, 0)

    def test_product_model_str(self) -> None:
        """
        Тест строкового отображения модели Product
        :return: None
        """
        self.assertEqual(str(self.product), str(self.product.name))

    def test_product_str_false(self) -> None:
        """
        Проверяем строковое отображение модели Product с ошибкой.
        :return: None
        """
        self.assertEqual(str(self.product), 'Zamolee')

    def test_product_get_absolute_url(self) -> None:
        """
        Тест get_absolute_url модели Product.
        :return: None
        """
        product = ProductModelTestCase.product
        self.assertEqual(product.get_absolute_url(), '/product/Zamok/')


class ProductImageModelTestCase(TestCase):
    """
    Тестируем модель ProductImage
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Создаем объекты классов модели и тестовую базу данных
        :return: None
        """
        super().setUpClass()
        cls.material = Material.objects.create(name='Цинк', slug='Chink')
        cls.category = Category.objects.create(name='Колесико для мебели', slug='Kolesyko-dly-mebely')
        cls.product = Product.objects.create(name='Колесо для тумбы', slug='Koleso-dly-tumby', price=2000,
                                             material=cls.material, category=cls.category)
        cls.product_image = ProductImage.objects.create(product=cls.product)

        cls.product_image_model_product_field = cls.product_image._meta.get_field('product')
        cls.product_image_model_image_field = cls.product_image._meta.get_field('image')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Удаление тестовой базы данных поле прогона тестов
        :return: None
        """
        cls.product.delete()
        cls.material.delete()
        cls.category.delete()
        cls.product_image.delete()

    def test_model_product_field_verbose_name(self) -> None:
        """
        Тест модели ProductImage поля product на verbose_name
        :return: None
        """
        product_image_verbose_name = getattr(self.product_image_model_product_field, 'verbose_name')
        real_verbose_name = 'Изображение товара'
        self.assertEqual(product_image_verbose_name, real_verbose_name)

    def test_model_product_field_related_name(self) -> None:
        """
        Тест модели ProductImage поля product на related_name
        Тест упадет, так как 'ForeignKey' object has no attribute 'related_name'
        :return: None
        """
        product_image_product_field = getattr(self.product_image_model_product_field, 'related_name')
        self.assertEqual(product_image_product_field, 'product_image')

    def test_model_product_image_field_verbose_name(self) -> None:
        """
        Тест модели ProductImage поля image на verbose_name
        :return: None
        """

        product_image_field_verbose_name = getattr(self.product_image_model_image_field, 'verbose_name')
        self.assertEqual(product_image_field_verbose_name, 'Изображение')

    def test_model_product_image_field_upload_to(self) -> None:
        """
        Тест модели ProductImage поля image на upload_to
        :return: None
        """
        product_image_field_upload_to = getattr(self.product_image_model_image_field, 'upload_to')
        self.assertEqual(product_image_field_upload_to, 'product_images/%Y/%m/%d/')

    def test_model_product_image_field_default(self) -> None:
        """
        Тест модели ProductImage поля image на default
        :return: None
        """
        product_image_field_default = getattr(self.product_image_model_image_field, 'default')
        self.assertIsNone(product_image_field_default)

    def test_model_product_image_field_null(self) -> None:
        """
        Тест модели ProductImage поля image на null
        :return: None
        """
        product_image_field_null = getattr(self.product_image_model_image_field, 'null')
        self.assertTrue(product_image_field_null)

    def test_model_product_image_field_blank(self) -> None:
        """
        Тест модели ProductImage поля image на blank
        :return: None
        """
        product_image_field_blank = getattr(self.product_image_model_image_field, 'blank')
        self.assertTrue(product_image_field_blank)

    def test_model_verbose_name(self) -> None:
        """
        Тестируем модель ProductImage на verbose_name
        :return: None
        """
        product_image = ProductImageModelTestCase.product_image
        real_verbose_name = 'Изображение товара'
        self.assertEqual(product_image._meta.verbose_name, real_verbose_name)

    def test_model_verbose_name_plural(self) -> None:
        """
        Тестируем модель ProductImage на verbose_name_plural
        :return: None
        """
        product_image = ProductImageModelTestCase.product_image
        real_verbose_name_plural = 'Изображение товаров'
        self.assertEqual(product_image._meta.verbose_name_plural, real_verbose_name_plural)
