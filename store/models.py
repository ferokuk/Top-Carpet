from django.contrib.auth.models import User
from django.db import models
from colorfield.fields import ColorField
from django.db.models import UniqueConstraint


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=200, verbose_name='Описание')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=250, verbose_name='Описание')

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Shape(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    hex_value = ColorField(format="hex", verbose_name="Выберите значение")

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='static/images/carpets', null=True, blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return self.image.name


class Carpet(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    materials = models.ManyToManyField(Material, verbose_name='Материалы')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна производства')
    shape = models.ForeignKey(Shape, on_delete=models.CASCADE, verbose_name='Форма')
    images = models.ManyToManyField(Image, verbose_name="Фото")
    pile_height = models.IntegerField(verbose_name='Высота ворса, мм')
    colors = models.ManyToManyField(Color, verbose_name="Цвета")
    description = models.TextField(max_length=2000, verbose_name="Описание")

    def get_sizes(self):
        return self.carpet_sizes.all()

    def get_quantity_for_size(self, size):
        return self.carpet_sizes.filter(size=size).first().quantity if self.carpet_sizes.filter(
            size=size).exists() else 0

    class Meta:
        verbose_name = "Ковёр"
        verbose_name_plural = "Ковры"

    def __str__(self):
        return self.name


class CarpetSize(models.Model):
    carpet = models.ForeignKey(Carpet, on_delete=models.CASCADE, related_name='carpet_sizes', verbose_name='Ковёр')
    width = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Ширина, см')
    length = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='Длина, см')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Цена, ₽')
    waiting_days = models.IntegerField(default=0, verbose_name='Время ожидания в днях')

    class Meta:
        verbose_name = "Размер ковра"
        verbose_name_plural = "Размеры ковров"
        constraints = [
            UniqueConstraint(fields=['carpet', 'width', 'length'], name='unique_carpet_size')
        ]

    def __str__(self):
        return f"{self.carpet.name} {self.width} x {self.length} см | {self.quantity} шт."


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    carpet = models.ForeignKey(Carpet, on_delete=models.CASCADE, verbose_name='Ковёр')
    text = models.TextField(max_length=500, verbose_name='Текст')
    rating = models.PositiveIntegerField(default=1, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.rating}⭐ отзыв от {self.user.username} про ковёр "{self.carpet.name}"'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Пользователь')
    carpet = models.ForeignKey(Carpet, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Ковёр')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        unique_together = ('user', 'carpet')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'{self.user.username} добавил в избранное {self.carpet}'
