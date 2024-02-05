from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class Product(models.Model):
    """
    Модель продукта
    """
    name = models.CharField(max_length=255, verbose_name="Название товара", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug", db_index=True)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', null=True, blank=True, default=None,
                              verbose_name="Изображение")
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Общее количество")
    material = models.ForeignKey('Material', on_delete=models.PROTECT,
                                 blank=True, verbose_name="Материал", related_name='material')
    description = models.TextField(blank=True, verbose_name="Описание товара")
    vendor_code = models.IntegerField(null=True, blank=True, default=None, unique=True, verbose_name="Артикул")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products',
                                 verbose_name="Категория")
    height = models.FloatField(blank=True, null=True, verbose_name="Высота", default=0)
    length = models.FloatField(blank=True, null=True, verbose_name="Длина", default=0)
    width = models.FloatField(blank=True, null=True, verbose_name="Ширина", default=0)

    def __str__(self):
        """
        Каждая запись модели будет идентифицироваться благодаря этому методу
        :return:
        """
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-time_create']
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"product_slug": self.slug})


class Category(models.Model):
    """
    Модель категорий товаров
    """
    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug})


class Material(models.Model):
    """
    Модель материал товаров
    """
    name = models.CharField(max_length=255, verbose_name="Материал")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def get_absolute_url(self):
        return reverse('material', kwargs={"material_slug": self.slug})