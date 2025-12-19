from django.urls import path
from .views import menu_list, menu_3d

urlpatterns = [
    path('', menu_list, name='menu_list'),
    path('3d/', menu_3d, name='menu_3d'),
]
