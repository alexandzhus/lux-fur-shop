from django.contrib import admin

from .models import *

class OrderItemsTabularInline(admin.TabularInline):
    model = OrderItems
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'time_create', 'time_update', 'paid']
    list_display_links = ['id', 'user','first_name']
    list_filter = ['paid', 'time_create', 'time_update']
    inlines = [OrderItemsTabularInline, ]


@admin.register(OrderItems)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'product_amount', 'product_price', 'order_total_cost']
    list_display_links = ['id', 'order']

    @admin.display(description="Общая стоимость")
    def order_total_cost(self, order: OrderItems):
        return OrderItems.get_cost(order)
