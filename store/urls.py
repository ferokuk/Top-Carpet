from django.urls import path

from store.views import *

app_name = 'store'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('carpet/<int:carpet_id>/', carpet_details, name='carpet_details'),
    path('carpet/<int:carpet_id>/add_comment/', add_comment, name="add_comment"),
    path('carpet/<int:carpet_id>/remove_comment/', remove_comment, name="remove_comment"),
    path('get_quantity', get_carpet_quantity_by_size, name='get_quantity'),
    path('add_to_fav', add_to_favs, name='add_to_favs'),
]
