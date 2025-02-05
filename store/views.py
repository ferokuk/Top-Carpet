from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.paginator import Paginator
from django.db.models import Count, Min, Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from order.models import OrderItem
from store.forms import CommentForm
from store.models import Carpet, Material, Category, Country, CarpetSize, Comment, Favorite


def index(request):
    context = {
        "current_page": "index"
    }
    return render(request, 'index.html', context)


def about(request):
    context = {
        "title": "О нас",
        "current_page": "about"
    }
    return render(request, 'about.html', context)


def catalog(request):
    carpets = Carpet.objects.annotate(min_price=Min("carpet_sizes__price"), avg_rating=Avg('comment__rating'))
    materials = Material.objects.annotate(carpet_count=Count('carpet'))
    categories = Category.objects.annotate(carpet_count=Count('carpet'))
    countries = Country.objects.annotate(carpet_count=Count('carpet'))

    materials_param = request.GET.getlist("material")
    categories_param = request.GET.getlist("category")
    countries_param = request.GET.getlist("country")
    sizes_param = request.GET.getlist("size")
    search = request.GET.get("search")
    price_sort = request.GET.get("price_sort")
    quantity = request.GET.get("quantity")
    favorites = request.GET.get("favorites")

    if categories_param:
        carpets = carpets.filter(category__in=categories_param)
    if materials_param:
        carpets = carpets.filter(materials__in=materials_param)
    if countries_param:
        carpets = carpets.filter(country__in=countries_param)
    if sizes_param:
        carpets = carpets.filter(size__in=sizes_param)
    if search:
        carpets = carpets.filter(name__icontains=search)
    if price_sort:
        carpets = carpets.order_by("min_price" if price_sort == "asc" else "-min_price")
    if quantity:
        if quantity == "have":
            carpets = carpets.filter(carpet_sizes__quantity__gt=0)
        else:
            carpets = carpets.filter(carpet_sizes__quantity=0)
    if favorites:
        favorite_carpets_ids = Favorite.objects.filter(user=request.user).values_list('carpet_id', flat=True)
        carpets = carpets.filter(id__in=favorite_carpets_ids)
    if request.user.is_authenticated:
        results = carpets.all()
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('carpet_id', flat=True))

        carpets_with_favorites = [
            {'carpet': carpet, 'is_favorite': carpet.id in user_favorites}
            for carpet in results
        ]
    else:
        results = carpets.all()
        user_favorites = []
        carpets_with_favorites = [
            {'carpet': carpet, 'is_favorite': False in results}
            for carpet in results
        ]
    page = request.GET.get('page', 1)
    paginator = Paginator(carpets_with_favorites, 16)
    current_page = paginator.page(int(page))
    context = {"title": "Каталог",
               "params": dict(request.GET),
               "current_page": "catalog",
               "products": current_page,
               "materials": materials,
               "categories": categories,
               "countries": countries,
               "favs_carpet_count": len(user_favorites),
               }
    return render(request, 'catalog.html', context)


def carpet_details(request, carpet_id: int):
    carpet = get_object_or_404(Carpet.objects.filter(id=carpet_id))
    comments = Comment.objects.filter(carpet=carpet.id).all()
    if request.user.is_authenticated:
        can_comment = OrderItem.objects.filter(carpet_size__carpet=carpet, order__user_id=request.user.id).exists()
    else:
        can_comment = False
    sizes = CarpetSize.objects.filter(carpet=carpet.id).order_by('price').all()
    comment = Comment.objects.filter(user=request.user.id, carpet=carpet).first()
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 20)
    current_page = paginator.page(int(page))
    context = {
        "current_page": "catalog",
        "carpet": carpet,
        "sizes": sizes,
        "title": carpet.name,
        "comments": current_page,
        "can_comment": can_comment,
        "comment": comment,
    }
    return render(request, 'carpet_details.html', context)


def get_carpet_quantity_by_size(request):
    size_id = request.POST.get("size_id")
    carpet_info = CarpetSize.objects.filter(id=size_id).first()
    context = {"quantity": intcomma(carpet_info.quantity),
               "price": intcomma(carpet_info.price),
               "waiting_days": intcomma(carpet_info.waiting_days),
               }
    return JsonResponse(context)


@login_required
def add_comment(request, carpet_id: int):
    carpet = get_object_or_404(Carpet, pk=carpet_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.filter(user=request.user, carpet=carpet).first()
            if comment is None:
                comment = form.save(commit=False)
            else:
                comment.text = form.data.get("text")
                comment.rating = form.data.get("rating")
            comment.carpet = carpet
            comment.user = request.user
            comment.save()
    return redirect('store:carpet_details', carpet_id=carpet_id)


@login_required
def remove_comment(request, carpet_id: int):
    carpet = get_object_or_404(Carpet, pk=carpet_id)

    if request.method == 'POST':
        comment = Comment.objects.filter(user=request.user, carpet=carpet).first()
        if comment is not None:
            comment.delete()
    return redirect('store:carpet_details', carpet_id=carpet_id)


@login_required
def add_to_favs(request):
    carpet_id = request.POST.get("carpet_id")
    fav = Favorite.objects.filter(user=request.user, carpet_id=carpet_id).first()
    context = {
        "type": "Успешно"
    }
    if fav:
        fav.delete()
        context["message"] = "Ковёр удалён из избранного"
    else:
        fav = Favorite(user=request.user, carpet_id=carpet_id)
        fav.save()
        context["message"] = "Ковёр добавлен в избранное"
    return JsonResponse(context)
