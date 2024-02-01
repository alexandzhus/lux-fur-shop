from django.db import models
from django.urls import reverse


# Create your models here.


class Product(models.Model):
    """
    Модель продукта
    """
    name = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug", db_index=True)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', null=True, blank=True, default=None,
                              verbose_name="Изображение")
    quantity = models.IntegerField(null=True, blank=True, verbose_name="Общее количество")
    material = models.CharField(max_length=255, blank=True, verbose_name="Материал")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    vendor_code = models.IntegerField(null=True, blank=True, default=None, unique=True, verbose_name="Артикул")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products',
                                 verbose_name="Категория")
    height = models.FloatField(blank=True, null=True, verbose_name="Высота", default=0)
    length = models.FloatField(blank=True, null=True, verbose_name="Длина", default=0)
    width = models.FloatField(blank=True, null=True, verbose_name="Ширина", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

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
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug})
