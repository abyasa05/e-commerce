from django.urls import path
from main.views import show_main, create_shop_entry, show_xml, show_json, show_xml_by_id, \
    show_json_by_id, register, login_user, logout_user, edit_item, delete_item, \
    create_shop_entry_ajax, create_shop_entry_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create_shop_entry', create_shop_entry, name='create_shop_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-item/<uuid:id>', edit_item, name='edit_item'),
    path('delete/<uuid:id>', delete_item, name='delete_item'),
    path('create-ajax', create_shop_entry_ajax, name='create_shop_entry_ajax'),
    path('create-flutter/', create_shop_entry_flutter, name='create_shop_entry_flutter'),
]