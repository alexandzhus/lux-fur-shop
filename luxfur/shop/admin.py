from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'image', 'description', 'price', 'vendor_code',
              'quantity', 'material', 'category', 'height', 'length', 'width']
    list_display = ['id', 'name', 'product_image', 'slug', 'price', 'vendor_code',
                    'quantity', 'material', 'time_create',
                    'time_update', 'category', 'height', 'length', 'width', 'brief_descriptions']
    list_display_links = ['name', 'slug']
    prepopulated_fields = {'slug': ("name",)}
    list_filter = ('name', 'price', 'quantity')
    list_editable = ('price', 'quantity',)
    list_per_page = 5
    save_on_top = True
    inlines = [ProductImageTabularInline,]

    @admin.display(description="Изображение")
    def product_image(self, product: Product):
        """
        Метод позволяет отображать поле с изображением в админке
        """
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width=50>')
        else:
            return "без изображения"


    @admin.display(description="Краткое описание товара")
    def brief_descriptions(self, product: Product):

        return f'{product.description[0:75]}' + "..."

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", 'product', 'product_image', 'image')
    list_display_links = ("id", 'product', 'image')

    @admin.display(description="Изображение")
    def product_image(self, product_image: ProductImage):
        """
        Метод позволяет отображать поле с изображением в админке
        """
        if product_image.image:
            return mark_safe(f'<img src="{product_image.image.url}" width=50>')
        else:
            return "без изображения"



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'slug')
    list_display_links = ("id", 'name')
    prepopulated_fields = {'slug': ("name", )}


@admin.register(Material)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'slug')
    list_display_links = ("id", 'name')
    prepopulated_fields = {'slug': ("name", )}
