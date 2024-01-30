from django.contrib import admin

from .models import *
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'image', 'description', 'material', 'category', 'height', 'length', 'width']
    list_display = ['name', 'slug', 'image', 'material', 'time_create', 'time_update', 'category', 'height', 'length', 'width']
    list_display_links = ['name', 'slug', 'image']




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", 'name')
    list_display_links = ("id", 'name')
