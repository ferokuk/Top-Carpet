from django.urls import path

from users.forms import UserLoginForm, UserRegistrationForm
from users.views import login, registration, logout, profile

app_name = 'user'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
]
