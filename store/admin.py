from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    ordering = ("name", "description")
    search_fields = ("name", "description")
    search_help_text = "Введите часть названия или описания"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    ordering = ("name", "description")
    search_fields = ("name", "description")
    search_help_text = "Введите часть названия или описания"


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)
    search_help_text = "Введите часть названия"


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "color_display")
    ordering = ("name",)
    search_fields = ("name",)

    def color_display(self, obj):
        return mark_safe(
            '<div style="color: {};">{}</div>'.format(obj.hex_value, obj.name))

    search_help_text = "Введите часть названия или шестнадцатеричного кода"


@admin.register(Carpet)
class CarpetAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "get_materials", "country", "get_colors", "get_sizes")
    ordering = ("name", "category", "country")
    search_fields = ("name", "category__name", "colors__name", "country__name", "description")
    search_help_text = "Введите часть названия, категории, цвета, страны или описания"

    def get_materials(self, carpet):
        return ', '.join(str(item) for item in carpet.materials.all())

    def get_colors(self, carpet):
        return ', '.join(str(item) for item in carpet.colors.all())

    def get_sizes(self, carpet):
        return sum(carpet.quantity for carpet in carpet.get_sizes())

    get_materials.short_description = "Материалы"
    get_colors.short_description = "Цвета"
    get_sizes.short_description = "Количество, всего"


@admin.register(CarpetSize)
class CarpetSizeAdmin(admin.ModelAdmin):
    list_display = ("carpet", "width", "length", "price", "quantity", "waiting_days")
    ordering = ("width", "length", "carpet__name", "price", "quantity", "waiting_days")
    search_fields = ("width", "length", "carpet__name", "quantity")
    search_help_text = "Введите ширину, длину, название ковра или его количество"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "carpet", "text", "rating", "created_at", "updated_at")
    ordering = ("user", "carpet", "rating", "created_at", "updated_at")
    search_fields = ("user", "carpet", "text", "created_at", "updated_at")
    search_help_text = "Введите пользователя, название ковра, часть комментария или дату"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "carpet", "created_at")
    ordering = ("user", "carpet", "created_at")
    search_fields = ("user", "carpet", "created_at")
    search_help_text = "Введите пользователя, название ковра, или дату"


admin.site.register(Shape)

admin.site.register(Image)
