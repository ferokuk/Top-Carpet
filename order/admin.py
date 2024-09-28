from django.contrib import admin

from order.models import Order, OrderItem, Cart

admin.site.register(Cart)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "created_at")
    ordering = ("user", "phone_number", "created_at")
    search_fields = ("user__username", "phone_number", "created_at")
    search_help_text = "Введите пользователя, телефон или дату заказа"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "carpet_name", "quantity", "price", "created_timestamp")
    ordering = ("order", "carpet_size__carpet__name", "carpet_size__quantity", "carpet_size__price")
    search_fields = ("order__id", "carpet_size__carpet__name", "order__user__username")
    search_help_text = "Введите номер заказа, название ковра или имя покупателя"

    def carpet_name(self, obj):
        return obj.carpet_size.carpet.name

    carpet_name.short_description = "Ковер"  # Customizing the column header

    def quantity(self, obj):
        return obj.carpet_size.quantity

    quantity.short_description = "Количество"

    def price(self, obj):
        return obj.carpet_size.price

    price.short_description = "Цена, ₽"
