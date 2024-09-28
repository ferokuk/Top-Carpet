from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{user.username}, Вы успешно вошли в аккаунт", 'success')
                next_url = request.GET.get('next', None)
                if next_url:
                    # Если параметр 'next' существует, выполнить перенаправление на указанный URL-адрес
                    return redirect(next_url)
                return redirect("catalog:catalog")
            messages.error(request, f"Неправильное имя пользователя или пароль", 'danger')
            return redirect("user:login")
        else:
            messages.error(request, f"Неправильное имя пользователя или пароль", 'danger')
            return redirect("user:login")
    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form,
        'current_page': 'login',
    }
    return render(request, 'login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)

            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return redirect('catalog:catalog')
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Регистрация",
        "form": form,
        "current_page": "registration",
    }
    return render(request, "registration.html", context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect("user:login")


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен", "success")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        "title": "Профиль",
        "form": form,
        "current_page": "profile",
    }
    return render(request, "profile.html", context)
