from django.contrib.auth.models import User
from django.db import models

from store.models import Carpet, CarpetSize


class OrderItemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ №{self.id} от {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    carpet_size = models.ForeignKey(CarpetSize, on_delete=models.CASCADE, verbose_name='Ковёр', null=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена ₽')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

    def products_price(self):
        return round(self.price * self.quantity, 2)

    objects = OrderItemQueryset.as_manager()

    def __str__(self):
        return f'{self.quantity} шт. ковра {self.carpet_size.carpet.name} в заказе №{self.order.id}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    carpet_size = models.ForeignKey(CarpetSize, on_delete=models.CASCADE, verbose_name='Ковёр', null=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def products_price(self):
        return round(self.carpet_size.price * self.quantity, 2)

    objects = OrderItemQueryset.as_manager()

    def __str__(self):
        return f'{self.user.username} | {self.carpet_size.carpet} {self.carpet_size.width} x {self.carpet_size.length} см. | {self.quantity} шт.'
