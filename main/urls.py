from django.urls import path
from main.views import show_main, create_shop_entry

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create_shop_entry', create_shop_entry, name='create_shop_entry'),
]