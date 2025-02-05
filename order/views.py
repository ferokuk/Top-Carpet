import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from order.models import Cart, Order, OrderItem
from store.models import CarpetSize


# Create your views here.
@login_required
def show_cart(request):
    cart = Cart.objects.filter(user=request.user).order_by('id').prefetch_related('carpet_size')
    context = {
        "title": f"Корзина {request.user.username}",
        "cart": cart,
        "current_page": "cart",
    }
    return render(request, 'cart.html', context)


def add_to_cart(request):
    if request.method != "POST":
        return redirect("store:catalog")
    if not request.user.is_authenticated:
        return JsonResponse({"type": "Ошибка", "message": "Авторизуйтесь для добавления в корзину"})
    carpet_size_id = request.POST.get("carpet_size_id")
    carpet = CarpetSize.objects.get(id=carpet_size_id)
    if carpet.quantity == 0:
        return JsonResponse({"type": "Ошибка", "message": "Этого ковра нет в наличии"})
    carts = Cart.objects.filter(user=request.user.id, carpet_size=carpet)

    if carts.exists():
        cart = carts.first()
        if cart:
            cart.quantity += 1
            cart.save()
    else:
        Cart.objects.create(user=request.user, carpet_size=carpet, quantity=1)
    return JsonResponse({"type": "Успешно",
                         "message": f"Ковёр {carpet.carpet.name} {carpet.width} x {carpet.length} см. добавлен в корзину"})


@login_required
def cart_change_quantity(request):
    if request.method != "POST":
        return redirect("store:catalog")
    cart_id = request.POST.get('cart_id')
    quantity = request.POST.get('quantity')
    phone = request.POST.get('phone')
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    cart = Cart.objects.filter(user=request.user).order_by('id').select_related('carpet_size')
    cart_items_html = render_to_string(
        "cart_items_list.html", {'cart': cart, 'phone': phone}, request=request
    )

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity
    }

    return JsonResponse(response_data)


@login_required
def cart_remove(request):
    cart_id = request.POST.get('cart_id')
    phone = request.POST.get("phone")
    cart = Cart.objects.get(id=cart_id)
    cart.delete()

    user_cart = Cart.objects.filter(user=request.user).order_by('id').select_related('carpet_size')
    cart_items_html = render_to_string(
        "cart_items_list.html", {'cart': user_cart, 'phone': phone}, request=request
    )

    response_data = {
        "type": "Успешно",
        "message": "Товар удален из корзины",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


@login_required
def create_order(request):
    if request.method != "POST":
        return redirect("order:cart")
    phone = request.POST.get("phone")
    pattern = re.compile(r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$')
    if not bool(pattern.match(phone)):
        messages.error(request, "Неправильный формат телефона", "danger")
        return redirect("order:cart")
    try:
        with transaction.atomic():
            user = request.user
            cart_items = Cart.objects.filter(user=user)

            if cart_items.exists():
                # Создать заказ
                order = Order.objects.create(
                    user=request.user,
                    phone_number=phone,
                )

                for cart_item in cart_items:
                    carpet_size = cart_item.carpet_size
                    name = cart_item.carpet_size.carpet.name
                    quantity = cart_item.quantity
                    price = cart_item.carpet_size.price
                    size = f"{carpet_size.width} x {carpet_size.length} см."
                    if carpet_size.quantity < quantity:
                        raise ValidationError(
                            f'Недостаточное количество {name} {size}. В наличии - {carpet_size.quantity}')

                    OrderItem.objects.create(
                        order=order,
                        carpet_size=carpet_size,
                        price=price,
                        quantity=quantity,
                    )
                    carpet_size.quantity -= quantity
                    carpet_size.save()

                cart_items.delete()
                messages.success(request, "Заказ успешно оформлен!", "success")
                return redirect("order:my_orders")
    except ValidationError as e:
        messages.error(request, e.message, "danger")
        return redirect("order:cart")
    messages.error(request, "Корзина пустая", "warning")
    return redirect("order:cart")


@login_required
def my_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.select_related('carpet_size'))
        )
        .order_by('-id')
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 10)
    current_page = paginator.page(int(page))
    context = {
        "title": "Мои заказы",
        "orders": current_page,
        "current_page": "orders",
    }
    return render(request, "my_orders.html", context)
